import plotly.graph_objects as gop
import numpy as np

def go(folder):
    """
    Plots skills against knowledge.
    
    in: folder (str): folder where relevant data are located
    """
    
    skills = {
        "coding - JavaScript": {"best": 5.5},
        "coding - html/css": {"best": 5},
        "coding - Python": {"best": 1},
        
        "cloud - Kubernetes": {"best": 7},
        "cloud - AWS": {"best" : 4}, 
        
        "numerical optimisation": {"best" : 0.5},
        
        "power systems - planning (11-132kV)": {"best" : 1}, 
        "power systems - network design (<=20kV)": {"best" : 2}
        }
    
    
    figData = [
           {'type': 'bar',
            'orientation': 'h',
            'x': [3 for i in skills],
            'y': [i for i  in skills],
            "base": [skills[i]["best"] for i in skills],
            'name': None,
            "hoverinfo":"skip"},
           ]

    # set hover label length
    for i in range(len(figData)):
      figData[i]['hoverlabel'] = {'namelength' : -1}     
    
    figLayout = {'width'     : 450,
                 'height'    : 560,
                 'font'      : {'size' : 10},
                 'hovermode' : 'x',
                 'margin'    : {'t':26,'b':20,'l':40,'r':0},
                 'showlegend': False,
                 'xaxis'     : {'title': "knowledge",
                                'range': [0,10],
                                'tickmode': 'array',
                                'tickvals': [1.5,5,8.5],
                                'ticktext': ["expert", 
                                             "applied",
                                             "basic"]
                                },
                 'yaxis'     : {'title' : 'domain',
                                'type' : 'category'},
                 'title'     : 'Background'
                }
    
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/about_skillset.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    