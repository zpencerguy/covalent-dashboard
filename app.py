import os
from pathlib import Path
import dash
from dash import html, dcc
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask import Flask
import plotly.express as px
import pandas as pd
from flask_caching import Cache

from pages import layout
from data.covalent_api import CovalentApi
from data.config import TABLE_INFO
from helpers.formatting import f_img, etherscan_link, etherscan_txn_link

BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR.joinpath('data/cache')

server = Flask(__name__)
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    server=server,
    suppress_callback_exceptions=True
)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': CACHE_DIR
})


app.title = "DEX Dashboard"

api = CovalentApi()

# seconds
TIMEOUT = 1800


@cache.memoize(timeout=TIMEOUT)
def query_pool_data(chain, dex):
    return api.get_dex_pool(chain_id=chain, dexname=dex)


def pool_data(chain, dex):
    return query_pool_data(chain, dex)


def serve_layout():
    return html.Div([
        dcc.Location(id="url"),
        html.Div(id="page-content")
    ])


app.layout = serve_layout()


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return layout.dashboard


@app.callback(
    Output("collapse", "is_open"),
    Input("collapse_button", "n_clicks"),
    State("collapse", "is_open"))
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [Output("volume_chart_main", "figure"),
     Output("liquidity_chart_main", "figure")],
    Input("dex_name", "value"),
    Input("chain_id", "value")
)
def display_volume_chart(dex, chain):
    if dex and chain:
        sushi_ecosystem_data = api.get_dex_ecosystem(chain_id=chain, dexname=dex)
        df_volume = pd.DataFrame(sushi_ecosystem_data['data']['items'][0]['volume_chart_7d'])
        fig_volume = px.line(df_volume, x="dt", y="volume_quote")

        df_liquidity = pd.DataFrame(sushi_ecosystem_data['data']['items'][0]['liquidity_chart_7d'])
        fig_liquidity = px.line(df_liquidity, x="dt", y="liquidity_quote")

        return fig_volume, fig_liquidity
    else:
        return dash.no_update


@app.callback(
    [Output("active_pairs", "children"),
     Output("total_swaps", "children"),
     Output("total_fees", "children"),
     Output("gas_quote", "children")],
    Input("dex_name", "value"),
    Input("chain_id", "value")
)
def display_kpis(dex, chain):
    if dex and chain:
        sushi_ecosystem_data = api.get_dex_ecosystem(chain_id=chain, dexname=dex)
        ap = "{:0,.0f}".format(sushi_ecosystem_data['data']['items'][0]['total_active_pairs_7d'])
        ts = "{:0,.0f}".format(sushi_ecosystem_data['data']['items'][0]['total_swaps_24h'])
        tf = "{:0,.0f}".format(sushi_ecosystem_data['data']['items'][0]['total_fees_24h'])
        gq = "{:0,.4f}".format(sushi_ecosystem_data['data']['items'][0]['gas_token_price_quote'])
        return [ap, ts, tf, gq]
    else:
        return dash.no_update


@app.callback(
    Output("pools_data", "children"),
    Input("dex_name", "value"),
    Input("chain_id", "value"),
    Input("token_search", "value")
)
def display_pools_table(dex, chain, token):
    if dex and chain:
        sushi_pool_data = pool_data(chain, dex)
        df_pools = pd.json_normalize(sushi_pool_data['data']['items'])
        if token:
            print(token)
            df_pools = df_pools.loc[
                (df_pools['token_0.contract_ticker_symbol'].str.lower().str.contains(token)) |
                (df_pools['token_1.contract_ticker_symbol'].str.lower().str.contains(token))
            ]
        df_pools['Pair'] = df_pools.apply(
            lambda x: f"{x['token_0.contract_ticker_symbol']} - {x['token_1.contract_ticker_symbol']}",
            axis=1
        )
        df_pools['Pair'] = df_pools.apply(etherscan_link, name="exchange", axis=1)
        df_pools["token_0.logo_url"] = df_pools.apply(f_img, name="token_0.logo_url", axis=1)
        df_pools["token_1.logo_url"] = df_pools.apply(f_img, name="token_1.logo_url", axis=1)
        dt = DataTable(
            id="pools_datatable",
            columns=[
                {
                    "name": TABLE_INFO["liquidity_pools"]["column_names"].get(i, i),
                    "id": i,
                    "presentation": TABLE_INFO["liquidity_pools"]["presentation"].get(i),
                    "format": TABLE_INFO["liquidity_pools"]["format"].get(i),
                    "type": TABLE_INFO["liquidity_pools"]["type"].get(i)
                } for i in TABLE_INFO["liquidity_pools"]["column_ids"]
            ],
            hidden_columns=TABLE_INFO["liquidity_pools"]["hidden"],
            data=df_pools.to_dict('records'),
            page_size=25,
            sort_action="native",
            filter_action="native",
            row_selectable="single",
            fixed_rows={"headers": True},
            css=[{"selector": ".show-hide", "rule": "display: none"}],
            style_as_list_view=True,
            style_table={"overflowX": "auto", "overflowY": "auto"},
            style_header={
                "backgroundColor": "white",
                "fontWeight": "bold",
                "height": "auto",
                "whitespace": "normal",
                "minWidth": "20px",
                "maxWidth": "80px"
            },
            style_cell={
                "whiteSpace": "normal",
                "textAlign": "left",
                "textOverflow": "ellipsis",
                "minWidth": "20px"
            }
        )
        return dt
    else:
        return dash.no_update


@app.callback(
    Output("txns_data", "children"),
    Input("pools_datatable", "derived_virtual_selected_rows"),
    State("pools_datatable", "derived_virtual_data"),
    prevent_initial_call=True
)
def display_txns_table(row, data):
    if row:
        df = pd.DataFrame(data)
        address = df.iloc[row[0]].exchange
        response = api.get_txn_by_address(address=address)
        df_txns = pd.json_normalize(response['data']['items'])
        df_txns['tx_hash'] = df_txns.apply(etherscan_txn_link, name="tx_hash", axis=1)
        dt = DataTable(
            id="txns_datatable",
            columns=[
                {
                    "name": TABLE_INFO["pool_transactions"]["column_names"].get(i, i),
                    "id": i,
                    "presentation": TABLE_INFO["pool_transactions"]["presentation"].get(i),
                    "format": TABLE_INFO["pool_transactions"]["format"].get(i),
                    "type": TABLE_INFO["pool_transactions"]["type"].get(i)
                } for i in TABLE_INFO["pool_transactions"]["column_ids"]
            ],
            hidden_columns=TABLE_INFO["pool_transactions"]["hidden"],
            data=df_txns.to_dict('records'),
            page_size=25,
            sort_action="native",
            filter_action="native",
            fixed_rows={"headers": True},
            css=[{"selector": ".show-hide", "rule": "display: none"}],
            style_as_list_view=True,
            style_table={"overflowX": "auto", "overflowY": "auto"},
            style_header={
                "backgroundColor": "white",
                "fontWeight": "bold",
                "height": "auto",
                "whitespace": "normal",
                "minWidth": "20px",
                "maxWidth": "80px"
            },
            style_cell={
                "whiteSpace": "normal",
                "textAlign": "left",
                "textOverflow": "ellipsis",
                "minWidth": "20px"
            }
        )
        return dt
    else:
        return dash.no_update


if __name__ == "__main__":
    app.run_server(port=os.getenv("PORT_NUMBER", 8080), host="0.0.0.0")
