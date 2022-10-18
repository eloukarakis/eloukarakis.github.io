import pandas as pd
import plotly.graph_objects as gop

def go(folder):
    """
    Plots OHLC data, moving averages and MACD oscillator and signal using
    example data.
    
    in: folder (str): folder where relevant data are located
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
                 'margin'    : {'t':20,'b':20,'l':0,'r':0},
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
    
    fig.write_html(folder + 'figures/technicalAnalysis_movingAverages_example1.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    return data