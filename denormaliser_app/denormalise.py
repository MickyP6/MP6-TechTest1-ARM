import pandas as pd
import matplotlib.pyplot as plt
import random
from typing import List


def default_func(data: List[int], i: int = None) -> List[int]:
    return data


def denormalise(func = None,size = 100, overlap_ratio = 0.5):
    """
    denormalise the data in relation to historic values.
    The google widget data is a scale in relation to a window.
    This function uses overlapping data to denormalise.
    """

    if not func:
        func = default_func
    
    f_x = pd.Series([func(random.randint(0, 100), i) for i in range(size)])

    ser_list = []
    chunksize = 20
    offset = round(chunksize * overlap_ratio)
    i = 0

    while i <= size:
        ser_copy = f_x[i:i+chunksize]
        ser_copy = ser_copy/ser_copy.max()
        ser_list.append(ser_copy)
        i += (chunksize - offset)
    
    df = pd.concat(ser_list, axis=1)
    df.columns = [f"s{i}" for i in range(1, len(ser_list) + 1)]
    dx = df.shift(axis=1)/df
    T = df * dx.max().cumprod()
    g_x = (T*(f_x.max()/T.max().max())).mean(axis=1)

    _, axes = plt.subplots(nrows=2, ncols=2)
    for sub_plot in axes.flatten():
        sub_plot.set_xlim([0,size])
        sub_plot.set_xticks=range(0,size,10)

    f_x.plot(title="raw", ax=axes[0,0])
    df.plot(title="denorm", ax=axes[0,1])
    g_x.plot(title="renorm", ax=axes[1,0])
    (f_x - g_x).plot(title="deviance", ax=axes[1,1])
    plt.show()


if __name__=="__main__":
    denormalise(size=100)