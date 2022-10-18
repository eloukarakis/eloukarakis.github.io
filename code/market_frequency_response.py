import plotly.graph_objects as gop
import numpy as np

def go(folder):
    """
    Plots standardised droop requirements for frequency response services.
    
    in: folder (str): folder where relevant data are located
    """
    
    frequency = np.arange(49.45, 50.55 + 0.01, 0.005)
    
    def FFR(f):
        if   50.5 > f > 50.015: return + (f - 50.015) / (50.5 - 50.015)
        elif 49.5 < f < 49.985: return - (f - 49.985) / (49.5 - 49.985)
        elif f >= 50.5 : return + 1
        elif f <= 49.5: return - 1
        else: return 0
        
    def DC(f):
        if f >= 50.5:   return   1
        elif f <= 49.5: return - 1
        elif f<= 49.8 : return - 1 + 0.95 / 0.3 *(f - 49.5)
        elif f >= 50.2 : return   0.05 + 0.95 / 0.3 * (f - 50.2)
        elif f < 49.985: return - 0.05 / 0.185 * (49.985 - f)
        elif f > 50.015: return   0.05 / 0.185 * (f - 50.015)
        else: return 0
        
    def DM(f):
        if f >= 50.2:   return   1
        elif f <= 49.8: return - 1
        elif f<= 49.9 : return - 1 + 0.95 / 0.1 *(f - 49.8)
        elif f >= 50.1 : return   0.05 + 0.95 / 0.1 * (f - 50.1)
        elif f < 49.985: return - 0.05 / 0.085 * (49.985 - f)
        elif f > 50.015: return   0.05 / 0.085 * (f - 50.015)
        else: return 0
        
    def DR(f):
        if f >= 50.2:   return   1
        elif f <= 49.8: return - 1
        elif f < 49.985: return - 1 / 0.185 * (49.985 - f)
        elif f > 50.015: return   1 / 0.185 * (f - 50.015)
        else: return 0
        
    def FCAS(f):
        if   50.5 > f > 50.15: return + (f - 50.15) / (50.5 - 50.15)
        elif 49.5 < f < 49.85: return - (f - 49.85) / (49.5 - 49.85)
        elif f >= 50.5 : return + 1
        elif f <= 49.5: return - 1
        else: return 0
    
    figData = [
           {'type' : 'scatter',
            'x'    : frequency,
            'y'    : [-FFR(f)*100 for f in frequency],
            'line' : {'color' : 'orangered'},
            'name' : 'FFR'},
           {'type' : 'scatter',
            'x'    : frequency,
            'y'    : [-DC(f)*100 for f in frequency],
            'line' : {'color' : 'blue'},
            'name' : 'DC'},
           {'type' : 'scatter',
            'x'    : frequency,
            'y'    : [-DM(f)*100 for f in frequency],
            'line' : {'color' : 'green'},
            'name' : 'DM'},
           {'type' : 'scatter',
            'x'    : frequency,
            'y'    : [-DR(f)*100 for f in frequency],
            'line' : {'color' : 'yellow'},
            'name' : 'DR'},
           ]

    # set hover label length
    for i in range(len(figData)):
      figData[i]['hoverlabel'] = {'namelength' : -1}     
    
    figLayout = {'width'     : 450,
                 'height'    : 300,
                 'font'      : {'size' : 10},
                 'hovermode' : 'x',
                 'margin'    : {'t':26,'b':20,'l':40,'r':0},
                 'showlegend': True,
                 'xaxis'     : {'title': 'frequency'},
                 'yaxis'     : {'title' : 'power [%]'},
                 'title'     : 'Standard frequency response droop curves - UK'
                }
    
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/market_frequencyResponse_ukDroop.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    
    figData = [
           {'type' : 'scatter',
            'x'    : frequency,
            'y'    : [-FCAS(f)*100 for f in frequency],
            'line' : {'color' : 'orangered'},
            'name' : 'FCAS'},
           ]

    # set hover label length
    for i in range(len(figData)):
      figData[i]['hoverlabel'] = {'namelength' : -1}     
    
    figLayout = {'width'     : 450,
                 'height'    : 300,
                 'font'      : {'size' : 10},
                 'hovermode' : 'x',
                 'margin'    : {'t':26,'b':20,'l':40,'r':0},
                 'showlegend': True,
                 'xaxis'     : {'title': 'frequency'},
                 'yaxis'     : {'title' : 'power [%]'},
                 'title'     : 'Standard frequency response droop curve - AU'
                }
    
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/market_frequencyResponse_auDroop.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)