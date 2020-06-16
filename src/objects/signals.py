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


class SignalProfile:

    def __init__(self, csv_name):
        self.df = pd.read_csv(
            f'{signals_folder}{csv_name}',
            skiprows=3,
            dtype={time_column_name: 'float64'},
            skipfooter=1
        )
        self.columns = self.df.columns
        self._set_backgorund()
        self._set_type(csv_name)
        self._set_mineral_minus_background()

    def build_csv_profile(self, element_name):
        self.df.plot(y=element_name, kind='line', figsize=(35, 10))

    def _set_backgorund(self):
        element_name = 'Na23'
        df_initial = self.df[self.df[time_column_name] < initial_signal_time]
        initial_signal_mean = df_initial[element_name].mean()
        self.df_analyte = self.df[self.df[element_name] > initial_signal_mean * 3][10:-20]

    def _set_mineral_minus_background(self):
        self.df_mineral_minus_background = pd.DataFrame(columns=self.columns)
        for column in self.columns:
            if column != time_column_name:
                df_initial = self.df[self.df[time_column_name] < initial_signal_time]
                initial_signal_mean = df_initial[column].mean()
                self.df_mineral_minus_background[column] = self.df_analyte[column] - initial_signal_mean

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

    def get_ppm_per_cps(self):
        ppm_per_cps = {}
        if not self.isanalytetype():
            for column in self.columns:
                if column != time_column_name:
                    mean_cps = self.df_mineral_minus_background[column].mean()
                    try:
                        element_concentration = self._get_element_concentration(column)
                        ppm_per_cps[column] = element_concentration / mean_cps
                    except:
                        ppm_per_cps[column] = None

        return ppm_per_cps

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

    def isanalytetype(self):
        return self.type == analyte_type_name


def get_signal_files():
    return os.listdir(signals_folder)
