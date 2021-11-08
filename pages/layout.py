from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable


def generate_header():
    return dbc.NavbarSimple(
                children=[
                    dcc.Dropdown(
                        placeholder="Chain",
                        id="chain_id",
                        options=[
                            {"label": "Ethereum", "value": 1},
                            {"label": "Binance", "value": 56},
                            {"label": "Matic", "value": 137},
                            {"label": "Avalanche", "value": 43114},
                            {"label": "Fantom", "value": 250}
                        ],
                        value=1,
                        multi=False,
                        className="dropdown"
                    ),
                    dcc.Dropdown(
                        placeholder="Select DEX",
                        id="dex_name",
                        options=[
                            {"label": "SushiSwap", "value": "sushiswap"},
                            {"label": "QuickSwap", "value": "quickswap"},
                            {"label": "Pangolin", "value": "pangolin"},
                            {"label": "SpiritSwap", "value": "spiritswap"},
                            {"label": "SpookySwap", "value": "spookyswap"},
                        ],
                        value="sushiswap",
                        multi=False,
                        className="dropdown"
                    ),
                ],
                brand="DEX Analytics",
                brand_href="#",
                color="primary",
                dark=True,
)


def generate_dropdown_menu(label, items):
    dropdown = dbc.DropdownMenu(
        label=label,
        menu_variant="dark",
        children=items,
    )
    return dropdown


dashboard = html.Div(
    children=[
        generate_header(),
        # top row
        html.Div(
            children=[
                # cards
                html.Div(
                    children=[
                        # kpi card
                        html.Div(
                            children=[
                                html.Div(
                                    # KPIs
                                    children=[
                                        html.Div(
                                            # pais count
                                            children=[
                                                html.Div(children="Active Pairs", className="menu-title"),
                                                html.P(id="active_pairs")
                                            ]
                                        ),
                                        html.Div(
                                            # swaps count
                                            children=[
                                                html.Div(children="Total Swaps", className="menu-title"),
                                                html.P(id="total_swaps")
                                            ],
                                        ),
                                        html.Div(
                                            # fees
                                            children=[
                                                html.Div(children="Total Fees", className="menu-title"),
                                                html.P(id="total_fees")
                                            ],
                                        ),
                                        html.Div(
                                            # quote
                                            children=[
                                                html.Div(children="Gas Price Quote", className="menu-title"),
                                                html.P(id="gas_quote")
                                            ],
                                        ),
                                    ],
                                    className="card-row"
                                ),
                            ],
                            className="half-card",
                        ),
                    ],
                    className="card-row"
                ),
            ],
            className="wrapper"
        ),
        dcc.Loading(
            children=[

            ],
            id="loading",
            type="default"
        ),
        html.Div(
            children=[
                dbc.Button("Show Charts", id="collapse_button", className="mb-3", color="secondary"),
                dbc.Collapse(
                    # graphs card
                    html.Div(
                        children=[
                            dcc.Graph(id="volume_chart_main"),
                            dcc.Graph(id="liquidity_chart_main")
                        ],
                        className="card-row",
                        style={"display": "flex", "height": "600px"}
                    ),
                    id="collapse"
                ),
                dbc.Input(id="token_search", type="text", placeholder="Search Tokens", debounce=True),
                html.Div(
                    children=[
                        dcc.Loading(html.Div(id="pools_data"), id="loading1")
                    ],
                    className="card"
                )
            ],
            className="wrapper"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Loading(html.Div(id="txns_data"), id="loading2")
                    ],
                    className="card"
                )
            ],
            className="wrapper"
        ),
    ]
)
