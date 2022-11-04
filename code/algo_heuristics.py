
import pandas as pd
import numpy as np
import multiprocessing as mp
import plotly.graph_objects as gop


def test(folder):
    
    results = grid_search(func = obj_func,
                          params = {'x': [-12, 12, 20],
                                    'y': [-12, 12, 20]
                                })
    
    results2 = random_search(func = obj_func,
                            params = {'x': [-12, 12],
                                      'y': [-12, 12]
                                   })
    
    figData = [
           {'type' : 'contour',
            'x'    : results['x'].unique(),
            'y'    : results['y'].unique(),
            'z'    : results['val'].values.reshape(20, 20),
            'dx'   : 0.1,
            'dy'   : 0.1,
            'colorscale' : 'blues'},
           {'type' : 'scatter',
            'x'    : results['x'],
            'y'    : results['y'],
            'line' : {'color' : 'black'},
            'mode' : 'markers',
            'name' : 'grid search points'},
           {'type' : 'scatter',
            'x'    : results2['x'],
            'y'    : results2['y'],
            'line' : {'color' : 'orangered'},
            'mode' : 'markers',
            'name' : 'grid search points'}
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
                 'xaxis'     : {'title': 'x'},
                 'yaxis'     : {'title' : 'y'},
                 'title'     : 'Grid & random search'
                }
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/algo_gridsearch.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    return results


def obj_func(x):
    
    return min(x['x']**2 + x['y']**2 - 10, 10) \
         + min((x['x']-4)**2 + (x['y']-4)**2, 10) \
         + min((x['x']+7)**2 + (x['y']+7)**2-20, 12) 


def grid_search(func, params):
    """
    Performs parallelised grid search.
    
    in: func (function): objective function
    in: params (dict): set of parameter names including [min, max, number of samples]
    out: results (dataframe): parameters and associated objective function values
    """
    
    # discretise space
    params = {ip : np.linspace(params[ip][0], params[ip][1], params[ip][2])
              for ip in params}
    
    x = np.array(np.meshgrid(*[params[i] for i in params])).transpose()
    x = x.reshape(-1, len(params))
    x = pd.DataFrame(columns = [i for i in params], data = x)
    
    # parallel processing
    pool = mp.Pool(mp.cpu_count())
    results = [pool.apply_async(func, args = (x.loc[i].to_dict(), ))
               for i in x.index]
    
    pool.close()
    pool.join()
    x['val'] = [r.get() for r in results]
    
    return x


def random_search(func, params):
    """
    Performs random search.
    
    in: func (function): objective function
    in: params (dict): set of parameter names including [min, max]
    out: results (dataframe): parameters and associated objective function values
    """
    
    rng = np.random.default_rng()
    rng_fc = 0.95
    rng_pm = {ip: (params[ip][1]-params[ip][0])*0.5 for ip in params}
    xb = {ip: rng.uniform(params[ip][0], params[ip][1])  for ip in params}
    f  = func(xb)
    x  = [xb]

    for i in range(50):
        xc = {ip: rng.uniform(max(params[ip][0], xb[ip]-(rng_pm[ip]*rng_fc)), 
                              min(params[ip][1], xb[ip]+(rng_pm[ip]*rng_fc))) 
              for ip in params}
        fn = func(xc)
        x += [xc]
        if fn < f:
            xb = xc
            rng_fc = max(rng_fc * 0.9, 0.2)        
    
    x = pd.DataFrame(x)
    return x
            