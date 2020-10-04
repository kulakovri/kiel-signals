from src.objects import profiles
from src.objects import signals


def build_grain():
    grn = signals.Grain('18-5h-x2-2-41')
    grn.set_signal_profiles(
        ['2-035-VK18-5h-x2-2-41L34.csv',
         '2-036-VK18-5h-x2-2-41L34a.csv',
         '2-037-VK18-5h-x2-2-41L35.csv',
         '2-038-VK18-5h-x2-2-41L35a.csv'])
    grn.set_external_standard_profiles(['2-048-SPH.csv'])
    grn.set_internal_standard_profiles(['2-051-NIST.csv', '2-020-NIST610.csv'])
    grn.calculate_weights()
    grn.save_csv()
    return grn


def build_profiles_divided(element_name):
    grn = build_grain()
    prf = profiles.CompositionalProfile(grn)
    prf.build_profiles_divided(element_name)


def compare_grain_with_bse():
    grn = build_grain()
    prf = profiles.CompositionalProfile(grn)
    prf.add_bse_profile('18-5h-x2-2-41(1).csv')
    prf.add_bse_profile('18-5h-x2-2-41(2).csv')
    prf.build_anorthite_profile_with_bse()


def compare_profile_with_bse():
    prf = profiles.CompositionalProfile('18-5h-x2-2-41.csv')
    prf.add_bse_profile('18-5h-x2-2-41(1).csv')
    prf.add_bse_profile('18-5h-x2-2-41(2).csv')
    prf.build_anorthite_profile_with_bse()


def fetch_zoned_plagioclase(csv_name):
    if csv_name == '18-5h-x2-2-41.csv':
        prf = profiles.CompositionalProfile(csv_name)
        prf.add_zone('Rim', 0, 105)
        prf.add_zone('Oscillation', 105, 380)
        prf.add_zone('Core', 380, 580)
        prf.add_zone('Inner Core', 580, 700)
        return prf
    if csv_name == '18-5h-x3-1-54.csv':
        prf = profiles.CompositionalProfile('18-5h-x3-1-54.csv')
        prf.add_zone('Rim', 0, 110)
        prf.add_zone('Oscillation', 110, 390)
        prf.add_zone('Core', 390, 520)
        prf.add_zone('Inner Core', 520, 700)
        return prf
    if csv_name == '18-5h-x2-1-25.csv':
        prf = profiles.CompositionalProfile('18-5h-x2-1-25.csv')
        prf.add_zone('Rim', 0, 80)
        prf.add_zone('Oscillation', 80, 220)
        prf.add_zone('Resorbed Core', 220, 340)
        prf.add_zone('Core', 340, 500)
        prf.add_zone('Inner Core', 500, 740)
        return prf
    if csv_name == '18-5h-x3-1-12.csv':
        prf = profiles.CompositionalProfile('18-5h-x3-1-12.csv')
        prf.add_zone('Rim', 0, 80)
        prf.add_zone('Oscillation', 80, 220)
        prf.add_zone('Resorbed Core', 220, 340)
        prf.add_zone('Core', 340, 500)
        prf.add_zone('Inner Core', 500, 740)
        return prf
