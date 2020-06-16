from src.objects import signals
import pandas as pd

file_list = signals.get_signal_files()


def get_standard_ppm_cps():
    dicts_ppm_cps_ratios = {}
    for file in file_list:
        sign = signals.SignalProfile(file)
        if not sign.isanalytetype():
            dicts_ppm_cps_ratios[file] = (sign.get_ppm_per_cps())
    df = pd.DataFrame(dicts_ppm_cps_ratios)
    df = df.reindex(sorted(df.columns), axis=1)
    print(df)
