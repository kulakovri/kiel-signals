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
# cps - (counts (clicks) per second) signal measurement value
# standard - analyzed reference material, used for calibration and getting ppm/cps. NIST, BCR2, SPH are standard names
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

    def _set_cps_percentages(self):
        df_values = self.df.drop(time_column_name, 1)
        self.df_analyte_percents = pd.concat([
            self.df[time_column_name],
            df_values.div(df_values.sum(1), 'index') * 100
        ], 1)

    def _set_background(self):
        element_name = 'Na23'
        df_initial = self.df[self.df[time_column_name] < initial_signal_time]
        initial_signal_mean = df_initial[element_name].mean()
        self.df_mineral = self.df[self.df[element_name] > initial_signal_mean * 3][10:-20]

    def _set_mineral_minus_background(self):
        self.df_mineral_cps_minus_background = pd.DataFrame(columns=self.columns)
        self.df_mineral_percantages_minus_background = pd.DataFrame(columns=self.columns)
        for column in self.columns:
            if column != time_column_name:
                df_initial = self.df[self.df[time_column_name] < initial_signal_time]
                initial_signal_mean = df_initial[column].mean()
                self.df_mineral_cps_minus_background[column] = self.df_mineral[column] - initial_signal_mean

    def get_ppm_per_cps(self):
        ppm_per_cps = {}
        if not self.isnonstandard():
            for column in self.columns:
                if column != time_column_name:
                    mean_cps = self.df_mineral_cps_minus_background[column].mean()
                    try:
                        element_concentration = self._get_element_concentration(column)
                        ppm_per_cps[column] = element_concentration / mean_cps
                    except:
                        ppm_per_cps[column] = None

        return ppm_per_cps

    def get_ppm_per_percents(self):
        ppm_per_percent = {}
        if not self.isnonstandard():
            for column in self.columns:
                if column != time_column_name:
                    mean_cps = self.df_mineral_cps_minus_background[column].mean()
                    try:
                        element_concentration = self._get_element_concentration(column)
                        ppm_per_percent[column] = element_concentration / mean_cps
                    except:
                        ppm_per_percent[column] = None

        return ppm_per_percent

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
