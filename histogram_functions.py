import numpy as np

### Merge histograms ###
# Assumes histograms use consistent bins

def add_to_histogram(dst, src):
    if len(dst) < len(src):
        raise ValueError("dst histogram smaller than src histogram")

    for i in range(len(src)):
        dst[i] += src[i]

    return dst

def sum_histograms(hists):
    if len(hists) == 0:
        return []

    n = max(len(hist) for hist in hists)

    tot = [0] * n
    for hist in hists:
        add_to_histogram(tot, hist)

    return tot


### Calculate statistics from histograms ###
# Should give results consistent with running the corresponding
# normal functions (ex np.quantile instead of bincount_quantile)
# on bincount_to_values(bins, counts), but without having
# to actually explode the histograms into individual values

def get_bin_widths(bins):
    return np.diff(bins)

def get_bin_centers(bins):
    bins = np.array(bins)
    return bins[:-1] + get_bin_widths(bins) / 2

def bincount_to_values(bins, counts):
    return np.repeat(get_bin_centers(bins), counts)

def bincount_sample(bins, counts, n=10000, uniform_noise=True):
    if bincount_isempty(bins, counts):
        return np.full(n, np.nan)
    
    widths = get_bin_widths(bins)
    mids = get_bin_centers(bins)
    
    x = np.random.choice(mids, p=np.divide(counts, sum(counts)), size=n)
    if uniform_noise:
        noise = np.random.uniform(-0.5, 0.5, n)
        x += noise * widths[np.digitize(x, bins) - 1]
    
    return x

def bincount_count(bins, counts):
    """ bins argument is ignored, just to be consistent with other methods """
    return np.sum(counts)

def bincount_isempty(bins, counts):
    return bincount_count(bins, counts) == 0

def bincount_min(bins, counts):
    if bincount_isempty(bins, counts):
        return np.nan

    i = 0
    while counts[i] == 0:
        i += 1

    return get_bin_centers(bins)[i]

def bincount_max(bins, counts):
    if bincount_isempty(bins, counts):
        return np.nan

    i = len(counts) - 1
    while counts[i] == 0:
        i -= 1

    return get_bin_centers(bins)[i]

def bincount_mean(bins, counts):
    if bincount_isempty(bins, counts):
        return np.nan
    return np.average(get_bin_centers(bins), weights=counts)

def bincount_var(bins, counts, ddof=1, shepard_corr=False):
    n = bincount_count(bins, counts)
    if n <= ddof:
        return np.nan

    ex = bincount_mean(bins, counts)
    x = get_bin_centers(bins)
    var = np.multiply(counts, (x - ex)**2).sum() / (n - ddof)
    if shepard_corr:
        widths = get_bin_widths(bins)
        if not all(np.isclose(widths, widths[0])):
            raise ValueError("Can only apply Sheppard's correction if bin-widths are equal")

        var -= widths[0]**2 / 12

    return var

def bincount_std(bins, counts, ddof=1, shepard_corr=False):
    return np.sqrt(bincount_var(bins, counts, ddof=ddof, shepard_corr=shepard_corr))

def bincount_median(bins, counts):
    return bincount_quantile(bins, counts, 0.5)

def bincount_iqr(bins, counts):
    return (bincount_quantile(bins, counts, 0.75) - 
            bincount_quantile(bins, counts, 0.25))

def bincount_quantile(bins, counts, q):
    if not 0 <= q <= 1:
        raise ValueError("q must be in range [0, 1]")
    
    n = bincount_count(bins, counts)
    if n == 0:
        return np.nan

    center_vals = get_bin_centers(bins)

    virt_idx = q * (n - 1)
    if virt_idx <= 0:
        return bincount_min(bins, counts)
    elif virt_idx >= n - 1:
        return bincount_max(bins, counts)

    # find bin virtual index is in
    right_edge = np.cumsum(counts)
    i = np.searchsorted(right_edge, virt_idx, side="left")
    val = center_vals[i]

    # quantile in-between current bin and next (non-empty) bin
    # interpolate
    if virt_idx > right_edge[i] - 1:
        next_i = np.searchsorted(right_edge - 1, virt_idx, side="left")
        val += ((virt_idx) - (right_edge[i] - 1)) * (center_vals[next_i] - center_vals[i])

    return val

def bincount_ecdf(bins, counts):
    x = get_bin_centers(bins)
    y = np.cumsum(counts) / np.sum(counts)
    return np.concatenate(([x[0]], x)), np.concatenate(([0], y))
