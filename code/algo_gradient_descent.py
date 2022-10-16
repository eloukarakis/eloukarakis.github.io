import pandas as pd
import plotly.graph_objects as gop
import matplotlib.pyplot as plt


def test():
    """
    Simple test of convergence for basic gradient descent using a quadratic
    function: min{x^2}
    """
    
    base(f = lambda x: x*x,
         df = lambda x: 2*x,
         x0 = 2)
    


def base(f, df, x0):
    """
    Basic gradient descent implementation.
    
    Arguments:
        f (lambda) : function to be minimised
        df (lambda) : first derivative of function to be minimized
        x0 (array) : starting point
        
    Returns:
        -
    """
    
    e = 0.001 # convergence tolerance
    a = 0.9 # step size
    max_iter = 100 # maximum number of iterations
    
    x  = [x0]
    fo = [f(x0)]
    for i in range(max_iter):
        dx = a * df(x[-1])
        x += [x[-1] - dx]
        fo += [f(x[-1])]
        if abs(dx) < e:
            break
        
    plt.plot(x, fo)
    
    
def plot(folder):
    """
    Plots base gradient descend convergence example.
    
    in: folder (str): folder where relevant data are located
    """
    
    figData = [
           {'type' : 'scatter',
            'x'    : [-2,-1.8,-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2,0,
                        0.2,0.4,0.6,0.8,1,1.2,1.4,1.6,1.8,2],
            'y'    : [4,3.24,2.56,1.96,1.44,1,0.64,0.36,0.16,0.04,0,
                      0.04,0.16,0.36,0.64,1,1.44,1.96,2.56,3.24,4],
            'line' : {'color' : 'blue'},
            'name' : 'function'},
           {'type' : 'scatter',
            'x'    : [-1.50,1.20,-0.96,0.77,-0.61,0.49,-0.39,0.31,-0.25,0.20],
            'y'    : [2.250,1.440,0.922,0.590,0.377,0.242,0.155,0.099,0.063,0.041],
            'line' : {'color' : 'orange'},
            'name' : 'solution path'},
           ]

    # set hover label length
    for i in range(len(figData)):
      figData[i]['hoverlabel'] = {'namelength' : -1}     
    
    figLayout = {'width'     : 450,
                 'height'    : 300,
                 'font'      : {'size' : 10},
                 'hovermode' : 'x',
                 'margin'    : {'t':20,'b':20,'l':40,'r':0},
                 'showlegend': True,
                 'xaxis'     : {'title': 'x', 
                                'range': [-2, 2]},
                 'yaxis'     : {'title' : 'f(x)',
                                'range' : [-0.001, 2.4] },
                 'title'     : 'Gradient descent on quadratic function'
                }
    
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/algo_gradientDescent_basic.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    