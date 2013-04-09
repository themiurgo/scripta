import csv
import itertools
import matplotlib
matplotlib.use('PDF')
import numpy as np

from pylab import *

def skip_lines(f_ptr, lines=0):
    for i in xrange(lines):
        f_ptr.readline()

def read_edgelist(f_ptr, delimiter=" ", oneleading=False):
    f_ptr, f_ptr_copy = itertools.tee(f_ptr)
    m, n = get_dims_from_edgelist(f_ptr_copy, oneleading=False)
    arr = zeros((m, n))
    reader = csv.reader(f_ptr, delimiter=" ")
    for row in reader:
        try:
            try:
                val = float64(float(row[2])) # TODO type handling
            except IndexError:
                val = 1 # TODO better method to manage unweighted case
            arr[int(row[0]),int(row[1])] = val
        except IOError: # For example if head was used on stdin
            break
    return arr

def get_dims_from_edgelist(f_ptr, delimiter=" ", oneleading=False):
    reader = csv.reader(f_ptr, delimiter=" ")
    for row in reader:
        values = []
        try:
            v = (int(row[0]), int(row[1]))
            values.append(v)
        except IOError: # For example if head was used on stdin
            break
    m = max(values, key=lambda x: x[0])[0]
    n = max(values, key=lambda x: x[1])[1]
    if not oneleading:
        m += 1
        n += 1
    return m, n

def write_matrix(mat, fname):
    np.savetxt(fname, mat) # FIXME fname to f_ptr

# MATPLOTLIB

def latex_mode():
    rc('text', usetex=True)
    rc('font', family='serif', size=18)
    rc('lines', markersize=10)
    rc('axes', linewidth=1.5)
    rc('xtick.major', size=10)
    rc('xtick.minor', size=5)

def density_plot(fname, pdfname, figtitle="Matrix"):
    clf()
    data = loadtxt(fname)
    title(figtitle)
    #imshow(data, norm=mpl.colors.LogNorm(), cmap=cm.hsv,
    #    interpolation='None')
    imshow(data, norm=mpl.colors.LogNorm(), cmap=cm.hsv,
        interpolation='None')
    colorbar()
    #show()
    savefig(pdfname, format='pdf')

def marginal(timeseries):
    """Calculate marginal probabilities from a timeseries
    
    timeseries -- dict of values
    """
    marginal = {}
    norm_factor = 0
    td = np.true_divide
    for value in timeseries:
        marginal[value] = marginal.get(value, 0) + 1
        norm_factor += 1
    for key, value in marginal.iteritems():
        marginal[key] = td(value, norm_factor)
    return marginal

def conjunct(timeseries1, timeseries2):
    """Calculate conjunct probabilities from two timeseries"""
    conjunct = {}
    norm_factor = 0
    td = np.true_divide
    for v1, v2 in itertools.izip(timeseries1, timeseries2):
        key = (v1, v2)
        conjunct[key] = conjunct.get(key, 0) + 1
        norm_factor += 1
    for key, value in conjunct.iteritems():
        conjunct[key] = td(value, norm_factor)
    return conjunct

def mutual_info(marginal1, marginal2, conjunct):
    mi = 0
    for keys, p in conjunct.iteritems():
        k1, k2 = keys
        if k1 in marginal1 and k2 in marginal2:
            p1 = marginal1[k1]
            p2 = marginal2[k2]
            log_arg = np.true_divide(p, p1*p2)
            mi += p * np.log(log_arg)
    return mi
