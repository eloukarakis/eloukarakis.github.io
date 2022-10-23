import pandas as pd
import plotly.graph_objects as gop


def moving_average(folder):
    
    data = pd.read_csv(folder + 'code/data/algo_timeSeriesAnalysis.csv',
                       index_col = 0,
                       parse_dates = [0],
                       date_parser = lambda t: pd.to_datetime(t, unit='s'))
    
    data['mean'] = data['MID_GBPMWH'].mean()
    data['rolling8'] = data['MID_GBPMWH'].rolling(8).mean()
    data['rolling360'] = data['MID_GBPMWH'].rolling(360).mean()
    
    
    data = data.iloc[-90*48:]
    
    figData = [  
           {'type'  : 'scatter',
            'x'     : data.index,
            'y' : data['MID_GBPMWH'].values,
            'name'  : 'actual'},
           {'type' : 'scatter',
            'x'    : data.index,
            'y'    : data['rolling8'].values,
            'line' : {'color': 'orangered'},
            'name' : 'rolling (8)'},
           {'type' : 'scatter',
            'x'    : data.index,
            'y'    : data['rolling360'].values,
            'line' : {'color': 'olive'},
            'name' : 'rolling (360)'},
           {'type' : 'scatter',
            'x'    : data.index,
            'y'    : data['mean'].values,
            'line' : {'color': 'green'},
            'name' : 'average'},
           
           ]

    for i in range(len(figData)):
      figData[i]['hoverlabel'] = {'namelength' : -1}     
    
    figLayout = {'width'     : 450,
                 'height'    : 300,
                 'font'      : {'size' : 10},
                 'hovermode' : 'x',
                 'margin'    : {'t':26,'b':20,'l':0,'r':0},
                 'showlegend': True,
                 'yaxis'     : {'title'   : 'energy price £/MWh'},
                 'title'     : 'Moving averages example'
                }
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout})
    
    fig.write_html(folder + 'figures/algo_timeSeriesAnalysis_movingAverages.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    