from src.objects import signals
import pandas as pd
import matplotlib.pyplot as plt

file_list = signals.get_signal_files()


def get_standard_ppm_cps():
    dicts_ppm_cps_ratios = {}
    for file in file_list:
        sign = signals.SignalProfile(file)
        if not sign.is_non_standard() and not sign.is_unreliable_standard():
            dicts_ppm_cps_ratios[file] = sign.get_ppm_per_cps()
    df = pd.DataFrame(dicts_ppm_cps_ratios)
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.reindex(sorted(df.columns), axis=1).T
    print(df)

def get_standard_ppm_percents():
    dicts_ppm_cps_ratios = {}
    for file in file_list:
        sign = signals.SignalProfile(file)
        if not sign.is_non_standard() and not sign.is_unreliable_standard():
            dicts_ppm_cps_ratios[file] = sign.get_ppm_per_percent()
    df = pd.DataFrame(dicts_ppm_cps_ratios)
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.reindex(sorted(df.columns), axis=1).T
    print(df)

