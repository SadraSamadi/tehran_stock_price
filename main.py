import matplotlib.pyplot as plt
import pandas as pd
from tehran_stocks import db, Stocks, StockPrice
from argparse import ArgumentParser

pd.options.display.max_columns = None
pd.options.display.max_rows = None


def save_prices(search):
    stocks = db.session.query(Stocks) \
        .filter(Stocks.name.like(f'%{search}%')) \
        .filter(Stocks.title.like(f'%{search}%')) \
        .all()
    if not stocks:
        print('No stocks!')
        return
    if len(stocks) == 1:
        stock = stocks[0]
    else:
        print('Multiple results found!')
        for i, s in enumerate(stocks):
            print(f'Result [{i:2}] - {s.name}')
        index = int(input('Enter the number: '))
        stock = stocks[index]
    print('-' * 80)
    fields = [
        'id',
        'name',
        'title',
        'group_name',
        'group_code',
        'instId',
        'insCode',
        'code',
        'sectorPe',
        'shareCount',
        'estimatedEps',
        'baseVol'
    ]
    for field in fields:
        value = getattr(stock, field)
        print(f'{field:16} : {value}')
    print('-' * 80)
    stock.update()
    prices = db.session.query(StockPrice) \
        .filter_by(code=stock.code) \
        .order_by(StockPrice.date.desc()) \
        .limit(300) \
        .all()
    if not prices:
        print('No prices!')
        return
    data = reversed(list(map(lambda p: {
        'Date': p.date,
        'Open': p.open,
        'High': p.high,
        'Low': p.low,
        'Close': p.close,
        'Adj Close': p.close,
        'Volume': p.vol
    }, prices)))
    dataset = pd.DataFrame(data)
    dataset['Date'] = pd.to_datetime(dataset['Date'], format='%Y%m%d')
    dataset.to_csv(f'{stock.name}.csv', index=False)
    print(dataset.tail(10))
    dataset.plot(x='Date', y='Close')
    plt.title(stock.name)
    plt.show()
    print('=' * 80)


def main():
    parser = ArgumentParser()
    parser.add_argument('search')
    args = parser.parse_args()
    save_prices(args.search)


if __name__ == '__main__':
    main()
