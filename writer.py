import bases
import line_shapes
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm.auto import tqdm


# ---------Functions for creating unique binary numbers------
def cycle_list(l, loops=1):
    n = len(l)
    for t in range(loops):
        l = [l[(i + 1) % n] for i in range(n)]
    return (l)


def generate_unique_combinations(L):
    combinations = generate_binary_strings(L)
    non_repeating = [combinations[0]]
    for i in tqdm(range(len(combinations)), desc="Genearting Unique Binary Numbers"):
        ref = list(combinations[i])
        N = len(ref)
        test = 0
        for j in range(len(non_repeating)):
            for n in range(N):

                if cycle_list(list(non_repeating[j]), loops=n + 1) == ref:
                    test += 1

        if test == 0:
            non_repeating.append(combinations[i])

    for i in np.arange(len(non_repeating)):
        non_repeating[i] = [int(s) for s in list(non_repeating[i])]
    return (non_repeating)


def genbin(n, bs=''):
    if n - 1:
        genbin(n - 1, bs + '0')
        genbin(n - 1, bs + '1')
    else:
        pass
        # print('1' + bs)


def generate_binary_strings(bit_count):
    binary_strings = []

    def genbin(n, bs=''):
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            genbin(n, bs + '0')
            genbin(n, bs + '1')

    genbin(bit_count)
    # print(binary_strings)
    return binary_strings


# -------Functions for drawing runes
def decode_shape(fig, ui, in_array, k=1, point_color='k', color='k',
                 label=None, base_fn=bases.polygon, base_kwargs=[],
                 shape_fn=line_shapes.straight, shape_kwargs=[],
                 plot_base=False):
    # decodes a single array into a given base, use plot_base = True if you are plotting it on its own
    n = len(in_array)
    x, y = base_fn(n, *base_kwargs)
    if plot_base == True:
        plt.scatter(x[1:], y[1:], s=3, facecolors='none', edgecolors=point_color)
        plt.scatter(x[0], y[0], s=3, facecolors=point_color, edgecolors=point_color)
        plt.axis('off')
        plt.axis('scaled')
    for i, elem in enumerate(in_array):
        P = [x[i], y[i]]
        Q = [x[(i + k) % n], y[(i + k) % n]]
        # print(shape_kwargs)
        X, Y = shape_fn(P, Q, *shape_kwargs)
        if elem == 0:
            if ui.checkb_guide_line.isChecked():
                plt.plot(X, Y, color=color, ls=ui.cb_guide_line_type.currentText(), linewidth=ui.hs_guide_line_size.value()/10)
        elif elem == 1:
            plt.plot(X, Y, color=color, ls="-",linewidth=ui.hs_spell_line_size.value()/10, label=label if i == np.where(in_array == 1)[0][0] else None)
        else:
            print(f'elem {elem} at index {i} is not valid, input being skipped')


def draw_multiple_inputs(fig,fig2 ,ui, in_array,
                         base_fn=bases.polygon, base_kwargs=[],
                         shape_fn=line_shapes.straight, shape_kwargs=[],
                         point_color='k', labels=[], legend=False, colors=[],
                         legend_loc="best"):
    base_kwargs = [i for i in base_kwargs if i]
    shape_kwargs = [i for i in shape_kwargs if i is False or i != 0.0]
    # draws multiple inputs on a single base
    if colors == []:
        colors = [point_color] * in_array.shape[0]
    n = in_array.shape[1]
    x, y = base_fn(n, *base_kwargs)
    plt.scatter(x[1:], y[1:], s=ui.hs_marker_size.value()*10, facecolors=point_color, edgecolors=point_color)
    plt.scatter(x[0], y[0], s=ui.hs_marker_size.value()*10, facecolors=point_color, edgecolors=point_color)

    if len(labels) != in_array.shape[0]:
        labels = [None] * in_array.shape[0]

    for i, k in enumerate(range(in_array.shape[0])):
        decode_shape(fig, ui, in_array[i], k=k + 1, base_fn=base_fn, base_kwargs=base_kwargs,
                     shape_fn=shape_fn, shape_kwargs=shape_kwargs, label=labels[i], color=colors[i])
    if labels[0] != None and legend == True:
        x,y = ui.hs_h_loc_pos.value()/100 , ui.vs_v_loc_pos.value()/100
        print(x,y)
        fig.legend(loc='outside upper left',bbox_to_anchor=(x,y))

        # fig.legend(loc='outside upper left',bbox_to_anchor=(x, y))
        fig2.legend(loc='outside upper left',fontsize=20,bbox_to_anchor=(x,y))

        # plt.legend(loc=1, bbox_to_anchor=(.99, 0.3), bbox_transform=plt.gcf().transFigure, fontsize=10)
    plt.axis('off')
    plt.axis('scaled')


def load_attribute(fname):
    with open(fname, "r") as f:
        data = f.readlines()
        f.close()
    data = [d.replace("\n", "").lower() for d in data]
    return (data)