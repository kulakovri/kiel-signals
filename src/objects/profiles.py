import pandas as pd
import matplotlib.pyplot as plt
from src.objects import signals

dist_from_rim = 'Dist from rim'


class CompositionalProfile:

    def __init__(self, profile):
        plt.rcParams.update({'font.size': 26})
        if isinstance(profile, str):
            self.df = pd.read_csv(f'profiles/{profile}')
            self.name = profile
        elif isinstance(profile, signals.Grain):
            self.df = profile.merged_df
            self.name = profile.grain_name
        self.zones = []
        self.bse_profiles = []

    def build_anorthite_profile(self):
        self.build_profile('An', 0, 900)

    def build_profile(self, element_name, min_range, max_range):
        df_to_build = self.df[self.df[dist_from_rim] > min_range]
        df_to_build = df_to_build[df_to_build[dist_from_rim] < max_range]
        df_to_build.plot(x=dist_from_rim, y=element_name, kind='line', figsize=(35, 10))

    def add_zone(self, name, minrange, maxrange):
        new_zone = Zone(name=name, minrange=minrange, maxrange=maxrange, df=self.df)
        self.zones.append(new_zone)

    def get_zone(self, name):
        for zone in self.zones:
            if zone.name == name:
                return zone
        print(f'Zone with requested name {name} is not in {self.name}')

    def build_spiders(self):
        plt.figure(figsize=(35, 10))
        plt.ylabel('Ratio to Core')
        plt.yscale('log')
        inner_core_means = self.get_zone('Inner Core').fetch_means()
        for zone in self.zones:
            df = zone.fetch_means()
            df['ratio'] = df[zone.name] / inner_core_means['Inner Core']
            plt.plot(df.index, df['ratio'], label=zone.name)
        plt.legend()
        plt.show()

    def build_profiles_divided(self, element_name):
        plt.figure(figsize=(35, 10))
        plt.ylabel(element_name)
        for profile_name in self.df['name'].unique():
            profile_df = self.df[self.df['name'] == profile_name]
            plt.plot(profile_df[dist_from_rim], profile_df[element_name], label=profile_name)
        plt.legend()
        plt.show()

    def build_zoned_profile(self, element_name):
        compositions = []
        zone_names = []
        for zone in self.zones:
            compositions.append(zone.fetch_element_compositions(element_name))
            zone_names.append(zone.name)
        compositions_df = pd.concat(compositions, sort=False)
        ax = compositions_df.plot(x=dist_from_rim, y=zone_names, kind='line', figsize=(35, 10))
        ax.set_ylabel(element_name)

    def build_zoned_ratios(self, element_x, elements_y):
        elements_count = len(elements_y)
        columns = round(elements_count / 2)
        fig = plt.figure(figsize=(12 * columns, 20))
        plot_count = 1
        for element_y in elements_y:
            ax1 = fig.add_subplot(2, columns, plot_count)
            for zone in self.zones:
                df = zone.fetch_element_compositions_ratio(element_x, element_y)
                ax1.scatter(df[element_x], df[element_y], label=zone.name)
                ax1.set_ylabel(element_y + ', ppm', fontsize=26)
                ax1.tick_params(axis='both', which='both', labelsize=20)
                ax1.set_yscale('log')
            if plot_count <= columns:
                ax1.set_xticklabels([])
            plot_count = plot_count + 1
        plt.tight_layout()
        plt.xlabel(element_x, fontsize=26)
        plt.legend(fontsize=20)
        plt.show()

    def build_zoned_ratio(self, element_x, element_y):
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(111)
        for zone in self.zones:
            df = zone.fetch_element_compositions_ratio(element_x, element_y)
            ax1.scatter(df[element_x], df[element_y], label=zone.name)
        plt.yscale('log')
        plt.xlabel(element_x)
        plt.ylabel(element_y)
        plt.legend()
        plt.show()

    def build_an_ratios(self):
        self.build_zoned_ratios('An', ('Mg24', 'Li7', 'Mn55', 'Fe57', 'Pb208', 'Ti47'))
        self.build_zoned_ratios('An', ('Ba138', 'Ga71', 'Y89', 'Sr88', 'Ce140', 'K39'))
        self.build_zoned_ratios('An', ('Cu65', 'Si29', 'P31', 'Al27'))

    def add_bse_profile(self, csv_name):
        df_bse = pd.read_csv(f'bse-profiles/{csv_name}')
        df_bse.rename(columns={'An, mol.%': 'An'}, inplace=True)
        df_bse[dist_from_rim] = df_bse['Distance core to rim, mkm'].values[::-1]
        self.bse_profiles.append(df_bse)

    def build_anorthite_profile_with_bse(self):
        fig = plt.figure(figsize=(20, 10))
        ax1 = fig.add_subplot(111)
        ax1.scatter(self.df[dist_from_rim], self.df['An'], label='LA-ICP-MS')
        index = 0
        for bse_profile in self.bse_profiles:
            ax1.scatter(bse_profile[dist_from_rim], bse_profile['An'], label=f'BSE{index}')
            index = index + 1
        plt.xlabel(dist_from_rim)
        plt.ylabel('An')
        plt.legend()
        plt.show()


