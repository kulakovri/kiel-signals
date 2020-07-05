import pandas as pd
from src import catalog
import os
import re

# mineral - non-background part of the signal profile
# m/z - mass/divided by charge number of the ion
# cps - (counts (clicks) per second) signal measurement value
# percent - is the total percentage of m/z cps out of cps sum
# standard - analyzed reference material, used for calibration and getting ppm/cps.
# NIST610, NIST612, BCR2, SPH are names of standard materials
# analyte - analyzed non-standard

dist_from_rim = 'Dist from rim'
time_column_name = 'Time [Sec]'
initial_signal_time = 10
signals_folder = 'signals/'
sph_type_name = 'SPH'
brc_type_name = 'BCR2'
nist_type_name = 'NIST610'
analyte_type_name = 'analyte'
grain_names = catalog.grains
profile_lenghts = catalog.profile_lenghts


class Grain:

    def __init__(self, grain_name):
        self.grain_name = grain_name
        self.signal_profiles = []
        self.standard_profiles = []

    def set_signal_profiles(self, profile_names):
        for profile_name in profile_names:
            self.signal_profiles.append(SignalProfile(profile_name))

    def set_standard_profiles(self, profile_names):
        for profile_name in profile_names:
            self.standard_profiles.append(SignalProfile(profile_name))

    def merge(self):
        signal_profile_dataframes = []
        for signal_profile in self.signal_profiles:
            signal_profile_dataframes.append(signal_profile.df_mineral_percentages_minus_background)
        merged_df = pd.concat(signal_profile_dataframes, ignore_index=True, sort=False)
        print(merged_df)
        merged_df.plot(x=dist_from_rim, y='Ca44', kind='line', figsize=(35, 10))


