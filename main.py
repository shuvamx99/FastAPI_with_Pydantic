from fastapi import FastAPI,Query
from typing import List, Optional
from trade_model import Trade
from trade_model import TradeDetails
import datetime as dt

app = FastAPI()

# Creating a mock database
trades_db = [
    Trade(
        assetClass="Equity",
        counterparty="XYZ",
        instrumentId="AAPL",
        instrumentName="Apple Stock",
        tradeDateTime=dt.datetime(2022, 1, 1, 10, 0),
        tradeDetails=TradeDetails(buySellIndicator="BUY", price=150.0, quantity=10),
        tradeId="1",
        trader="John"
    ),
    Trade(
        assetClass="Equity",
        counterparty="ABC",
        instrumentId="GOOGL",
        instrumentName="Google Stock",
        tradeDateTime=dt.datetime(2022, 1, 2, 9, 30),
        tradeDetails=TradeDetails(buySellIndicator="SELL", price=2500.0, quantity=5),
        tradeId="2",
        trader="Jane"
    ),
    Trade(
        assetClass="Equity",
        counterparty="XYZ",
        instrumentId="MSFT",
        instrumentName="Microsoft Stock",
        tradeDateTime=dt.datetime(2022, 1, 3, 14, 45),
        tradeDetails=TradeDetails(buySellIndicator="BUY", price=300.0, quantity=8),
        tradeId="3",
        trader="John"
    ),
    Trade(
        assetClass="Bond",
        counterparty="MNO",
        instrumentId="GS",
        instrumentName="Goldman Sachs Stock",
        tradeDateTime=dt.datetime(2022, 12, 29, 14, 45),
        tradeDetails=TradeDetails(buySellIndicator="BUY", price=280.0, quantity=8),
        tradeId="4",
        trader="Jacob"
    ),
        Trade(
        assetClass="Bond",
        counterparty="PQRS",
        instrumentId="JPMC",
        instrumentName="JP Morgan Stock",
        tradeDateTime=dt.datetime(2022, 11, 30, 14, 45),
        tradeDetails=TradeDetails(buySellIndicator="SELL", price=315.0, quantity=10),
        tradeId="4",
        trader="Jacob"
    ),
        Trade(
        assetClass="FX",
        counterparty="XYZ",
        instrumentId="SE",
        instrumentName="Steel Eye Stock",
        tradeDateTime=dt.datetime(2022, 5, 18, 14, 45),
        tradeDetails=TradeDetails(buySellIndicator="BUY", price=500.0, quantity=12),
        tradeId="5",
        trader="Martha"
    )
]

# get all trades
@app.get("/trades",response_model=List[Trade])
def get_trade():
    return trades_db

# get a single trade using id
@app.get("/trades/{trade_id}",response_model=Trade)
def get_trade(trade_id : str):
    for trade in trades_db:
        if trade.trade_id == trade_id:
            return trade
    return {"error" : "Trade id {trade_id} not found"}


# search a trade 
@app.get("/search_trades",response_model=List[Trade])
def search_trades(
    counterparty: Optional[str] = Query(None),
    instrument_id: Optional[str] = Query(None),
    instrument_name: Optional[str] = Query(None),
    trader: Optional[str] = Query(None),
):
    filtered_trades = trades_db
    if counterparty:
        filtered_trades = [trade for trade in filtered_trades if trade.counterparty == counterparty]
    if instrument_id:
        filtered_trades = [trade for trade in filtered_trades if trade.instrument_id == instrument_id]
    if instrument_name:
        filtered_trades = [trade for trade in filtered_trades if trade.instrument_name == instrument_name]
    if trader:
        filtered_trades = [trade for trade in filtered_trades if trade.trader == trader]
    return filtered_trades


# filter trades
@app.get("/filtered_trades", response_model=List[Trade])
def get_trades(
    assetClass: Optional[str] = Query(None),
    start: Optional[dt.datetime] = Query(None),
    end: Optional[dt.datetime] = Query(None),
    minPrice: Optional[float] = Query(None),
    maxPrice: Optional[float] = Query(None),
    tradeType: Optional[str] = Query(None),
):
    filtered_trades = trades_db
    if assetClass:
        filtered_trades = [trade for trade in filtered_trades if trade.asset_class == assetClass]
    if start:
        filtered_trades = [trade for trade in filtered_trades if dt.datetime.fromisoformat(trade.trade_date_time) >= start]
    if end:
        filtered_trades = [trade for trade in filtered_trades if dt.datetime.fromisoformat(trade.trade_date_time) <= end]
    if minPrice:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_details.price  >= minPrice]
    if maxPrice:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_details.price <= maxPrice]
    if tradeType:
        filtered_trades = [trade for trade in filtered_trades if trade.trade_details.buySellIndicator == tradeType]
    return filtered_trades