class Zone:
    def __init__(self, name, minrange, maxrange, df):
        self.df = df
        self.name = name
        zone_df = df[df[dist_from_rim] > minrange]
        self.zone_df = zone_df[zone_df[dist_from_rim] < maxrange]

    def fetch_means(self):
        means = pd.DataFrame(columns=[self.name])
        for column in self.zone_df.columns:
            if column == dist_from_rim or column == 'An' or column == 'Line Number' or 'O' in column:
                continue
            else:
                means.loc[column] = [self.zone_df[column].mean()]
        return means

    def fetch_element_compositions(self, element_name):
        compositions = self.zone_df[[dist_from_rim, element_name]]
        compositions.columns = [dist_from_rim, self.name]
        return compositions

    def fetch_element_compositions_ratio(self, element_x, element_y):
        compositions = self.zone_df[[dist_from_rim, element_x, element_y]]
        return compositions


class Comparator:
    zones = []

    def __init__(self, profiles):
        self.profiles = profiles

    def builld_spiders_by_zone(self, zone_name):
        fig = plt.figure(figsize=(36, 20))
        ax1 = fig.add_subplot(111)
        for profile in self.profiles:
            zone = profile.get_zone(zone_name)
            df = zone.fetch_means()
            ax1.plot(df.index, df[zone.name], label=profile.name)
            ax1.set_yscale('log')
        plt.title(zone_name)
        plt.legend()
        plt.show()

    def build_an_ratios(self, zone_name):
        self.build_ratios_by_zone('An', ('Mg24', 'Li7', 'Mn55', 'Fe57', 'Pb208', 'Ti47'), zone_name)
        self.build_ratios_by_zone('An', ('Ba138', 'Ga71', 'Y89', 'Sr88', 'Ce140', 'K39'), zone_name)
        self.build_ratios_by_zone('An', ('Cu65', 'Si29', 'P31', 'Al27'), zone_name)

    def build_ratios_by_zone(self, element_x, elements_y, zone_name):
        elements_count = len(elements_y)
        columns = round(elements_count / 2)
        fig = plt.figure(figsize=(12 * columns, 20))
        plot_count = 1
        for element_y in elements_y:
            ax1 = fig.add_subplot(2, columns, plot_count)
            for profile in self.profiles:
                zone = profile.get_zone(zone_name)
                df = zone.fetch_element_compositions_ratio(element_x, element_y)
                ax1.scatter(df[element_x], df[element_y], label=profile.name)
                ax1.set_ylabel(element_y + ', ppm', fontsize=26)
                ax1.tick_params(axis='both', which='both', labelsize=20)
                ax1.set_yscale('log')
            if plot_count <= columns:
                ax1.set_xticklabels([])
            plot_count = plot_count + 1
        plt.tight_layout()
        plt.xlabel(element_x, fontsize=26)
        plt.legend(fontsize=20)
        plt.show()
