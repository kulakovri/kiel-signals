grains = [
    "18-5h-1-2",
    "18-5h-1-8",
    "18-5h-1-10",
    "18-5h-x2-1-5",
    "18-5h-x2-1-13",
    "18-5h-x2-1-25",
    "18-5h-x2-1-27",
    "18-5h-x3-1-10",
    "18-5h-x3-1-12",
    "18-3a-1-8",
    "18-3a-2-2",
    "18-3a-2-5",
    "18-5h-x3-1-41",
    "18-5h-x3-1-49",
    "18-5h-x3-1-53",
    "18-5h-x3-1-54",
    "18-5h-x2-2-41",
    "18-5h-x2-2-43",
    "18-5h-x2-2-84"
]

molar_weights = {
    "Mn": 54.938,
    "Al": 26.9815,
    "K": 39.098,
    "O": 15.9994,
    "Cr": 51.996,
    "P": 30.9738,
    "Na": 22.99,
    "Ti": 47.867,
    "Si": 28.086,
    "V": 50.9415,
    "Mg": 24.305,
    "Ni": 58.693,
    "Ca": 40.078,
    "Fe": 55.845,
    "Sr": 103.62
}

profile_lenghts = {
    "1-007-18-5h-1-2L1.csv": 380.9,
    "1-008-18-5h-1-2L1a.csv": 444.4,
    "1-009-18-5h-1-2L2.csv": 448.6,
    "1-010-18-5h-1-2L2a.csv": 376.7,
    "1-011-18-5h-1-8L3.csv": 440.2,
    "1-012-18-5h-1-8L4.csv": 522.7,
    "1-013-18-5h-1-10L5.csv": 471.9,
    "1-014-18-5h-1-10L6.csv": 476.2,
    "1-019-18-5h-x2-1-5L7.csv": 378.8,
    "1-020-18-5h-x2-1-5L7a.csv": 391.5,
    "1-021-18-5h-x2-1-5L8.csv": 351.3,
    "1-022-18-5h-x2-1-5L8a.csv": 402.1,
    "1-023-18-5h-x2-1-13L9.csv": 476.1,
    "1-024-18-5h-x2-1-13L10.csv": 501.5,
    "1-025-18-5h-x2-1-25L11.csv": 491.0,
    "1-026-18-5h-x2-1-25L11a.csv": 234.9,
    "1-027-18-5h-x2-1-25L12.csv": 412.6,
    "1-028-18-5h-x2-1-25L12a.csv": 313.2,
    "1-029-18-5h-x2-1-27L13.csv": 440.2,
    "1-030-18-5h-x2-1-27L14.csv": 448.6,
    "1-032-VK18-5h-x3-1-10L15.csv": 349.2,
    "1-033-VK18-5h-x3-1-10L15a.csv": 249.7,
    "1-034-VK18-5h-x3-1-10L16.csv": 332.2,
    "1-035-18-5h-x3-1-10L16a.csv": 275.1,
    "1-036-18-5h-x3-1-12L17.csv": 380.9,
    "1-037-18-5h-x3-1-12L17a.csv": 220.1,
    "1-038-18-5h-x3-1-12L18.csv": 376.7,
    "1-039-18-5h-x3-1-12L18a.csv": 217.9,
    "2-005-VK18-3a-1-8L19.csv": 465.2,
    "2-006-VK18-3a-1-8L19a.csv": 455.5,
    "2-007-VK18-3a-1-8L20.csv": 538.8,
    "2-008-VK18-3a-1-8L20a.csv": 426.3,
    "2-009-VK18-3a-2-2L21.csv": 471.1,
    "2-010-VK18-3a-2-2L21a.csv": 360.5,
    "2-011-VK18-3a-2-2L22.csv": 478.3,
    "2-012-VK18-3a-2-2L22a.csv": 353.3,
    "2-013-VK18-3a-2-5L23.csv": 376.9,
    "2-014-VK18-3a-2-5L23a.csv": 441.0,
    "2-015-VK18-3a-2-5L24.csv": 453.8,
    "2-016-VK18-3a-2-5L24a.csv": 371.7,
    "2-023-VK18-5h-x3-1-41L25.csv": 374.6,
    "2-024-VK18-5h-x3-1-41L26.csv": 374.6,
    "2-025-VK18-5h-x3-1-49L27.csv": 556.6,
    "2-026-VK18-5h-x3-1-49L28.csv": 539.6,
    "2-027-VK18-5h-x3-1-53L29.csv": 476.1,
    "2-028-VK18-5h-x3-1-53L30.csv": 444.4,
    "2-029-VK18-5h-x3-1-53L31a.csv": 105.8,
    "2-030-VK18-5h-x3-1-54L32.csv": 305.7,
    "2-031-VK18-5h-x3-1-54L32a.csv": 284.1,
    "2-032-VK18-5h-x3-1-54L33.csv": 586.2,
    "2-035-VK18-5h-x2-2-41L34.csv": 340.7,
    "2-036-VK18-5h-x2-2-41L34a.csv": 325.9,
    "2-037-VK18-5h-x2-2-41L35.csv": 387.3,
    "2-038-VK18-5h-x2-2-41L35a.csv": 275.1,
    "2-039-VK18-5h-x2-2-43L36.csv": 554.4,
    "2-040-VK18-5h-x2-2-43L36a.csv": 211.6,
    "2-041-VK18-5h-x2-2-43L37.csv": 438.0,
    "2-042-VK18-5h-x2-2-43L37a.csv": 211.6,
    "2-043-VK18-5h-x2-2-84L38.csv": 461.3,
    "2-044-VK18-5h-x2-2-84L38a.csv": 442.3,
    "2-045-VK18-5h-x2-2-84L39.csv": 334.3,
    "2-046-VK18-5h-x2-2-84L39a.csv": 495.2
}

