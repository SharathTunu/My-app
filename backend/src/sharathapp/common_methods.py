import pandas as pd

from constants import *
from expenses.constants import *


def weighted_average(v, w):
    try:
        return (v * w).sum() / w.sum()
    except ZeroDivisionError:
        return 0

def summary_numeric_1d(name, minimum, maximum, average, standard_deviation):
    stat_index = ([MINIMUM, AVERAGE, MAXIMUM, STANDARD_DEVIATION])
    d = ([minimum, average, maximum, standard_deviation])
    return pd.Series(d, index=stat_index, name=name)

def dataframe_summary(df, columns=None):
    # this function computes the min, avg, max, std for a pool of loans
    # all the avg and std are weighted except for Current Balance and Original Balance
    # this function should be belong inside the offer class

    summary = pd.DataFrame()
    nums = columns or df._get_numeric_data().columns

    average_columns = [TransactionVerboseNames.AMOUNT]

    for n in nums:
        minimum = df[n].min()
        maximum = df[n].max()
        average = df[n].mean() if n in average_columns else weighted_average(
            df[n], df[TransactionVerboseNames.AMOUNT])
        std = df[n].std()
        summary[n] = summary_numeric_1d(n, minimum, maximum, average, std)

    return summary.T