class SignalProfile:

    def __init__(self, csv_name):
        self.df = pd.read_csv(
            f'{signals_folder}{csv_name}',
            skiprows=3,
            dtype={time_column_name: 'float64'},
            skipfooter=1
        )
        self.columns = self.df.columns
        self._set_type(csv_name)
        self._set_cps_percentages()
        self._set_background()
        self._set_mineral_minus_background()
        if self.is_analyte_type():
            self._set_direction()
            self._set_position()
            self._set_profile_length()
            self._set_overlap_length()
            self._set_profile_closest_distance()
            self._set_distance_from_rim()

    def _set_type(self, csv_name):
        self.name = csv_name
        if 'NIST' in csv_name or '610' in csv_name:
            self.type = nist_type_name
        elif 'BCR' in csv_name:
            self.type = brc_type_name
        elif 'SPH' in csv_name:
            self.type = sph_type_name
        else:
            self.type = analyte_type_name

    def _set_background(self):
        element_name = 'Na23'
        df_initial = self.df[self.df[time_column_name] < initial_signal_time]
        initial_signal_mean = df_initial[element_name].mean()
        self.df_mineral = self.df[self.df[element_name] > initial_signal_mean * 3][10:-20]

    def _set_cps_percentages(self):
        df_values = self.df.drop(time_column_name, 1)
        self.df_percents = pd.concat([
            self.df[time_column_name],
            df_values.div(df_values.sum(1), 'index') * 100
        ], 1)

    def _set_mineral_minus_background(self):
        self.df_mineral_cps_minus_background = pd.DataFrame(columns=self.columns)
        self.df_mineral_percentages_minus_background = pd.DataFrame(columns=self.columns)
        for column in self.columns:
            if column != time_column_name:
                df_initial_cps = self.df[self.df[time_column_name] < initial_signal_time]
                initial_cps_mean = df_initial_cps[column].mean()
                self.df_mineral_cps_minus_background[column] = self.df_mineral[column] - initial_cps_mean
                df_initial_percent = self.df[self.df[time_column_name] < initial_signal_time]
                initial_percent_mean = df_initial_percent[column].mean()
                self.df_mineral_percentages_minus_background[column] = self.df_mineral[column] - initial_percent_mean

    def _set_position(self):
        self.is_continuation = False
        if "a.csv" in self.name:
            self.is_continuation = True

    def _set_direction(self):
        self.is_from_rim_to_core = False
        for rim_to_core_line in catalog.rim_to_core_lines:
            if f'{rim_to_core_line}.csv' in self.name or f'{rim_to_core_line}a.csv' in self.name:
                self.is_from_rim_to_core = True
                break

    def _set_profile_length(self):
        self.profile_length = profile_lenghts.get(self.name)

    def _set_overlap_length(self):
        self.overlap_length = 0
        csv_key = self.name
        if not self.is_continuation:
            csv_key = (self.name.split("-"))[-1].split(".csv")[0]
        for key, value in catalog.profile_overlaps.items():
            if csv_key in key:
                self.overlap_length = value
                break

    def _set_profile_closest_distance(self):
        if self.is_from_rim_to_core:
            if self.is_continuation:
                line_number = (self.name.split("-"))[-1].split("a.csv")[0]
                for key, value in profile_lenghts.items():
                    if line_number in key and key != self.name:
                        self.closest_distance = value - self.overlap_length
            else:
                self.closest_distance = 0
        else:
            if self.is_continuation:
                self.closest_distance = 0
            else:
                line_number = (self.name.split("-"))[-1].split(".csv")[0]
                for key, value in profile_lenghts.items():
                    if line_number in key and key != self.name:
                        self.closest_distance = value - self.overlap_length

    def _set_distance_from_rim(self):
        time_series = self.df_mineral[time_column_name]
        mineral_time = time_series.iloc[-1] - time_series.iloc[0]
        ratio = self.profile_length / mineral_time
        time_series = time_series - time_series.iloc[0]
        distance_from_rim = self.closest_distance + time_series * ratio
        if not self.is_from_rim_to_core:
            distance_from_rim = distance_from_rim.values[::-1]
        self.df_mineral['Dist from rim'] = distance_from_rim
        self.df_mineral_percentages_minus_background['Dist from rim'] = distance_from_rim
        self.df_mineral_cps_minus_background['Dist from rim'] = distance_from_rim

    def get_ppm_per_cps(self):
        return self._get_ppm_per(self.df_mineral_cps_minus_background)

    def get_ppm_per_percent(self):
        return self._get_ppm_per(self.df_mineral_percentages_minus_background)

    def _get_ppm_per(self, df_minus_background):
        ppm_per = {}
        if not self.is_analyte_type():
            for column in self.columns:
                if column != time_column_name:
                    mean_signal = df_minus_background[column].mean()
                    try:
                        element_concentration = self._get_element_concentration(column)
                        ppm_per[column] = element_concentration / mean_signal
                    except:
                        ppm_per[column] = None
        return ppm_per

    def _get_element_concentration(self, column):
        element = re.sub('\d', '', column)
        if self.is_sph_type():
            return catalog.sph[element]
        elif self.is_bcr2_type():
            return catalog.bcr_2[element]
        elif self.is_nist610_type():
            return catalog.nist_610[element]

    def is_sph_type(self):
        return self.type == sph_type_name

    def is_bcr2_type(self):
        return self.type == brc_type_name

    def is_nist610_type(self):
        return self.type == nist_type_name

    def is_analyte_type(self):
        return self.type == analyte_type_name

    def is_unreliable_standard(self):
        return self.name in catalog.unreliable_standard_profiles

    def build_csv_profile(self, element_name):
        self.df.plot(y=element_name, kind='line', figsize=(35, 10))

    def build_percentage_profile(self, element_name):
        self.df_percents.plot(y=element_name, kind='line', figsize=(35, 10))

    def calculate_with_standards(self, reference_profiles):
        means = get_standard_ppm_percents_means(reference_profiles)
        df_ppm_values = pd.DataFrame()
        for column in self.columns:
            if column != time_column_name:
                df_ppm_values[column] = self.df_mineral_percentages_minus_background[column] * means[column]
        return df_ppm_values


def get_standard_ppm_percents_means(reference_profiles):
    dicts_ppm_percent_ratios = {}
    for profile in reference_profiles:
        dicts_ppm_percent_ratios[profile.name] = profile.get_ppm_per_percent()
    means = pd.DataFrame(dicts_ppm_percent_ratios)
    means = means.reindex(sorted(means.columns), axis=1).T
    means = means.mean()
    return means.to_dict()


def get_signal_files():
    return os.listdir(signals_folder)


def _get_signal_profiles():
    signal_profiles = []
    file_list = get_signal_files()
    for file_name in file_list:
        signal_profiles.append(SignalProfile(file_name))
    return signal_profiles
