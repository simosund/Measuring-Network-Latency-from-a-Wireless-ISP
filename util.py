import ipaddress
import numpy as np
from hilbertcurve.hilbertcurve import HilbertCurve # https://pypi.org/project/hilbertcurve/

def vectorized_dict_lookup(dictionary, keys, default=None, dtype=None):
    unique, idx = np.unique(keys, return_inverse=True)
    if default is None:
        return np.array([dictionary[key] for key in unique], 
                        dtype=dtype)[idx].reshape(np.shape(keys))
    return np.array([dictionary.get(key, default) for key in unique], 
                    dtype=dtype)[idx].reshape(np.shape(keys))

# Generate evenly spaced points for different scales (example at end of notebook)
def linspace_scaled(vmin, vmax, n=1000, scale="linear"):
    supported_scales = ("linear", "log", "logit")
    
    if n < 0:
        raise ValueError("n must be positive (>= 0)")
    if vmin > vmax:
        raise ValueError("ymin must be <= ymax")
    if scale not in supported_scales:
        raise ValueError("scale must be one of: {}".format(supported_scales))
    if vmin <= 0 and scale in ("log", "logit"):
        raise ValueError("vmin must be greater than 0 with scale={}".format(scale))
    if vmax >= 1 and scale == "logit":
        raise ValueError("vmax must be less than 1 with scale=logit")
    
    elif scale == "linear":
        x = np.linspace(vmin, vmax, n)
    elif scale == "log":
        x = np.logspace(np.log10(vmin), np.log10(vmax), n)
    elif scale == "logit":
        x = logit_inv(np.linspace(logit(vmin), logit(vmax), n))
    else:
        raise NotImplementedError("Don't know how to handle scale '{}'".format(scale))
          
    return x

def logit(x, base=10):
    return np.emath.logn(base, x / (1 - x))

def logit_inv(x, base=10):
    return np.power(base, x) / (1 + np.power(base, x))

def ecdf(x, filtnan=True):
    x = np.array(x)
    if filtnan:
        x = x[np.logical_not(np.isnan(x))]
    
    x.sort()
    return np.concatenate(([x[0]], x)), np.linspace(0, 1, len(x)+1)

def quantile_ecdf(x, n=1000, vmin=0, vmax=1, scale_optimized="linear"):
    q = linspace_scaled(vmin, vmax, n=n, scale=scale_optimized)
    return np.nanquantile(x, q), q

def as_hilbert_matrix(seq1d):
    n = len(seq1d)
    
    for level in range(1, 13):
        if n == 2**(level * 2):
            break
        elif n < 2**(level * 2):
            raise ValueError("seq1d has length {} which is not compatible with a Hilbert curve".format(n))
    
    if n > 2**(level * 2):
        raise ValueError("seq1d too long, maximum supported size is {}".format(2**(level * 2)))
    
    as_hilbert = np.reshape(seq1d, (2**level, 2**level)).copy()
    xy = np.array(HilbertCurve(level, 2).points_from_distances(np.arange(n)))
    as_hilbert[xy[:, 1], xy[:, 0]] = seq1d
    
    return as_hilbert

def netify(subnet):
    """
    Ensures subnet is an ipaddress.IPvXNetwork instance
    Small convenience function which allows the code requireing ipaddress
    functionality to work with both string and ipaddress subnets, but
    being much faster than calling ipaddress.ip_network() in case subnet is
    already ipaddress
    """
    if isinstance(subnet, ipaddress.IPv4Network) or isinstance(subnet, ipaddress.IPv6Network):
        return subnet
    else:
        return ipaddress.ip_network(subnet)

def int_ceil(x, multiple):
    rem = x % multiple
    return x + ((rem > 0) * multiple - rem)

def int_floor(x, multiple):
    return x - (x % multiple)

def int_floor(x, multiple):
    return x - (x % multiple)
