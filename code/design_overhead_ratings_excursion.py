import plotly.graph_objects as gop

def go(folder):
    """
    Plots overhead circuits rating excursion probability data.
    
    in: folder (str): folder where relevant data are located
    """
    
    figData = [
           {'type' : 'scatter',
            'x'    : [0, 0.9, 0.912, 0.93, 0.98, 1, 1.018, 1.03, 1.063, 1.085,
                      1.135, 1.17, 1.245, 1.315, 1.382, 1.475, 1.64, 1.86, 1000],
            'y'    : [0.00001, 0.00001, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.7, 1,
                      2, 3, 6, 10, 14, 20, 30, 40, 40],
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
                 'margin'    : {'t':20,'b':20,'l':40,'r':0},
                 'showlegend': False,
                 'xaxis'     : {'title': 'Ct', 
                                'range': [0.6, 2]},
                 'yaxis'     : {'title' : 'excursion probability [%]',
                                'range' : [0, 38] },
                 'title'     : 'Rating excursion probability'
                }
    
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/design_circuitRating_excursionProbability.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    