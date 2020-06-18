import pandas as pd
from src import catalog
import os
import re

time_column_name = 'Time [Sec]'
initial_signal_time = 10
signals_folder = 'signals/'
sph_type_name = 'SPH'
brc_type_name = 'BCR2'
nist_type_name = 'NIST610'
analyte_type_name = 'analyte'


# mineral - non-background part of the signal profile
# m/z - mass/divided by charge number of the ion
# cps - (counts (clicks) per second) signal measurement value
# percent - is the total percentage of m/z cps out of cps sum
# standard - analyzed reference material, used for calibration and getting ppm/cps.
# NIST610, NIST612, BCR2, SPH are names of standard materials
# analyte - analyzed non-standard

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

    def _set_type(self, csv_name):
        self.name = csv_name
        if 'NIST' in csv_name or '610' in csv_name:
            self.type = 'NIST610'
        elif 'BCR' in csv_name:
            self.type = 'BCR2'
        elif 'SPH' in csv_name:
            self.type = 'SPH'
        else:
            self.type = 'analyte'

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

    def get_ppm_per_cps(self):
        return self._get_ppm_per(self.df_mineral_cps_minus_background)

    def get_ppm_per_percent(self):
        return self._get_ppm_per(self.df_mineral_percentages_minus_background)

    def _get_ppm_per(self, df_minus_background):
        ppm_per = {}
        if not self.isnonstandard():
            for column in self.columns:
                if column != time_column_name:
                    mean_cps = df_minus_background[column].mean()
                    try:
                        element_concentration = self._get_element_concentration(column)
                        ppm_per[column] = element_concentration / mean_cps
                    except:
                        ppm_per[column] = None
        return ppm_per

    def _get_element_concentration(self, column):
        element = re.sub('\d', '', column)
        if self.issphtype():
            return catalog.sph[element]
        elif self.isbcr2type():
            return catalog.bcr_2[element]
        elif self.isnist610type():
            return catalog.nist_610[element]

    def issphtype(self):
        return self.type == sph_type_name

    def isbcr2type(self):
        return self.type == brc_type_name

    def isnist610type(self):
        return self.type == nist_type_name

    def isnonstandard(self):
        return self.type == analyte_type_name

    def isunreliable(self):
        return self.name in catalog.unreliable_standard_profiles

    def build_csv_profile(self, element_name):
        self.df.plot(y=element_name, kind='line', figsize=(35, 10))


def get_signal_files():
    return os.listdir(signals_folder)
