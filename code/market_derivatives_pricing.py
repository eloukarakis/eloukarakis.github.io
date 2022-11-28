import plotly.graph_objects as gop
import numpy as np

def bm(folder):
    """
    Plots overhead circuits rating excursion probability data.
    
    in: folder (str): folder where relevant data are located
    """
    
    figData = [
           {'type' : 'scatter',
            'x'    : np.arange(100),
            'y'    : brownian_motion(n=100),
            'line' : {'color' : 'blue'},
            'name' : 'brownian motion'},
           {'type' : 'scatter',
            'x'    : np.arange(100),
            'y'    : brownian_motion_geometric(n=100),
            'line' : {'color' : 'orangered'},
            'name' : 'geometric brownian motion'},
           
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
                 'xaxis'     : {'title': 't'},
                 'yaxis'     : {'title' : ''},
                 'title'     : 'Sample brownian motion path'
                }
    
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/market_derivativePricing_brownianMotion.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    
def brownian_motion(n, m=0, s=1):
    """
    Generates a sample brownian motion path.
    
    Args:
        n (int): number of samples
        m (float): drift
        s (float): volatility
    """
    
    v = np.random.normal(loc=0, scale=1, size=n)
    v = 100 + np.cumsum(v)

    
    return v


def brownian_motion_geometric(n, m=0, s=0.1):
    """
    Generates a sample geometric brownian motion path.
    
    Args:
        n (int): number of samples
        m (float): drift
        s (float): volatility
    """
    
    v = np.random.normal(loc=0, scale=1, size=n)

    v = np.exp(m - s**2 *0.5 + s * v)
    
    print(v)
    v = 100 * np.cumprod(v)
    print(v)
    
    return v
    
    
    
    