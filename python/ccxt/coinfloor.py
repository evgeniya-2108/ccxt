# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import base64
from ccxt.base.errors import NotSupported


class coinfloor (Exchange):

    def describe(self):
        return self.deep_extend(super(coinfloor, self).describe(), {
            'id': 'coinfloor',
            'name': 'coinfloor',
            'rateLimit': 1000,
            'countries': ['UK'],
            'has': {
                'CORS': False,
                'fetchOpenOrders': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/28246081-623fc164-6a1c-11e7-913f-bac0d5576c90.jpg',
                'api': 'https://webapi.coinfloor.co.uk/bist',
                'www': 'https://www.coinfloor.co.uk',
                'doc': [
                    'https://github.com/coinfloor/api',
                    'https://www.coinfloor.co.uk/api',
                ],
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
                'password': True,
                'uid': True,
            },
            'api': {
                'public': {
                    'get': [
                        '{id}/ticker/',
                        '{id}/order_book/',
                        '{id}/transactions/',
                    ],
                },
                'private': {
                    'post': [
                        '{id}/balance/',
                        '{id}/user_transactions/',
                        '{id}/open_orders/',
                        '{symbol}/cancel_order/',
                        '{id}/buy/',
                        '{id}/sell/',
                        '{id}/buy_market/',
                        '{id}/sell_market/',
                        '{id}/estimate_sell_market/',
                        '{id}/estimate_buy_market/',
                    ],
                },
            },
            'markets': {
                'BTC/GBP': {'id': 'XBT/GBP', 'symbol': 'BTC/GBP', 'base': 'BTC', 'quote': 'GBP', 'baseId': 'XBT', 'quoteId': 'GBP'},
                'BTC/EUR': {'id': 'XBT/EUR', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR', 'baseId': 'XBT', 'quoteId': 'EUR'},
                'BCH/GBP': {'id': 'BCH/GBP', 'symbol': 'BCH/GBP', 'base': 'BCH', 'quote': 'GBP', 'baseId': 'BCH', 'quoteId': 'GBP'},
                'ETH/GBP': {'id': 'ETH/GBP', 'symbol': 'ETH/GBP', 'base': 'ETH', 'quote': 'GBP', 'baseId': 'ETH', 'quoteId': 'GBP'},
            },
        })

    def fetch_balance(self, params={}):
        self.load_markets()
        market = None
        if 'symbol' in params:
            market = self.find_market(params['symbol'])
        if 'id' in params:
            market = self.find_market(params['id'])
        if not market:
            raise NotSupported(self.id + ' fetchBalance requires a symbol param')
        request = {
            'id': market['id'],
        }
        response = self.privatePostIdBalance(self.extend(request, params))
        result = {
            'info': response,
        }
        # base/quote used for keys e.g. "xbt_reserved"
        keys = market['id'].lower().split('/')
        result[market['base']] = {
            'free': self.safe_float(response, keys[0] + '_available'),
            'used': self.safe_float(response, keys[0] + '_reserved'),
            'total': self.safe_float(response, keys[0] + '_balance'),
        }
        result[market['quote']] = {
            'free': self.safe_float(response, keys[1] + '_available'),
            'used': self.safe_float(response, keys[1] + '_reserved'),
            'total': self.safe_float(response, keys[1] + '_balance'),
        }
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'id': self.market_id(symbol),
        }
        response = self.publicGetIdOrderBook(self.extend(request, params))
        return self.parse_order_book(response)

    def parse_ticker(self, ticker, market=None):
        # rewrite to get the timestamp from HTTP headers
        timestamp = self.milliseconds()
        symbol = None
        if market is not None:
            symbol = market['symbol']
        vwap = self.safe_float(ticker, 'vwap')
        baseVolume = self.safe_float(ticker, 'volume')
        quoteVolume = None
        if vwap is not None:
            quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': vwap,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = self.publicGetIdTicker(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'date')
        id = self.safe_string(trade, 'tid')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'id': id,
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
            'side': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = self.publicGetIdTransactions(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_ledger(self, code=None, since=None, limit=None, params={}):
        # code is actually a market symbol in self situation, not a currency code
        self.load_markets()
        market = None
        if code:
            market = self.find_market(code)
            if not market:
                raise NotSupported(self.id + ' fetchTransactions requires a code argument(a market symbol)')
        request = {
            'id': market['id'],
            'limit': limit,
        }
        response = self.privatePostIdUserTransactions(self.extend(request, params))
        return self.parse_ledger(response, None, since, None)

    def parse_ledger_entry_status(self, status):
        types = {
            'completed': 'ok',
        }
        return self.safe_string(types, status, status)

    def parse_ledger_entry_type(self, type):
        types = {
            '0': 'transaction',  # deposit
            '1': 'transaction',  # withdrawal
            '2': 'trade',
        }
        return self.safe_string(types, type, type)

    def parse_ledger_entry(self, item, currency=None):
        #
        # trade
        #
        #     {
        #         "datetime": "2017-07-25 06:41:24",
        #         "id": 1500964884381265,
        #         "type": 2,
        #         "xbt": "0.1000",
        #         "xbt_eur": "2322.00",
        #         "eur": "-232.20",
        #         "fee": "0.00",
        #         "order_id": 84696745
        #     }
        #
        # transaction(withdrawal)
        #
        #     {
        #         "datetime": "2017-07-25 13:19:46",
        #         "id": 97669,
        #         "type": 1,
        #         "xbt": "-3.0000",
        #         "xbt_eur": null,
        #         "eur": "0",
        #         "fee": "0.0000",
        #         "order_id": null
        #     }
        #
        # transaction(deposit)
        #
        #     {
        #         "datetime": "2017-07-27 16:44:55",
        #         "id": 98277,
        #         "type": 0,
        #         "xbt": "0",
        #         "xbt_eur": null,
        #         "eur": "4970.04",
        #         "fee": "0.00",
        #         "order_id": null
        #     }
        #
        keys = list(item.keys())
        baseId = None
        quoteId = None
        baseAmount = None
        quoteAmount = None
        for i in range(0, len(keys)):
            key = keys[i]
            if key.find('_') > 0:
                parts = key.split('_')
                numParts = len(parts)
                if numParts == 2:
                    tmpBaseAmount = self.safe_float(item, parts[0])
                    tmpQuoteAmount = self.safe_float(item, parts[1])
                    if tmpBaseAmount is not None and tmpQuoteAmount is not None:
                        baseId = parts[0]
                        quoteId = parts[1]
                        baseAmount = tmpBaseAmount
                        quoteAmount = tmpQuoteAmount
        base = self.safe_currency_code(baseId)
        quote = self.safe_currency_code(quoteId)
        type = self.parse_ledger_entry_type(self.safe_string(item, 'type'))
        referenceId = self.safe_string(item, 'id')
        timestamp = self.parse8601(self.safe_string(item, 'datetime'))
        fee = None
        feeCost = self.safe_float(item, 'fee')
        result = {
            'id': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'amount': None,
            'direction': None,
            'currency': None,
            'type': type,
            'referenceId': referenceId,
            'referenceAccount': None,
            'before': None,
            'after': None,
            'status': 'ok',
            'fee': fee,
            'info': item,
        }
        if type == 'trade':
            #
            # it's a trade so let's make multiple entries, we have several options:
            #
            # if fee is always in quote currency(the exchange uses self)
            # https://github.com/coinfloor/API/blob/master/IMPL-GUIDE.md#how-fees-affect-trade-quantities
            #
            if feeCost is not None:
                fee = {
                    'cost': feeCost,
                    'currency': quote,
                }
            return [
                self.extend(result, {'currency': base, 'amount': abs(baseAmount), 'direction': baseAmount > 'in' if 0 else 'out'}),
                self.extend(result, {'currency': quote, 'amount': abs(quoteAmount), 'direction': quoteAmount > 'in' if 0 else 'out', 'fee': fee}),
            ]
            #
            # if fee is base or quote depending on buy/sell side
            #
            #     baseFee = (baseAmount > 0) ? {'currency': base, 'cost': feeCost} : None
            #     quoteFee = (quoteAmount > 0) ? {'currency': quote, 'cost': feeCost} : None
            #     return [
            #         self.extend(result, {'currency': base, 'amount': baseAmount, 'direction': baseAmount > 'in' if 0 else 'out', 'fee': baseFee}),
            #         self.extend(result, {'currency': quote, 'amount': quoteAmount, 'direction': quoteAmount > 'in' if 0 else 'out', 'fee': quoteFee}),
            #     ]
            #
            # fee as the 3rd item
            #
            #     return [
            #         self.extend(result, {'currency': base, 'amount': baseAmount, 'direction': baseAmount > 'in' if 0 else 'out'}),
            #         self.extend(result, {'currency': quote, 'amount': quoteAmount, 'direction': quoteAmount > 'in' if 0 else 'out'}),
            #         self.extend(result, {'currency': feeCurrency, 'amount': feeCost, 'direction': 'out', 'type': 'fee'}),
            #     ]
            #
        else:
            #
            # it's a regular transaction(deposit or withdrawal)
            #
            amount = baseAmount == quoteAmount if 0 else baseAmount
            code = baseAmount == quote if 0 else base
            direction = 'in' if (amount > 0) else 'out'
            if feeCost is not None:
                fee = {
                    'cost': feeCost,
                    'currency': code,
                }
            return self.extend(result, {
                'currency': code,
                'amount': abs(amount),
                'direction': direction,
                'fee': fee,
            })

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'id': self.market_id(symbol),
        }
        method = 'privatePostId' + self.capitalize(side)
        if type == 'market':
            request['quantity'] = amount
            method += 'Market'
        else:
            request['price'] = price
            request['amount'] = amount
        return getattr(self, method)(self.extend(request, params))

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise NotSupported(self.id + ' cancelOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'id': id,
        }
        return self.privatePostSymbolCancelOrder(request)

    def parse_order(self, order, market=None):
        timestamp = self.parse8601(self.safe_string(order, 'datetime'))
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        side = None
        status = self.safe_string(order, 'status')
        if order['type'] == 0:
            side = 'buy'
        elif order['type'] == 1:
            side = 'sell'
        symbol = None
        if market is not None:
            symbol = market['symbol']
        id = self.safe_string(order, 'id')
        return {
            'info': order,
            'id': id,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': None,
            'status': status,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'amount': amount,
            'filled': None,
            'remaining': None,
            'cost': cost,
            'fee': None,
        }

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise NotSupported(self.id + ' fetchOpenOrders requires a symbol param')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': market['id'],
        }
        response = self.privatePostIdOpenOrders(self.extend(request, params))
        #   {
        #     "amount": "1.0000",
        #     "datetime": "2019-07-12 13:28:16",
        #     "id": 233123443,
        #     "price": "1000.00",
        #     "type": 0
        #   }
        return self.parse_orders(response, market, since, limit, {'status': 'open'})

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        # curl -k -u '[User ID]/[API key]:[Passphrase]' https://webapi.coinfloor.co.uk:8090/bist/XBT/GBP/balance/
        url = self.urls['api'] + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.urlencode(self.extend({'nonce': nonce}, query))
            auth = self.uid + '/' + self.apiKey + ':' + self.password
            signature = self.decode(base64.b64encode(self.encode(auth)))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
