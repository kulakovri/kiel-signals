import pandas as pd
import matplotlib.pyplot as plt


class CompositionalProfile:

    def __init__(self, csv_name):
        plt.rcParams.update({'font.size': 26})
        self.df = pd.read_csv(f'profiles/{csv_name}')
        self.zones = []
        self.name = csv_name

    def build_anorthite_profile(self):
        self.build_profile('An', 0, 900)

    def build_profile(self, element_name, min_range, max_range):
        df_to_build = self.df[self.df['Dist from rim'] > min_range]
        df_to_build = df_to_build[df_to_build['Dist from rim'] < max_range]
        df_to_build.plot(x='Dist from rim', y=element_name, kind='line', figsize=(35, 10))

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

    def build_zoned_profile(self, element_name):
        compositions = []
        zone_names = []
        for zone in self.zones:
            compositions.append(zone.fetch_element_compositions(element_name))
            zone_names.append(zone.name)
        compositions_df = pd.concat(compositions, sort=False)
        ax = compositions_df.plot(x='Dist from rim', y=zone_names, kind='line', figsize=(35, 10))
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


class Zone:
    def __init__(self, name, minrange, maxrange, df):
        self.df = df
        self.name = name
        zone_df = df[df['Dist from rim'] > minrange]
        self.zone_df = zone_df[zone_df['Dist from rim'] < maxrange]

    def fetch_means(self):
        means = pd.DataFrame(columns=[self.name])
        for column in self.zone_df.columns:
            if column == 'Dist from rim' or column == 'An' or column == 'Line Number' or 'O' in column:
                continue
            else:
                means.loc[column] = [self.zone_df[column].mean()]
        return means

    def fetch_element_compositions(self, element_name):
        compositions = self.zone_df[['Dist from rim', element_name]]
        compositions.columns = ['Dist from rim', self.name]
        return compositions

    def fetch_element_compositions_ratio(self, element_x, element_y):
        compositions = self.zone_df[['Dist from rim', element_x, element_y]]
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
