from typing import Callable


def return_zero_on_zero_division(
    function: Callable[..., float]
) -> Callable[..., float]:
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ZeroDivisionError:
            return 0

    return wrapper


# def sort_df_to_maf_format(df):
#     chr_d = {f"chr{i}": i for i in range(1, 23)}
#     chr_d["chrX"] = 23
#     chr_d["chrY"] = 24
#     chr_d["chrM"] = 25
#     df["chrom_number"] = df["Chromosome"].replace(chr_d)
#     df.sort_values(by=["chrom_number", "Start_Position"], inplace=True)
#     df.drop(columns=["chrom_number"], inplace=True)
#     return df


def return_none_on_zero_division(
    function: Callable[..., float]
) -> Callable[..., float]:
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ZeroDivisionError:
            return None

    return wrapper


# def metric_means(metrics_data: Dict[str, Dict[str, float]]) -> Dict[str, float]:
#     metric_keys = set().union(*(item.keys() for item in metrics_data.values()))
#     result = {key: 0 for key in metric_keys}
#     for item in metrics_data.values():
#         for key in metric_keys:
#             result[key] += item[key]
#     for key in metric_keys:
#         result[key] /= len(metrics_data)
#     return result


@return_zero_on_zero_division
def precision(true_positive: int, false_positive: int) -> float:
    return true_positive / (true_positive + false_positive)


@return_zero_on_zero_division
def recall(true_positive: int, false_negative: int) -> float:
    return true_positive / (true_positive + false_negative)
