import ccxt
import datetime,time
import pandas as pd
import numpy as np
import traceback

class mid_class():
    def __init__(self, public_key, secret_key, symbol, jys_name, do_it_testnet):
        self.symbol = symbol
        if jys_name == 'bitmex':
            self.agent = ccxt.bitmex()
            if do_it_testnet:
                if 'test' in self.agent.urls:
                    self.agent.urls['api'] = self.agent.urls['test']
                else:
                    Log('Can not translate into bitmex testnet')
            self.agent.apiKey = public_key
            self.agent.secret = secret_key

    def make_min_not_num(self, price_N, amount_N):
        #由于bitmex期货市场的小数点位数和币种有关，而不是和现货一样统一，所以这里不能用通行法则。暂定人工手写。
        self.price_N = price_N
        self.amount_N = amount_N

    def get_ohlc_data(self,  timeframe, stm, limit, params):
        self.ohlc_data =  self.agent.fetch_ohlcv( self.symbol, timeframe, stm, limit, params)
        return self.ohlc_data

    def get_position_data(self):
        self.position_data = self.agent.private_get_position( self.symbol )
        self.position_dict = self.position_data[0]
        return self.position_dict

    def get_balance_data (self):
        #Log ( self.agent.fetch_balance() )
        self.balance_data = self.agent.fetch_balance( )
        return self.balance_data

    def get_ticker_data (self):
        self.tiker_data = self.agent.fetch_ticker( self.symbol)
        self.close_tiker_data = self.tiker_data['close']
        return self.close_tiker_data

    def get_orders_data(self):
        self.orders_data = self.agent.fetchOpenOrders( self.symbol, limit = 200)
        return self.orders_data

    def createLimitOrder(self, hand_type, amount, price):
        try:
            return self.agent.createLimitOrder(symbol, hand_type, amount, price)
        except:
            time.sleep(1)
            return self.agent.createLimitOrder(symbol, hand_type, amount, price)

    def creatMarketOrder(self, hand_type, amount):
        try:
            return self.agent.createMarketOrder(symbol, hand_type, amount)
        except:
            time.sleep(1)
            return self.agent.createMarketOrder(symbol, hand_type, amount)

    def cancel_order(self, order_id ):
        try:
            return self.agent.cancelOrder ( order_id )
        except:
            time.sleep(1)
            return self.agent.cancelOrder ( order_id )

    def close_position(self, symbol, price = None):
        if price:
            self.agent.private_post_order_closeposition( {'symbol': symbol,'price':price } )
        else:
            self.agent.private_post_order_closeposition( {'symbol': symbol } )


    def get_wallet_history_data(self):
        self.wallet_history_data =  self.agent.private_get_user_wallethistory()
        return self.wallet_history_data

    def refreash_data(self):
        self.get_position_data()
        time.sleep(0.1)
        self.get_orders_data()
        time.sleep(0.1)
        self.get_balance_data()
        time.sleep(0.1)
        self.get_ticker_data()
        time.sleep(0.1)

    def post_order(self, side, order_type, price, check_price, amount):
        this_symbol = 'XBTUSD' if self.symbol =='BTC/USD' else self.symbol
        params = {
        'symbol': this_symbol,
        'side' : side,
        'ordType': order_type,
        'price' : price,
        'stopPx' : check_price,
        'orderQty' : amount
        }
        rt = bitmex.agent.private_post_order(params)
        return rt
