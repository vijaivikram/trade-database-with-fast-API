from fastapi import FastAPI, HTTPException
import datetime as dt
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()


class TradeDetails(BaseModel):
    buySellIndicator: str
    price: float
    quantity: int


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None)
    counterparty: Optional[str] = Field(default=None)
    instrument_id: str = Field(alias="instrumentId")
    instrument_name: str = Field(alias="instrumentName")
    trade_date_time: dt.datetime = Field(alias="tradeDateTime")
    trade_details: TradeDetails = Field(alias="tradeDetails")
    trade_id: str = Field(alias="tradeId", default=None)
    trader: str


trade_ = {
    1: {"buysellindicator": "buy", "price": 100.0, "quantity": 90},
    2: {"buysellindicator": "sell", "price": 200.0, "quantity": 87},
    3: {"buysellindicator": "sell", "price": 398.14, "quantity": 23},
    4: {"buysellindicator": "buy", "price": 45.98, "quantity": 53},
    5: {"buysellindicator": "sell", "price": 98.46, "quantity": 52},
    6: {"buysellindicator": "buy", "price": 354, "quantity": 20},
    7: {"buysellindicator": "sell", "price": 34, "quantity": 67},
    8: {"buysellindicator": "buy", "price": 189, "quantity": 57},
    9: {"buysellindicator": "buy", "price": 78.43, "quantity": 18},
    10: {"buysellindicator": "sell", "price": 300.56, "quantity": 59},
}


Database = {
    1: {
        "asset_class": "equity",
        "counterparty": "buyer",
        "instrument_id": "TSLA",
        "instrument_name": "TESLA",
        "trade_date_time": "2023-06-07 22:36:46.869961",
        "trade_details": trade_[1],
        "trade_id": 1,
        "trader": "Akash",
    },
    2: {
        "asset_class": "equity",
        "counterparty": "seller",
        "instrument_id": "AMZN",
        "instrument_name": "AMAZON",
        "trade_date_time": "2023-06-01 08:31:48.869961",
        "trade_details": trade_[2],
        "trade_id": 2,
        "trader": "Ajay",
    },
    3: {
        "asset_class": "bonds",
        "counterparty": "seller",
        "instrument_id": "AAPL",
        "instrument_name": "APPLE",
        "trade_date_time": "2023-06-03 20:42:14.869961",
        "trade_details": trade_[3],
        "trade_id": 3,
        "trader": "Akash",
    },
    4: {
        "asset_class": "options",
        "counterparty": "buyer",
        "instrument_id": "INFY",
        "instrument_name": "INFOSYS",
        "trade_date_time": "2023-06-04 09:16:26.869961",
        "trade_details": trade_[4],
        "trade_id": 4,
        "trader": "Ranbir",
    },
    5: {
        "asset_class": "commodities",
        "counterparty": "seller",
        "instrument_id": "HINDUNILVR",
        "instrument_name": "HINDUSTAN UNILEVER",
        "trade_date_time": "2023-05-04 12:46:21.869961",
        "trade_details": trade_[5],
        "trade_id": 5,
        "trader": "Ajay",
    },
    6: {
        "asset_class": "equity",
        "counterparty": "buyer",
        "instrument_id": "LTIM",
        "instrument_name": "LTIMMINDTREE",
        "trade_date_time": "2023-06-05 10:14:21.869961",
        "trade_details": trade_[6],
        "trade_id": 6,
        "trader": "Balaji",
    },
    7: {
        "asset_class": "options",
        "counterparty": "buyer",
        "instrument_id": "SBIN",
        "instrument_name": "STATE BANK OF INDIA",
        "trade_date_time": "2023-06-05 12:28:46.869961",
        "trade_details": trade_[7],
        "trade_id": 7,
        "trader": "Akash",
    },
    8: {
        "asset_class": "currency",
        "counterparty": "seller",
        "instrument_id": "LT",
        "instrument_name": "LARSEN & TURBO",
        "trade_date_time": "2023-06-06 11:40:42.869961",
        "trade_details": trade_[8],
        "trade_id": 8,
        "trader": "Vijai",
    },
    9: {
        "asset_class": "bonds",
        "counterparty": "buyer",
        "instrument_id": "LICI",
        "instrument_name": "LIFE INSURANCE CORP OF INDIA",
        "trade_date_time": "2023-06-07 14:47:12.869961",
        "trade_details": trade_[9],
        "trade_id": 9,
        "trader": "Vikram",
    },
    10: {
        "asset_class": "options",
        "counterparty": "seller",
        "instrument_id": "ATGL",
        "instrument_name": "ADANI TOTAL GAS LTD",
        "trade_date_time": "2023-06-07 11:20:37.869961",
        "trade_details": trade_[10],
        "trade_id": 10,
        "trader": "Vijai",
    },
}


@app.get("/")
def index():
    return {"Assignment for API Developer Intern": "By Vijai Vikram I"}


# list all trades
@app.get("/trades")
def list_all_trades():
    return [trade for trade in Database.values()]


# list trades by trade_id
@app.get("/trade/{trade_id}")
def trade_by_id(trade_id: int):
    if trade_id not in Database:
        raise HTTPException(status_code=404, detail="Invalid Trade ID")
    return Database[trade_id]


# search through trades
@app.get("/search")
def by_search(name: str):
    data = {}
    for x in Database:
        if Database[x]["counterparty"] == name:
            data[x] = Database[x]
        if Database[x]["instrument_id"] == name:
            data[x] = Database[x]
        if Database[x]["instrument_name"] == name:
            data[x] = Database[x]
        if Database[x]["trader"] == name:
            data[x] = Database[x]

    return data


# Advanced filtering with asset classes
@app.get("/filter/assetclass")
def by_assetclass(name: str):
    data = {}
    for x in Database:
        if Database[x]["asset_class"] == name:
            data[x] = Database[x]

    return data


# Advanced filtering with price
@app.get("/filter/price")
def price(minprice: float, maxprice: float):
    data = {}
    for x in Database:
        if (
            Database[x]["trade_details"]["price"] >= minprice
            and Database[x]["trade_details"]["price"] <= maxprice
        ):
            data[x] = Database[x]

    return data


# Advanced filtering with dates
@app.get("/filter/dates")
def price(start: dt.datetime, end: dt.datetime):
    data = {}
    for x in Database:
        if (
            Database[x]["trade_date_time"] >= start
            and Database[x]["trade_date_time"] <= end
        ):
            data[x] = Database[x]

    return data


# Advanced filtering with trade type
@app.get("/filter/tradetype")
def tradetype(name: str):
    data = {}
    for x in Database:
        if Database[x]["trade_details"]["buysellindicator"] == name:
            data[x] = Database[x]

    return data


# pagination
@app.get("/paginate/")
def get_trades(limit: int = 5, offset: int = 0):
    end_index = offset + limit
    trades = list(Database.values())[offset:end_index]
    total_pages = len(Database) // limit + (len(Database) % limit != 0)
    previous_url = None
    if offset > 0:
        previous_offset = max(offset - limit, 0)
        previous_url = f"/get-trade/?limit={limit}&offset={previous_offset}"
    next_url = None
    if end_index < len(Database):
        next_offset = end_index
        next_url = f"/get-trade/?limit={limit}&offset={next_offset}"
    result = {
        "trades": trades,
        "pagination": {
            "total_pages": total_pages,
            "previous": previous_url,
            "next": next_url,
        },
    }

    return result
