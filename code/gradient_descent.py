
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
    