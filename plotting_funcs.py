import numpy as np
import matplotlib.pyplot as plt

import util

def plot_heatmap(x, axes=None, cmap="YlOrRd", colorbar=True,
                 cbar_size=0.8, cbar_label=None, print_vals=True, 
                 val_fmt=".1e", labels=None, fontsize=6, 
                 grid=True, del_ticks=True, ignore_vals=None,
                 interpolation="nearest", cbar_kwargs=None, **kwargs):
    
    if axes is None:
        axes = plt.gca()
    
    xmod = np.array(x, dtype="float")
    if ignore_vals is not None:
        for igval in ignore_vals:
            xmod[xmod == igval] = np.nan
    
    cm = axes.imshow(xmod, cmap=cmap, interpolation=interpolation, **kwargs)
    if colorbar:
        cb_kwargs = {"shrink": cbar_size, "label": cbar_label}
        if cbar_kwargs:
            cb_kwargs.update(cbar_kwargs)
        axes.get_figure().colorbar(cm, ax=axes, **cb_kwargs)
    
    if print_vals:
        if isinstance(val_fmt, str):
            val_fmt = "{:" + val_fmt + "}"
        
        offset = 0.2 if labels is not None else 0
        for i in range(np.shape(x)[0]):
            for j in range(np.shape(x)[1]):
                txt = val_fmt(x[i, j]) if callable(val_fmt) else val_fmt.format(x[i, j])
                axes.text(j, i + offset, txt, va="center", ha="center", 
                          fontsize=fontsize)
    
    if labels is not None:
        if np.shape(labels) != np.shape(x):
            raise ValueError("Shape of labels don't match shape of x ({} != {})".format(
                np.shape(labels), np.shape(x)))
        
        offset = -0.2 if print_vals else 0
        for i in range(np.shape(labels)[0]):
            for j in range(np.shape(labels)[1]):
                axes.text(j, i + offset, str(labels[i, j]), 
                          va="center", ha="center", fontsize=fontsize)
    
    if grid:
        grid_heatmap(axes)
    
    if del_ticks:
        axes.set_xticks([])
        axes.set_yticks([])
    
    return cm

def grid_heatmap(axes, axis="both", step_size=1, linestyle="-", 
                 color="k", linewidth=0.5, **kwargs):
    allowed_axis_vals = ("both", "x", "y")
    if axis not in allowed_axis_vals:
        raise ValueError("axis must be one of ''".format(allowed_axis_vals))
        
    xmin, xmax = np.sort(axes.get_xlim())
    ymin, ymax = np.sort(axes.get_ylim())
    
    if axis in ("both", "x"):
        for x in np.arange(xmin + step_size, xmax - 0.01, step_size):
            axes.plot([x, x], [ymin, ymax], linestyle=linestyle, 
                      color=color, linewidth=linewidth, **kwargs)
    
    if axis in ("both", "y"):
        for y in np.arange(ymin + step_size, ymax - 0.01, step_size):
            axes.plot([xmin, xmax], [y, y], linestyle=linestyle, 
                      color=color, linewidth=linewidth, **kwargs)
    
    return

def plot_ecdf(x, y, axes=None, **kwargs):
    if axes is None:
        axes = plt.gca()
    
    return axes.step(x, y, where="post", **kwargs)

def combine_legends(axes):
    handles = []
    labels = []
    for ax in axes:
        hand, lab = ax.get_legend_handles_labels()
        handles.extend(hand)
        labels.extend(lab)
    
    return handles, labels
