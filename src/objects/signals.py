import pandas as pd
from src import catalog
import os
import re
import matplotlib.pyplot as plt

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
oxygen_molar_weight = 15.9994


class Oxide:

    def __init__(self, name):
        self.formula_parts = name.split('O')
        self._set_oxygen_amount()
        self._set_cation()
        self._set_cation_amount()
        self._set_cation_molar_weight()
        self._set_ppm_weight_ratio()

    def _set_oxygen_amount(self):
        if self.formula_parts[1] == '':
            self.oxygen_amount = 1
        else:
            self.oxygen_amount = int(re.sub('\D', '', self.formula_parts[1]))

    def _set_cation(self):
        self.cation = re.sub(r'[0-9]+', '', self.formula_parts[0])

    def _set_cation_amount(self):
        amount_string = re.sub('\D', '', self.formula_parts[0])
        if amount_string == '':
            self.cation_amount = 1
        else:
            self.cation_amount = int(amount_string)

    def _set_cation_molar_weight(self):
        self.cation_molar_weight = catalog.molar_weights.get(self.cation)

    def _set_ppm_weight_ratio(self):
        oxygen_weight = oxygen_molar_weight * self.oxygen_amount
        formula_weight = self.cation_molar_weight * self.cation_amount + oxygen_weight
        self.ppm_weight_ratio = (formula_weight - oxygen_weight) * 10000 / formula_weight


class Grain:

    def __init__(self, grain_name):
        self.merged_df = pd.DataFrame()
        self.grain_name = grain_name
        self.signal_profiles = []
        self.external_standard_profiles = []

    def set_signal_profiles(self, profile_names):
        for profile_name in profile_names:
            self.signal_profiles.append(SignalProfile(profile_name))
        self._merge()

    def set_external_standard_profiles(self, profile_names):
        for profile_name in profile_names:
            sig = SignalProfile(profile_name)
            self.external_standard_profiles.append(sig)

    def save_csv(self):
        print(self.merged_df)
        self.merged_df.to_csv(f'./out-profiles/{self.grain_name}.csv')

    def save_percents_csv(self):
        df_with_percents = self.merged_df.filter(regex='O')
        print(df_with_percents)
        df_with_percents.to_csv(f'./out-profiles/{self.grain_name}_percents.csv')

    def save_major_elements_csv(self):
        df_major_elements = self.merged_df[['Ca44', 'Na23', 'K39', 'Al27', 'Si29', 'An']]
        print(df_major_elements)
        df_major_elements.to_csv(f'./out-profiles/{self.grain_name}_major.csv')

    def _merge(self):
        signal_profile_dataframes = []
        for signal_profile in self.signal_profiles:
            signal_profile_dataframes.append(signal_profile.df_mineral_cps_minus_background)
        self.merged_df = pd.concat(signal_profile_dataframes, ignore_index=True, sort=False)

    def calculate_weights(self):
        self._calculate_ppm()
        self._calculate_oxide_weight()
        self._calculate_cations()
        self._calculate_anorthite()

    def _calculate_ppm(self):
        reference_means = get_standard_ppm_percents_means(self.external_standard_profiles)
        for key, value in reference_means.items():
            self.merged_df[key] = round(self.merged_df[key] * value, 2)

    def _calculate_oxide_weight(self):
        convertible_elements = catalog.element_oxide_pairs.keys()
        for column in self.merged_df.columns:
            if column in convertible_elements:
                ratio = self._get_oxide_ratio(column)
                self._set_oxide_percent_column(column, ratio)
        self._normalize_oxides()

    def _get_oxide_ratio(self, element):
        oxide_name = catalog.element_oxide_pairs.get(element)
        oxide_ratio = Oxide(oxide_name).ppm_weight_ratio
        return oxide_ratio

    def _set_oxide_percent_column(self, element, ratio):
        oxide_name = catalog.element_oxide_pairs.get(element)
        element_column = self.merged_df[element]
        self.merged_df[oxide_name] = element_column / ratio

    def _normalize_oxides(self):
        oxide_names = catalog.element_oxide_pairs.values()
        df_sums = self._get_oxide_sums()
        for column in self.merged_df.columns:
            if column in oxide_names:
                self.merged_df[column] = round(100 * self.merged_df[column] / df_sums['sum'], 2)

    def _get_oxide_sums(self):
        oxide_names = catalog.element_oxide_pairs.values()
        df_sums = pd.DataFrame()
        df_sums['sum'] = self.merged_df['SiO2'] * 0
        for column in self.merged_df.columns:
            if column in oxide_names:
                df_sums['sum'] = df_sums['sum'] + self.merged_df[column]
        return df_sums

    def _calculate_cations(self):
        for key, value in catalog.сation_constants.items():
            oxide = catalog.element_oxide_pairs_without_number.get(key)
            self.merged_df[key] = self.merged_df[oxide] / value
        self._normalize_cations()

    def _normalize_cations(self):
        df_sums = pd.DataFrame()
        df_sums['sum'] = self.merged_df['SiO2'] * 0
        for key in catalog.сation_constants.keys():
            df_sums['sum'] = df_sums['sum'] + self.merged_df[key]
        for key in catalog.сation_constants.keys():
            self.merged_df[key] = round(5 * self.merged_df[key] / df_sums['sum'], 3)

    def _calculate_anorthite(self):
        self.merged_df['An'] = round(
            100 * self.merged_df['Ca'] / (self.merged_df['Ca'] + self.merged_df['Na'] + self.merged_df['K']), 0)


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
        distance_from_rim = round(self.closest_distance + time_series * ratio, 2)
        if not self.is_from_rim_to_core:
            distance_from_rim = distance_from_rim.values[::-1]
        self.df_mineral['Dist from rim'] = distance_from_rim
        self.df_mineral_percentages_minus_background['Dist from rim'] = distance_from_rim
        self.df_mineral_cps_minus_background['Dist from rim'] = distance_from_rim

    def get_ppm_per_cps(self):
        return self._get_ppm_per(self.df_mineral_cps_minus_background)

    def get_ppm_per_percent(self):
        return self._get_ppm_per(self.df_mineral_percentages_minus_background)

    def build_cps_profile(self, element_name):
        self.df.plot(y=element_name, kind='line', figsize=(35, 10))

    def compare_cps_with_another_profile(self, element_name, another_signal):
        plt.plot(self.df[time_column_name], self.df[element_name], label=self.name)
        plt.plot(another_signal.df[time_column_name], another_signal.df[element_name], label=another_signal.name)
        plt.legend()
        plt.show()

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
                df_ppm_values[column] = self.df_mineral_cps_minus_background[column] * means[column]
        return df_ppm_values


def get_standard_ppm_percents_means(reference_profiles):
    dicts_ppm_percent_ratios = {}
    for profile in reference_profiles:
        dicts_ppm_percent_ratios[profile.name] = profile.get_ppm_per_cps()
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
