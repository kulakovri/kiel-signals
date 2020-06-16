from src.objects import profiles


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