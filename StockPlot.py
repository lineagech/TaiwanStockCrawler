import datetime
import numpy as np
import bisect
import pandas_datareader.data as web

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import gridspec
from matplotlib import collections
from matplotlib.colors import colorConverter

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

def draw_values(ax, opens, highs, lows, closes, width=4, up_color='r', down_color='g', alpha=0.75):
    '''K-bars'''
    delta = width / 2.
    barVerts = [((i - delta, open),
                 (i - delta, close),
                 (i + delta, close),
                 (i + delta, open))
                for i, open, close in zip(range(len(opens)), opens, closes)]

    downSegments = [((i, low), (i, min(open, close)))
                    for i, low, high, open, close in zip(range(len(lows)), lows, highs, opens, closes)]

    upSegments = [((i, max(open, close)), (i, high))
                  for i, low, high, open, close in zip(range(len(lows)), lows, highs, opens, closes)]
    segments = downSegments + upSegments

    r, g, b = colorConverter.to_rgb(up_color)
    up_color = r, g, b, alpha
    r, g, b = colorConverter.to_rgb(down_color)
    down_color = r, g, b, alpha

    color_dict = {True: up_color, False: down_color,}
    colors = [color_dict[open < close] for open, close in zip(opens, closes)]

    line_collections = collections.LineCollection( segments,
                                                   linewidths=(0.5,),
                                                   colors=((0,0,0,1),),
                                                   antialiaseds=(0,)
                                                 )
    bar_collections = collections.PolyCollection( barVerts,
                                      facecolors=colors,
                                      edgecolors=((0, 0, 0, 1),),
                                      antialiaseds=(0,),
                                      linewidths=(0.5,),
                                    )
    min_x, max_x = 0, len(opens)
    min_y = min([low for low in lows])
    max_y = max([high for high in highs])

    corners = (min_x, min_y), (max_x, max_y)
    ax.update_datalim(corners)
    ax.autoscale_view()

    ax.add_collection(line_collections)
    ax.add_collection(bar_collections)

    return line_collections, bar_collections

def volume_overlay(ax, opens, closes, volumes, colorup='g', colordown='r', width=4, alpha=1.0):
    """Add a volume overlay to the current axes.  The opens and closes
    are used to determine the color of the bar.  -1 is missing.  If a
    value is missing on one it must be missing on all
    Parameters
    ----------
    ax : `Axes`
        an Axes instance to plot to
    opens : sequence
        a sequence of opens
    closes : sequence
        a sequence of closes
    volumes : sequence
        a sequence of volumes
    width : int
        the bar width in points
    colorup : color
        the color of the lines where close >= open
    colordown : color
        the color of the lines where close <  open
    alpha : float
        bar transparency
    Returns
    -------
    ret : `barCollection`
        The `barrCollection` added to the axes
    """

    colorup = colorConverter.to_rgba(colorup, alpha)
    colordown = colorConverter.to_rgba(colordown, alpha)
    colord = {True: colorup, False: colordown}
    colors = [colord[open < close]
              for open, close in zip(opens, closes)
              if open != -1 and close != -1]

    delta = width / 2.
    bars = [((i - delta, 0), (i - delta, v), (i + delta, v), (i + delta, 0))
            for i, v in enumerate(volumes)
            if v != -1]

    barCollection = collections.PolyCollection(bars,
                                   facecolors=colors,
                                   edgecolors=((0, 0, 0, 1), ),
                                   antialiaseds=(0,),
                                   linewidths=(0.5,),
                                   )

    ax.add_collection(barCollection)
    corners = (0, 0), (len(bars), max(volumes))
    ax.update_datalim(corners)
    ax.autoscale_view()

    # add these last
    return barCollection

def draw(df, title="", up_color='r', down_color='g'):
    startdate = datetime.date(df.index[0].year, df.index[0].month, df.index[0].day)
    enddate = datetime.date(df.index[-1].year, df.index[-1].month, df.index[-1].day)

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
                return "{}, y={:1.1f}M, price={:10.2f}M".format(df.index[index], y*1e-6, df.Volume[index]*1e-6)
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

    draw_values(ax0, df.Open, df.High, df.Low, df.Close, width=1)
    volume_overlay(ax1, df.Open, df.Close, df.Volume, colorup='g', colordown='r', width=4, alpha=1.0)

    dates_array = get_dates(startdate, enddate)
    xticks_date_indexes = get_xticks_date_index(df.index, dates_array)
    xticks_date_name = get_xticks_name(df.index, xticks_date_indexes) ## str array

    #draw_price_ta(ax0, df)

    '''Set up X-axis ticks and labels'''
    ax0.set_xticks(xticks_date_indexes)
    ax0.set_xticklabels(xticks_date_name)
    ax1.set_xticks(xticks_date_indexes)
    ax1.set_xticklabels(xticks_date_name)
    ax1.tick_params(axis='x',direction='out',length=5,labelsize=8)

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

    plt.show()

def main():
    startdate = datetime.date(2016,1,1)
    enddate = datetime.date.today()

    df = web.DataReader("AAPL", "yahoo", startdate, enddate)
    draw(df, "AAPL")

if __name__ == '__main__':
    main()