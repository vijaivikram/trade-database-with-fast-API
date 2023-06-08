# Trade-database-with-fast-API

## Installation:
Install the following modules to use the FastAPI

`pip install fastapi`

`pip install uvicorn`

`pip install pydantic`

## To run the program:

Enter the following command in terminal

`uvicorn main:app --reload`

The program will start on http://localhost:8000

## Database Schema:

This program uses two Pydantic models - TradeDetails and Trade. 
TradeDetails model contains the details such as the buy/sell indicator, price, and quantity. 
The Trade model contains the details such as asset class, counterparty, instrument ID and name, trade date-time, trade details, trade ID, and trader.

```
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
 ```
 ## Data:
 
 I have entered about 10 trade details into the database. We will query the same using the following endpoints.
 
 ## Endpoints:
 
 ### Homepage:
```
@app.get("/")
def index():
    return {"Assignment for API Developer Intern": "By Vijai Vikram I"}
```

### Listing all trades:
This endpoint `/trades` lists all the trade details in the database
```
@app.get("/trades")
def list_all_trades():
    return [trade for trade in Database.values()]
```

### Output:
```
[{"asset_class":"equity","counterparty":"buyer","instrument_id":"TSLA","instrument_name":"TESLA","trade_date_time":"2023-06-07 22:36:46.869961","trade_details":{"buysellindicator":"buy","price":100.0,"quantity":90},"trade_id":1,"trader":"Akash"},{"asset_class":"equity","counterparty":"seller","instrument_id":"AMZN","instrument_name":"AMAZON","trade_date_time":"2023-06-01 08:31:48.869961","trade_details":{"buysellindicator":"sell","price":200.0,"quantity":87},"trade_id":2,"trader":"Ajay"},{"asset_class":"bonds","counterparty":"seller","instrument_id":"AAPL","instrument_name":"APPLE","trade_date_time":"2023-06-03 20:42:14.869961","trade_details":{"buysellindicator":"sell","price":398.14,"quantity":23},"trade_id":3,"trader":"Akash"},{"asset_class":"options","counterparty":"buyer","instrument_id":"INFY","instrument_name":"INFOSYS","trade_date_time":"2023-06-04 09:16:26.869961","trade_details":{"buysellindicator":"buy","price":45.98,"quantity":53},"trade_id":4,"trader":"Ranbir"},{"asset_class":"commodities","counterparty":"seller","instrument_id":"HINDUNILVR","instrument_name":"HINDUSTAN UNILEVER","trade_date_time":"2023-05-04 12:46:21.869961","trade_details":{"buysellindicator":"sell","price":98.46,"quantity":52},"trade_id":5,"trader":"Ajay"},{"asset_class":"equity","counterparty":"buyer","instrument_id":"LTIM","instrument_name":"LTIMMINDTREE","trade_date_time":"2023-06-05 10:14:21.869961","trade_details":{"buysellindicator":"buy","price":354,"quantity":20},"trade_id":6,"trader":"Balaji"},{"asset_class":"options","counterparty":"buyer","instrument_id":"SBIN","instrument_name":"STATE BANK OF INDIA","trade_date_time":"2023-06-05 12:28:46.869961","trade_details":{"buysellindicator":"sell","price":34,"quantity":67},"trade_id":7,"trader":"Akash"},{"asset_class":"currency","counterparty":"seller","instrument_id":"LT","instrument_name":"LARSEN & TURBO","trade_date_time":"2023-06-06 11:40:42.869961","trade_details":{"buysellindicator":"buy","price":189,"quantity":57},"trade_id":8,"trader":"Vijai"},{"asset_class":"bonds","counterparty":"buyer","instrument_id":"LICI","instrument_name":"LIFE INSURANCE CORP OF INDIA","trade_date_time":"2023-06-07 14:47:12.869961","trade_details":{"buysellindicator":"buy","price":78.43,"quantity":18},"trade_id":9,"trader":"Vikram"},{"asset_class":"options","counterparty":"seller","instrument_id":"ATGL","instrument_name":"ADANI TOTAL GAS LTD","trade_date_time":"2023-06-07 11:20:37.869961","trade_details":{"buysellindicator":"sell","price":300.56,"quantity":59},"trade_id":10,"trader":"Vijai"}]
```