profile_overlaps = {
    "2-008-VK18-3a-1-8L20a.csv": 45.1,
    "2-029-VK18-5h-x3-1-53L31a.csv": 42.3,
    "2-040-VK18-5h-x2-2-43L36a.csv": 110.0,
    "2-044-VK18-5h-x2-2-84L38a.csv": 63.4
}

rim_to_core_lines = [
    "L2",
    "L4",
    "L5",
    "L8",
    "L10",
    "L12",
    "L14",
    "L16",
    "L18",
    "L20",
    "L22",
    "L24",
    "L26",
    "L28",
    "L30",
    "L31",
    "L33",
    "L35",
    "L37",
    "L39"
]

sph = {
    "Mn": 77.0,
    "Ce": 2.5,
    "Al": 156129.0,
    "K": 2324.0,
    "Co": 0.5,
    "Cr": 0.1,
    "Eu": 0.4,
    "P": 48.7,
    "Rb": 0.35,
    "Cu": 3.2,
    "Pb": 0.3,
    "Na": 33235.0,
    "Zn": 1.4,
    "La": 1.4,
    "Ti": 295.13,
    "Nd": 1.1,
    "V": 1.7,
    "Y": 0.26,
    "Ni": 0.0,
    "Li": 8.2,
    "Ba": 121.9,
    "Fe": 2876.0,
    "Pr": 0.3,
    "Sc": 0.2,
    "Dy": 0.1,
    "Si": 248911.0,
    "Ga": 14.9,
    "Mg": 663.0,
    "Sm": 0.2,
    "Gd": 0.1,
    "Ca": 87621.0,
    "Sr": 1024.0
}

# https://www-s.nist.gov/srmors/certificates/610.pdf

nist_610 = {
    "Mn": 444.0,
    "Ce": 453,
    "Al": 10300.0,
    "K": 464.0,
    "P": 413,
    "Rb": 425.7,
    "Cu": 441,
    "Na": 99400.0,
    "Ti": 452,
    "Nd": 430,
    "Y": 462,
    "Li": 468,
    "Ba": 452,
    "Fe": 458,
    "Si": 325800.0,
    "Ga": 433.0,
    "Mg": 432.0,
    "Sm": 453,
    "Ca": 82200.0,
    "Sr": 515.5,
    "Pb": 426
}

# Rocholl, Alexander. "Major and trace element composition and homogeneity of microbeam reference material:
# Basalt glass USGS BCR‐2G." Geostandards newsletter 22.1 (1998): 33-45.
# http://minerva.union.edu/hollochk/icp-ms/srm/usgs-bcr2.pdf

bcr_2 = {
    "Mn": 15200.0,
    "Ce": 53,
    "Al": 71400.0,
    "K": 1490.0,
    "P": 150,
    "Rb": 48.0,
    "Cu": 19,
    "Na": 23400.0,
    "Ti": 13500,
    "Nd": 28,
    "Y": 37,
    "Li": 9,
    "Ba": 683,
    "Fe": 96500,
    "Si": 253000.0,
    "Ga": 23.0,
    "Mg": 21600.0,
    "Sm": 6.7,
    "Ca": 50900,
    "Sr": 346.0,
    "Pb": 11
}

unreliable_standard_profiles = [
    "1-005-SPH.csv",
    "1-015-SPH3.csv",
    "2-003-SPH1.csv",
    "2-047-SPH.csv",
    "2-053-NIST612-1HZ.csv"
]

main_oxides = [
    "SiO2", "Al2O3", "FeO", "CaO", "Na2O", "K2O", "MgO", "SrO", "P2O5", "MnO", "TiO2", "An"
]
