import pandas as pd
import plotly.graph_objects as gop

def moving_averages(folder):
    """
    Plots OHLC data, moving averages and MACD oscillator and signal using
    example data.
    
    IN: folder (str): folder where relevant data are located
    """
    data = pd.read_parquet(folder + 'code/data/technicals_moving_averages_example1.parquet')
    
    data = data.sort_index()
    data = data.iloc[-300:]
    
    data['ma26'] = data['close'].rolling(28).mean()
    data['ma12'] = data['close'].rolling(12).mean()
    data['macd'] = data['ma12'] - data['ma26']
    data['macds'] = data['macd'].rolling(9).mean()
    data = data.dropna()
    
    figData = [  
           {'type'  : 'candlestick',
            'open'  : data['open'].values,
            'close' : data['close'].values,
            'high'  : data['high'].values,
            'low'   : data['low'].values,
            'name'  : 'OHLC data'},
           {'type' : 'scatter',
            'y'    : data['ma26'].values,
            'line' : {'color': 'blue'},
            'name' : 'MA 26-days'},
           {'type' : 'scatter',
            'y'    : data['ma12'].values,
            'line' : {'color': 'lime'},
            'name' : 'MA 12 days'},
           {'type' : 'bar',
            'y'    : data['macd'].values,
            'marker' : {'color':'black'},
            'name' : 'MACD',
            'yaxis': 'y2'},
           {'type' : 'scatter',
            'y'    : data['macds'],
            'line' : {'color' : 'orangered'},
            'name' : 'MACD signal',
            'yaxis': 'y2'}
           ]

    # set hover label length
    for i in range(len(figData)):
      figData[i]['hoverlabel'] = {'namelength' : -1}     
    
    figLayout = {'width'     : 450,
                 'height'    : 300,
                 'font'      : {'size' : 10},
                 'hovermode' : 'x',
                 'margin'    : {'t':26,'b':20,'l':0,'r':0},
                 'showlegend': True,
                 'xaxis'     : {'rangeslider' : {'visible' : False},
                                'anchor': 'y2'},
                 'yaxis'     : {'domain'  : [0.4, 1],
                                'type'    : 'linear',
                                'title'   : 'price',
                                },
                 'yaxis2'    : {'domain' : [0, 0.36],
                                'title' : 'MACD'},
                 
                 'title'     : 'Moving averages example'
                }
    
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/algo_technicalAnalysis_movingAverages.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    return data


def trends(folder):
    """
    Plots OHLC data and various trend curves examples.
    
    IN: folder (str): folder where relevant data are located
    """
    
    data = pd.read_parquet(folder + 'code/data/technicals_moving_averages_example1.parquet')
    
    data['barStochastic'] = (data['close'] - data['low']) / (data['high'] - data['low'])
    data['barStochastic'] = data['barStochastic'].rolling(90).mean()
    
    figData = [  
           {'type'  : 'candlestick',
            'open'  : data['open'].values,
            'close' : data['close'].values,
            'high'  : data['high'].values,
            'low'   : data['low'].values,
            'name'  : 'OHLC data'},
           {'type' : 'scatter',
            'x' : [663, 771, 892],
            'y' : [2807, 3868, 5150],
            'line' : {'color' : 'black'},
            'name' : 'up-trend'},
           {'type' : 'scatter',
            'x' : [1646, 2308, 2982],
            'y' : [4471, 3593, 2662],
            'line' : {'color' : 'dimgrey'},
            'name' : 'down-trend'},
           {'type' : 'scatter',
            'y'    : data['barStochastic'].values,
            'line' : {'color':'black'},
            'name' : 'bar stochastic avg.',
            'yaxis': 'y2'},
           ]

    # set hover label length
    for i in range(len(figData)):
      figData[i]['hoverlabel'] = {'namelength' : -1}     
    
    figLayout = {'width'     : 450,
                 'height'    : 300,
                 'font'      : {'size' : 10},
                 'hovermode' : 'x',
                 'margin'    : {'t':26,'b':20,'l':0,'r':0},
                 'showlegend': True,
                 'xaxis'     : {'rangeslider' : {'visible' : False},
                                'anchor': 'y2'},
                 'yaxis'     : {'domain'  : [0.4, 1],
                                'type'    : 'linear',
                                'title'   : 'price',
                                },
                 'yaxis2'    : {'domain' : [0, 0.36],
                                'title' : ''},
                 
                 'title'     : 'Trend definitions'
                }
    
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/algo_technicalAnalysis_trends.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    return data


def volumes(folder):
    """
    Plots OHLC data and various trend curves examples.
    
    IN: folder (str): folder where relevant data are located
    """
    
    data = pd.read_parquet(folder + 'code/data/technicals_moving_averages_example1.parquet')
    
    data = data.iloc[-900:]
    data['close-1'] = data['close'].shift(1)
    data['OBV'] = ((data['close'] - data['close-1']).apply(lambda x: 1 if x>0 else -1) * data['volume']).cumsum()
    data['ADL'] = ((2*data['close']-data['low']-data['high'])/(data['high']-data['low']) * data['volume']).cumsum()
    data['volume-avg'] = data['volume'].rolling(90).mean()
    
    figData = [  
           {'type'  : 'candlestick',
            'open'  : data['open'].values,
            'close' : data['close'].values,
            'high'  : data['high'].values,
            'low'   : data['low'].values,
            'name'  : 'OHLC data'},
           {'type' : 'bar',
            'y'    : data['volume'].values,
            'marker' : {'color':'black'},
            'name' : 'volumes',
            'yaxis': 'y3'},
           {'type' : 'scatter',
            'y' : data['volume-avg'].values,
            'line' : {'color' : 'blue'},
            'name' : 'volume MA',
            'yaxis': 'y3'},
           {'type' : 'scatter',
            'y' : data['OBV'],
            'line' : {'color' : 'green'},
            'name' : 'OBV',
            'yaxis': 'y2'},
           {'type' : 'scatter',
            'y'    : data['ADL'].values,
            'line' : {'color':'orange'},
            'name' : 'ADL',
            'yaxis': 'y2'},
           ]

    # set hover label length
    for i in range(len(figData)):
      figData[i]['hoverlabel'] = {'namelength' : -1}     
    
    figLayout = {'width'     : 450,
                 'height'    : 300,
                 'font'      : {'size' : 10},
                 'hovermode' : 'x',
                 'margin'    : {'t':26,'b':20,'l':0,'r':0},
                 'showlegend': True,
                 'xaxis'     : {'rangeslider' : {'visible' : False},
                                'anchor': 'y2'},
                 'yaxis'     : {'domain'  : [0.6, 1],
                                'type'    : 'linear',
                                'title'   : 'price',
                                },
                 'yaxis2'    : {'domain' : [0, 0.27],
                                'title' : ''},
                 'yaxis3'    : {'domain' : [0.30, 0.57]},
                 
                 'title'     : 'Volume indicators'
                }
    
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/algo_technicalAnalysis_volumes.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    return data