### Listing trades by trade_id:
Using this endpoint, we can list the trades using the trade_id

```
@app.get("/trade/{trade_id}")
def trade_by_id(trade_id: int):
    if trade_id not in Database:
        raise HTTPException(status_code=404, detail="Invalid Trade ID")
    return Database[trade_id]
```

For example, I am trying to get the trade details with trade id 4,
<br />URL : `http://localhost:8000/trade/4`

### Output:
```
{"asset_class":"options","counterparty":"buyer","instrument_id":"INFY","instrument_name":"INFOSYS","trade_date_time":"2023-06-04 09:16:26.869961","trade_details":{"buysellindicator":"buy","price":45.98,"quantity":53},"trade_id":4,"trader":"Ranbir"}
```

### Searching trades:
With this endpoint, we will be able to search across the trades using the API.
We can search through any of the following fields with input at `?name=`

`counterparty`
`instrument_id`
`instrument_name`
`trader`

```
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
 ```
For example, I would like to get the trade details of Akash,
<br />URL : `http://localhost:8000/search?name=Akash`

### Output:
```
{"1":{"asset_class":"equity","counterparty":"buyer","instrument_id":"TSLA","instrument_name":"TESLA","trade_date_time":"2023-06-07 22:36:46.869961","trade_details":{"buysellindicator":"buy","price":100.0,"quantity":90},"trade_id":1,"trader":"Akash"},"3":{"asset_class":"bonds","counterparty":"seller","instrument_id":"AAPL","instrument_name":"APPLE","trade_date_time":"2023-06-03 20:42:14.869961","trade_details":{"buysellindicator":"sell","price":398.14,"quantity":23},"trade_id":3,"trader":"Akash"},"7":{"asset_class":"options","counterparty":"buyer","instrument_id":"SBIN","instrument_name":"STATE BANK OF INDIA","trade_date_time":"2023-06-05 12:28:46.869961","trade_details":{"buysellindicator":"sell","price":34,"quantity":67},"trade_id":7,"trader":"Akash"}}
```

### Advanced filtering with the asset classes
With this endpoint,we can also filter the trade details using the asset classes.

```
@app.get("/filter/assetclass")
def by_assetclass(name: str):
    data = {}
    for x in Database:
        if Database[x]["asset_class"] == name:
            data[x] = Database[x]

    return data
 ```
 For example, if we want to get the trade details using the asset class of `bonds`,
 <br />URL : `http://localhost:8000/filter/assetclass?name=bonds`
 
 ### Output:
```
 {"3":{"asset_class":"bonds","counterparty":"seller","instrument_id":"AAPL","instrument_name":"APPLE","trade_date_time":"2023-06-03 20:42:14.869961","trade_details":{"buysellindicator":"sell","price":398.14,"quantity":23},"trade_id":3,"trader":"Akash"},"9":{"asset_class":"bonds","counterparty":"buyer","instrument_id":"LICI","instrument_name":"LIFE INSURANCE CORP OF INDIA","trade_date_time":"2023-06-07 14:47:12.869961","trade_details":{"buysellindicator":"buy","price":78.43,"quantity":18},"trade_id":9,"trader":"Vikram"}}
```

### Advanced filtering with price:
With this endpoint,we can also filter the trade details using the price of the trade

```
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
```

For example, if I want the trade details of all the trades with the price minimum of 50 and maximum of 300,
<br />URL : `http://localhost:8000/filter/price?minprice=50.00&maxprice=300.00`

### Output
All the trade details with the price between 50 and 300 will be listed

