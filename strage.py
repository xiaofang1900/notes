import tushare as ts
import pandas as pd
import datetime
import numpy as np
import talib as ta
stocks = ['000002', '000063', '000069', '000333', '000338', '000402', '000651', '000671', '000898', '000983', '002081',
          '002142', '002146', '002385', '002601', '600018', '600019', '600028', '600029', '600036', '600048', '600068',
          '600115', '600153', '600188', '600297', '600332', '600340', '600352', '600383', '600390', '600585', '600606',
          '600688', '600690', '600704', '600705', '600871', '600919', '600926', '601006', '601009', '601111', '601117',
          '601155', '601166', '601225', '601229', '601318', '601668', '601877', '601997']
#stocks = ['000002', '000063','000069']
g_end_day=datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)
start_day = g_end_day - datetime.timedelta(120)
str_start = start_day.strftime("%Y-%m-%d")
str_end = g_end_day.strftime("%Y-%m-%d")

keys = ['code','dist_60','cross_60','ma_linear']
datas = pd.DataFrame(columns=keys)
for s in stocks:
    #s = '600332'
    stock_data = ts.get_k_data(s, start=str_start,end=str_end, ktype='D')
    if stock_data['close'].values.size < 61:
        continue
    item = {}
    item['code'] = s;
    stock_data['ma_60'] = pd.rolling_mean(stock_data['close'], 60)
    item['dist_60'] = abs((stock_data['close'].values[-1] - stock_data['ma_60'].values[-1])/stock_data['close'].values[-1])
    persent = abs((stock_data['close'].values[-1] - stock_data['ma_60'].values[-1])/stock_data['close'].values[-1])
    #print "per: " + str(persent)
    if stock_data['close'].values[-2] < stock_data['ma_60'].values[-2] and stock_data['close'].values[-1] >= stock_data['ma_60'].values[-1]:
        item['cross_60'] = 0
    else:
        item['cross_60'] = 1
    #print stock_data['ma_60'][-5:]
    real = ta.LINEARREG_SLOPE(stock_data['ma_60'][-5:].values, timeperiod=3)
    item['ma_linear'] = abs(real[-1])
    datas = datas.append(pd.DataFrame([item]))

print datas
result = pd.DataFrame(np.zeros(datas['code'].values.size),index=datas['code'].values)
result.columns=['rank']
print result
for rule in ['dist_60','cross_60','ma_linear']:
    data = datas[['code',rule]]
    data.set_index('code',inplace=True)
    #print data
    rankdata =  data.rank(method="average",  pct=True)
    rankdata.columns=['rank']
    print rankdata
    result += rankdata
sort_stocks = result.sort_values('rank').index.tolist()
print sort_stocks
#print datas
    #print real[-1]
    #if( stock_data['close'][-2] < stock_data['ma_60'][-2] and stock_data['close'][-1] > stock_data['ma_60'][-1]):
    #    print s

