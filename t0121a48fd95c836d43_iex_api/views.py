import requests
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from t0121a48fd95c836d43_iex_api import TrendFollowing
from t0121a48fd95c836d43_iex_api import models
from numpy import average


__author__ = 'Andrew Kuchev (kuchevad@gmail.com)'

PERSISTENT_DATA = {}


def load_stock_data(ticker):
    url = 'https://api.iextrading.com/1.0/stock/{}/chart/1y'.format(ticker)
    r = requests.get(url)
    return r.json()


def index(request):
    return render(request, 'index.html')


@require_http_methods("POST")
def add_algo(request):
    name = request.POST.get("algo-name").strip().lower()
    if not name:
        raise Exception("you should specify name")
    signal = request.POST.get("signal")
    trade = request.POST.get("trade")
    ticker = request.POST.get("ticker").strip().lower()
    if not ticker:
        raise Exception("you should specify ticker")

    data = load_stock_data(ticker)
    if not data:
        raise Exception("unable to load data for ticker " + ticker)

    prices = [x['close'] for x in data]
    positions, PnL = TrendFollowing.algo_result(signal, trade, prices)
    results = list(zip(data, positions, PnL))
    average_pnl = average(PnL)

    algo, created = models.Algo.objects.get_or_create(name=name,
                                                      defaults={'signal': signal, 'trade': trade, 'ticker': ticker,
                                                                'average_pnl': average_pnl})
    algo.signal = signal
    algo.trade = trade
    algo.ticker = ticker
    algo.average_pnl = average_pnl
    algo.save()

    PERSISTENT_DATA[algo.name] = results

    return render(request, 'index.html', {'algo': algo})


def algo_table(request):
    algo_list = list(models.Algo.objects.all())
    return render(request, 'algo-table.html', {'algos': algo_list})


def algo(request, algo_name):
    algo = models.Algo.objects.filter(name=algo_name).first()
    if not algo:
        return render(request, 'algo.html', {'algo': algo})

    if algo.name not in PERSISTENT_DATA:
        data = load_stock_data(algo.ticker)
        if not data:
            raise Exception("unable to load data for ticker " + algo.ticker)

        prices = [x['close'] for x in data]
        positions, PnL = TrendFollowing.algo_result(algo.signal, algo.trade, prices)
        results = list(zip(data, positions, PnL))
        PERSISTENT_DATA[algo.name] = results

    results = PERSISTENT_DATA[algo.name]
    date_series = [x[0]['date'] for x in results]
    close_series = [x[0]['close'] for x in results]
    position_series = [x[1] for x in results]
    pnl_series = [x[2] for x in results]
    return render(request, 'algo.html', {'algo': algo,
                                         'date_series': date_series,
                                         'close_series': close_series,
                                         'position_series': position_series,
                                         'pnl_series': pnl_series, })