```
{"1":{"asset_class":"equity","counterparty":"buyer","instrument_id":"TSLA","instrument_name":"TESLA","trade_date_time":"2023-06-07 22:36:46.869961","trade_details":{"buysellindicator":"buy","price":100.0,"quantity":90},"trade_id":1,"trader":"Akash"},"2":{"asset_class":"equity","counterparty":"seller","instrument_id":"AMZN","instrument_name":"AMAZON","trade_date_time":"2023-06-01 08:31:48.869961","trade_details":{"buysellindicator":"sell","price":200.0,"quantity":87},"trade_id":2,"trader":"Ajay"},"5":{"asset_class":"commodities","counterparty":"seller","instrument_id":"HINDUNILVR","instrument_name":"HINDUSTAN UNILEVER","trade_date_time":"2023-05-04 12:46:21.869961","trade_details":{"buysellindicator":"sell","price":98.46,"quantity":52},"trade_id":5,"trader":"Ajay"},"8":{"asset_class":"currency","counterparty":"seller","instrument_id":"LT","instrument_name":"LARSEN & TURBO","trade_date_time":"2023-06-06 11:40:42.869961","trade_details":{"buysellindicator":"buy","price":189,"quantity":57},"trade_id":8,"trader":"Vijai"},"9":{"asset_class":"bonds","counterparty":"buyer","instrument_id":"LICI","instrument_name":"LIFE INSURANCE CORP OF INDIA","trade_date_time":"2023-06-07 14:47:12.869961","trade_details":{"buysellindicator":"buy","price":78.43,"quantity":18},"trade_id":9,"trader":"Vikram"}}
```

### Advanced filtering with trade type
With this endpooint, we can also filter the trade details using tradetype

```
@app.get("/filter/tradetype")
def tradetype(name: str):
    data = {}
    for x in Database:
        if Database[x]["trade_details"]["buysellindicator"] == name:
            data[x] = Database[x]

    return data
 ```
 
 For example, if I want the trade details of all the trades with the trade type of `buy`,
 <br />URL : `http://localhost:8000/filter/tradetype?name=buy`
 
 ### Output:
 
 All the trade details with the trade type of `buy` will be listed
 
 ```
 {"1":{"asset_class":"equity","counterparty":"buyer","instrument_id":"TSLA","instrument_name":"TESLA","trade_date_time":"2023-06-07 22:36:46.869961","trade_details":{"buysellindicator":"buy","price":100.0,"quantity":90},"trade_id":1,"trader":"Akash"},"4":{"asset_class":"options","counterparty":"buyer","instrument_id":"INFY","instrument_name":"INFOSYS","trade_date_time":"2023-06-04 09:16:26.869961","trade_details":{"buysellindicator":"buy","price":45.98,"quantity":53},"trade_id":4,"trader":"Ranbir"},"6":{"asset_class":"equity","counterparty":"buyer","instrument_id":"LTIM","instrument_name":"LTIMMINDTREE","trade_date_time":"2023-06-05 10:14:21.869961","trade_details":{"buysellindicator":"buy","price":354,"quantity":20},"trade_id":6,"trader":"Balaji"},"8":{"asset_class":"currency","counterparty":"seller","instrument_id":"LT","instrument_name":"LARSEN & TURBO","trade_date_time":"2023-06-06 11:40:42.869961","trade_details":{"buysellindicator":"buy","price":189,"quantity":57},"trade_id":8,"trader":"Vijai"},"9":{"asset_class":"bonds","counterparty":"buyer","instrument_id":"LICI","instrument_name":"LIFE INSURANCE CORP OF INDIA","trade_date_time":"2023-06-07 14:47:12.869961","trade_details":{"buysellindicator":"buy","price":78.43,"quantity":18},"trade_id":9,"trader":"Vikram"}}
```

## Listing all trades with Pagination:
 This endpoint lists all trade details with pagination. The default number of trades per page is set to 5
 
 ```
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
 ```

To paginate, URL : `http://localhost:8000/paginate/`
 
