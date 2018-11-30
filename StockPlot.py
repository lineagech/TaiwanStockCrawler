import datetime
import numpy as np
import bisect
import pandas_datareader.data as web

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import gridspec

def get_dates(startdate, enddate):
    dates = [datetime.date(m//12,m%12+1,1) for m in range(startdate.year*12+startdate.month-1, enddate.year*12+enddate.month)]
    return np.array(dates)

def get_xticks_date_index(list_dates, target_dates):
    list_dates = [ datetime.date(target.year, target.month, target.day) for target in list_dates ]
    date_lindex = [ bisect.bisect_left(list_dates, target) for target in target_dates ]
    return date_lindex

def get_xticks_name(list_dates, date_indexes):
    name_lists = []
    for index in date_indexes:
        name_lists.append(list_dates[index].strftime("%b'%y"))
    return np.array(name_lists)

def draw(df, title="", up_color='r', down_color='g'):
    startdate = df.Date[0]
    enddate = df.Date[-1]

    ''' Show prices '''
    def prices_format(x,y):
        try:
            index = int(x+0.5)
            if index < 0 or index >= len(df.Date):
                return ""
            else:
                return "{}, y={:1.1f}, price={:10.2f}".format(df.Date[index], y, df.Close[index])
        except Exception as e:
            print(e.args)
            return ""

    ''' Show volumes '''
    def volumes_format(x,y):
        try:
            index = int(x+0.5)
            if index < 0 or index >= len(df.Date):
                return ""
            else:
                return "{}, y={:1.1f}M, price={:10.2f}M".format(df.Date[index], y*1e-6, df.Volume[index]*1e-6)
        except Exception as e:
            print(e.args)
            return ""

    def tick_format(x, pos):
        return '%1.1fM' % (x * 1e-6)

    if df.empty:
        raise SystemExit


    fig = plt.figure(figsize=(16,12))
    fig.subplots_adjust(bottom=0.1)
    fig.subplots_adjust(hspace=0)

    '''create grid spec, one for prices and the other for volumes'''
    gd = gridspec.GridSpec(2,1,height_ratios=[4,1])

    ax0 = plt.subplot(gd[0,:])
    ax1 = plt.subplot(gd[1,:], sharex=ax0)

    dates_array = get_dates(startdate, enddate)
    xticks_date_indexes = get_xticks_date_index(df.index, dates_array)
    xticks_date_name = get_xticks_name(df.index, xticks_date_indexes) ## str array

    #draw_price_ta(ax0, df)

    '''Set up X-axis ticks and labels'''
    ax0.set_xticks(xticks_date_indexes)
    ax0.set_xticklabels(xticks_date_name)
    ax1.set_xticks(xticks_date_indexes)
    ax1.set_xticklabels(xticks_date_name)
    ax1.tick_params(axis='x',direction='out',length=5)

    '''Set up format coord when cursor points at a specific point'''
    ax0.format_coord = prices_format
    ax1.format_coord = volumes_format

    '''Legend'''
    ax0.legend(loc='upper left', shadow=True, fancybox=True)

    '''Formater'''
    vol_formater = FuncFormatter(tick_format)
    ax1.yaxis.set_major_formatter(vol_formater) # show up vol's format in millions
    ax1.yaxis.tick_right() # move tick to the right
    ax1.set_ylabel('Volume', fontsize=16)
    #ax1.yaxis.set_label_position("right")

    # plt.setp(ax0.get_xticklabels(), visible=False)

    ''''''
    ax0.set_ylabel('Price($)', fontsize=16)
    ax0.set_title(title, fontsize=24, fontweight='bold')
    ax0.grid(True)
    ax1.grid(True)

    yh = df.High.max()
    yl = df.Low.min()
    ax0.set_ylim(yl - (yh - yl) / 20.0, yh + (yh - yl) / 20.0)
    ax0.set_xlim(0, len(df.index) - 1)


    #ax0.autoscale_view()
    #ax1.autoscale_view()

def main():
    startdate = datetime.date(2016,1,1)
    enddate = datetime.date.today()

    df = web.DataReader("AAPL", "yahoo", startdate, enddate)
    draw(df, "AAPL")

if __name__ == '__main__':
    main()