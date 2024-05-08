import yfinance as yf
import ccxt
import requests
class Stocks:
    #def __init__(self):

    async def check_stock(self, ctx, tick):
        try:
            ticker = yf.Ticker(f'{tick}')
            data = ticker.history(period='1d')
            current_price = data['Close'].iloc[-1]
            await ctx.reply(f'{tick} Current price: ${round(current_price, 2)}')
        except:
            await ctx.reply(f'Ticker symbol {tick} is invalid or data is not available.')

    #async def company_info(self, ctx, ticker):

class Crypto:
    def __init__(self):
        self.exchange = ccxt.binance()

    async def check_coin(self, ctx, coin):
        pair_two = 'USD'
        pair_one = coin[0]
        if len(coin) > 1:
            pair_two = coin[1]
        symbol=f'{pair_one}-{pair_two}'
        #print(self.exchange.fetch_ohlcv(symbol, timeframe='1d'))
        response = requests.get(f'https://api.coinbase.com/v2/prices/{symbol}/spot')
        data = response.json()
        print(response)
        await ctx.reply(f'{data['data']['base']} is {data['data']['amount']} {data['data']['currency']}')
        print(data)