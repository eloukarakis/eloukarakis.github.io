import pandas as pd
import plotly.graph_objects as gop

def go(folder):
    """
    Plots a typical frequency response figure.
    
    in: folder (str): folder where relevant data are located
    """
    
    data = pd.read_csv(folder + 'code/data/design_typical_frequency_response.csv',
                       index_col=0)
    
    figData = [
           {'type' : 'scatter',
            'x'    : data.index,
            'y'    : data['f'],
            'line' : {'color' : 'blue'},
            'name' : 'excursion probability'}
           ]

    # set hover label length
    for i in range(len(figData)):
      figData[i]['hoverlabel'] = {'namelength' : -1}     
    
    figLayout = {'width'     : 450,
                 'height'    : 300,
                 'font'      : {'size' : 10},
                 'hovermode' : 'x',
                 'margin'    : {'t':26,'b':20,'l':40,'r':0},
                 'showlegend': False,
                 'xaxis'     : {'title': 'time [sec]'},
                 'yaxis'     : {'title' : 'frequency [Hz]'},
                 'title'     : 'Typical frequency response'
                }
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/design_frequencyResponse.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    