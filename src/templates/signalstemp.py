from src.objects import signals
import pandas as pd
import re
from src.catalog import sph

file_list = signals.get_signal_files()


def build_grain():
    grn = signals.Grain('18-5h-x2-2-41')
    grn.set_signal_profiles(
        ['2-035-VK18-5h-x2-2-41L34.csv',
         '2-036-VK18-5h-x2-2-41L34a.csv',
         '2-037-VK18-5h-x2-2-41L35.csv',
         '2-038-VK18-5h-x2-2-41L35a.csv'])
    grn.set_standard_profiles(['2-034-SPH.csv', '2-047-SPH.csv'])
    grn.calculate_ppm()


def get_standard_ppm_cps():
    dicts_ppm_cps_ratios = {}
    for file in file_list:
        sign = signals.SignalProfile(file)
        if not sign.is_analyte_type() and not sign.is_unreliable_standard():
            dicts_ppm_cps_ratios[file] = sign.get_ppm_per_cps()
    df = pd.DataFrame(dicts_ppm_cps_ratios)
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.reindex(sorted(df.columns), axis=1).T
    print(df)


def get_standard_ppm_percents():
    dicts_ppm_percent_ratios = {}
    for file in file_list:
        sign = signals.SignalProfile(file)
        if not sign.is_analyte_type() and not sign.is_unreliable_standard():
            dicts_ppm_percent_ratios[file] = sign.get_ppm_per_percent()
    df = pd.DataFrame(dicts_ppm_percent_ratios)
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.reindex(sorted(df.columns), axis=1).T
    print(df)
    df.to_csv('ratios.csv', sep=',')


def calculate_sph_using_nist_and_bcr():
    reference_profiles = [signals.SignalProfile('1-002-N610.csv')]
    calculated_profile = signals.SignalProfile('1-006-SPH.csv')
    df = calculated_profile.calculate_with_standards(reference_profiles)
    for column in df.columns:
        element = re.sub('\d', '', column)
        sph_value = sph.get(element)
        print(f'{column}: {df[column].mean()} | sph value: {sph_value}')