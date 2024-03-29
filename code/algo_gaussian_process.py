import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as gop
import gpflow
import tensorflow as tf
import pandas as pd

def test_basic():
    pass

def generate_sample_data(x, mode):
    if mode==1:
        return np.sin(x * 3 * 3.14) + 0.3 * np.cos(x * 9 * 3.14) + 0.5 * np.sin(x * 7 * 3.14)
    elif mode==2:
        return 2*x + 6*np.sin(x*3.14)


#------------------------------------------------------------------------------
    
def basic_fit(folder):
    
    K = gpflow.kernels.SquaredExponential(lengthscales = 0.3,
                                          variance     = 1)
    
    X0 = np.linspace(-1.5, 1.5, 1000)[:, None]
    Y0 = generate_sample_data(X0,1)
    
    N = 20
    X = np.random.normal(0,0.7,N)  # X values
    Y = np.array(generate_sample_data(X,1)) #+ np.random.normal(0, 0.2, N)
    
    m = gpflow.models.GPR(data   = (X.reshape(-1,1),Y.reshape(-1,1)),
                          kernel = K,
                          noise_variance = 1)
    opt = gpflow.optimizers.Scipy()
    opt.minimize(m.training_loss, m.trainable_variables, options=dict(maxiter=100))

    Xt = np.arange(-1.5,1.5,0.02).reshape(-1,1)
    #Xt = np.arange(0,50,0.01).reshape(-1,1)
    
    Yt, Yv = m.predict_f(Xt)
    
    plt.plot(X0,Y0, color='blue', linewidth=0.8)
    
    Yt = Yt.numpy().flatten()
    Yv = Yv.numpy().flatten()
    plt.plot(X, Y, 'kx')
    plt.fill_between(Xt.flatten(), Yt-Yv*1.96, Yt+Yv*1.96, 
                    color = 'green', alpha = 0.4)
    
    gpflow.utilities.print_summary(m)
    
    
    set1 = pd.DataFrame(data = {'x':Xt.flatten(),
                                'med': Yt,
                                'varH': Yt-Yv*1.96,
                                'varL': Yt+Yv*1.96})
    
    set2 = pd.DataFrame(data = {'x':X, 'y': Y})
            
    figData = [
           {'type' : 'scatter',
            'x'    : set1['x'],
            'y'    : set1['varL'],
            'line' : {'color' : 'lightgreen'},
            'name' : 'gaussian (low)'},
           {'type' : 'scatter',
            'x'    : set1['x'],
            'y'    : set1['varH'],
            'line' : {'color' : 'lightgreen'},
            'name' : 'gaussian (high)',
            'fill' : 'tonexty'},
           {'type' : 'scatter',
            'x'    : set1['x'],
            'y'    : set1['med'],
            'line' : {'color' : 'blue'},
            'name' : 'gaussian (average)'},
           {'type' : 'scatter',
            'x'    : set2['x'],
            'y'    : set2['y'],
            'line' : {'color' : 'black'},
            'name' : 'sample data',
            'mode' : 'markers'},
           
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
                 'xaxis'     : {'title': 'x', 'range': [-1.5, 1.5]},
                 'yaxis'     : {'title' : 'f(x)', 'range': [-2.5, 2]},
                 'title'     : 'Gaussian process example'
                }
    
    fig = gop.Figure({'data': figData,
                      'layout': figLayout
                      })
    
    fig.write_html(folder + 'figures/algo_gaussianProcess_base.html',
                   include_plotlyjs='cdn',
                   full_html=False,
                   auto_open=True)
    
    
def stepTwo():
    from gpflow.ci_utils import ci_niter
    
    X0 = np.linspace(-1.5, 1.5, 1000)[:, None]
    #X0 = np.linspace(0, 20, 2000)[:, None]
    Y0 = generate_sample_data(X0,1)
    
    N = 1000
    X = np.random.uniform(0,2,N)-1  # X values
    #X = np.random.uniform(0,20,N)  # X values
    Y = np.array(generate_sample_data(X,1)) + 0.2*np.random.normal(0, 1, N)
    X = X.reshape(-1,1)
    Y = Y.reshape(-1,1)
    
    #K = gpflow.kernels.Linear() + gpflow.kernels.Cosine(lengthscales=2)
    K = gpflow.kernels.SquaredExponential()
    m = gpflow.models.SVGP(kernel            = K, 
                           likelihood        = gpflow.likelihoods.Gaussian(), 
                           inducing_variable = X[:50].copy(),#np.random.uniform(0,20,50).reshape(-1,1), 
                           num_data          = N)

    # setup dataset
    train_dataset = tf.data.Dataset.from_tensor_slices((X,Y)).repeat().shuffle(N)
    training_loss = m.training_loss_closure(iter(train_dataset.batch(100)), 
                                            compile = True)
    # setup optimizer
    optimizer     = tf.optimizers.Adam()
    @tf.function
    def optimization_step():
        optimizer.minimize(training_loss, m.trainable_variables)

    # optimize!
    maxIter    = ci_niter(20000)
    logf       = []
    for iStep in range(maxIter):
        optimization_step()
        optimization_step()
        if iStep % 10 == 0:
            elbo = -training_loss().numpy()
            logf.append(elbo)
        
    #plt.figure()
    #plt.plot(logf)
    
    
    # plot stuff
    
    Xt = np.arange(-1.5,1.5,0.01).reshape(-1,1)
    #Xt = np.arange(0,30,0.01).reshape(-1,1)
    Yt, Yv = m.predict_y(Xt)

    plt.plot(X, Y, 'kx', alpha = 0.05)
    plt.plot(X0,Y0, color='blue', linewidth=0.8)
    
    Yt = Yt.numpy().flatten()
    Yv = Yv.numpy().flatten()**0.5
    
    plt.fill_between(Xt.flatten(), Yt-Yv*1.96, Yt+Yv*1.96, 
                     color = 'green', alpha = 0.4)
    
    gpflow.utilities.print_summary(m)