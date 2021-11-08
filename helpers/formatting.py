
def f_link(row, name: str):
    return "[{0}]({0})".format(row[name])


def etherscan_link(row, name: str):
    return f"[{row['Pair']}](https://etherscan.io/address/{row[name]})"


def etherscan_txn_link(row, name: str):
    return f"[{row[name]}](https://etherscan.io/tx/{row[name]})"


def f_img(row, name: str):
    return "![]({0})".format(row[name])


def etherscan_img(row, name: str):
    return f"![](https://etherscan.io/token/images/{row[name]}_32.png)"