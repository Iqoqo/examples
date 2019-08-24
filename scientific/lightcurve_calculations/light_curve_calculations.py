#!/usr/bin/env python3.6

from ttvfaster import run_ttvfaster
import numpy as np
from pylab import *
from PyAstronomy.modelSuite import forTrans as ft
import sys

# read file names form arg
if len(sys.argv) > 2:
    real_data_file = sys.argv[1]
    orbital_params_file = sys.argv[2]
else:
    sys.exit('Error! This script requires at least two arguments')

print("Using orbital params from %s and data from %s\n" % (orbital_params_file, real_data_file))

orbital_params = np.loadtxt(orbital_params_file) # Importing astrophysical parameters of the system which will be used in the construction of a synthetic light-curve
time = np.loadtxt('time_set.txt')
real_data = np.loadtxt(real_data_file)

mag = 1e-6 # Gaussian noise standard deviation
integrate_days = 1600

# Keplerian orbit and quadratic limb darkening
ma = ft.MandelAgolLC(orbit="circular", ld="quad") # Initiating Mandel-Agol function

p0 = orbital_params[0]
p1 = orbital_params[1]
stellar_mass = orbital_params[2]
TT0 = orbital_params[3]
TT1 = orbital_params[4]
linLimb_coefficient = orbital_params[5]
quadLimb_coefficient = orbital_params[6]
b0 = orbital_params[7]
b1 = orbital_params[8]
i0 = orbital_params[9]
i1 = orbital_params[10]
a0 = orbital_params[11]
a1 = orbital_params[12]
planet0_star_ratio = orbital_params[13]
planet1_star_ratio = orbital_params[14]
earth_mass = 0.000003003

################## Mandel-Agol linear (both planets) ################## Mandel-Agol linear (both planets) ################## Mandel-Agol linear (both planets) ################## Mandel-Agol linear (both planets) ################## Mandel-Agol linear (both planets)

# Generating a linear and a TTV Mandel-Agol light-curve (planet 0)
ma["per"] = p0
ma["i"] = i0
ma["a"] = a0
ma["p"] = planet0_star_ratio
ma["linLimb"] = linLimb_coefficient
ma["quadLimb"] = quadLimb_coefficient
ma["b"] = b0
ma["T0"] = TT0

ma0_linear = ma.evaluate(time)

ma["per"] = p1
ma["i"] = i1
ma["a"] = a1
ma["p"] = planet1_star_ratio
ma["linLimb"] = linLimb_coefficient
ma["quadLimb"] = quadLimb_coefficient
ma["b"] = b1
ma["T0"] = TT1

ma1_linear = ma.evaluate(time)

ma_linear_combined = [np.minimum(ma0_linear[i], ma1_linear[i]) for i in range(len(time))]

################## Mode generation ################## Mode generation ################## Mode generation ################## Mode generation ################## Mode generation ################## Mode generation ################## Mode generation

################## Mandel-Agol linear (both planets) ################## Mandel-Agol linear (both planets) ################## Mandel-Agol linear (both planets) ################## Mandel-Agol linear (both planets) ################## Mandel-Agol linear (both planets)

ex = 0.001
ey = 0.001
mu0 = earth_mass
mu1 = earth_mass

values_ecosomega = [0, ex, 0]
values_esinomega = [0, 0, ey]

for x in range(len(values_ecosomega)):

    m0 = mu0  # Original value: 5.090*earth_mass
    ecosomega_0 = 0  # 0.011
    inc0 = deg2rad(i0)
    esinomega_0 = 0  # 0.037
    Omega0 = -(math.pi) / 2  # Longitude of ascending node (big Omega)

    m1 = mu1  # Original value: 3.280*earth_mass
    ecosomega_1 = values_ecosomega[x]  # 0.006  # e1*cos(argument of periastron)
    inc1 = deg2rad(i1)
    esinomega_1 = values_esinomega[x]  # e0*cos(argument of periastron)
    Omega1 = -(math.pi) / 2  # Longitude of ascending node (big Omega)

    # Setting integration time and mass-constants (TTVFast requires masses in Stellar-mass units)
    params = [stellar_mass, m0, p0, ecosomega_0, inc0, Omega0, esinomega_0, TT0, m1, p1, -ecosomega_1, inc1, Omega1,-esinomega_1, TT1]  ### NOTE NEGATIVE -esinomega ###

    data_ttvfaster = (run_ttvfaster(2, params, 0, integrate_days, 10))

    a = np.linspace(0, len(data_ttvfaster[0]) - 1, len(data_ttvfaster[0]))
    linear_fit0 = np.polyfit(a, data_ttvfaster[0], 1)
    linear_ephemeris0 = [linear_fit0[1] + linear_fit0[0] * i for i in range(len(data_ttvfaster[0]))]

    a = np.linspace(0, len(data_ttvfaster[1]) - 1, len(data_ttvfaster[1]))
    linear_fit1 = np.polyfit(a, data_ttvfaster[1], 1)
    linear_ephemeris1 = [linear_fit1[1] + linear_fit1[0] * i for i in range(len(data_ttvfaster[1]))]

    if (x == 0):  # F0 - Zero relative eccentricity

        ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0

        F0_planet0 = [transpose(data_ttvfaster[0])[i] - linear_ephemeris0[i] for i in
                      range(len(transpose(data_ttvfaster[0])))]

        # Generating a TTV signal and a subsequent light-curve (planet 0)
        F0_P0 = np.ones(len(time))
        ma0_transits = np.array([])

        current_transit = np.array([])
        transit_indices = np.array([])

        r = 0
        mark = 0

        for x in range(len(F0_planet0)):

            mark = 0

            for i in range(len(time)):
                if (np.abs(time[i] - p0 * x - TT0) < p0 / 10):
                    current_transit = np.append(current_transit, time[i])
                    transit_indices = np.append(transit_indices, i)
                    r = i
                    mark = 1

                elif (mark == 1):
                    break

            ma["per"] = p0
            ma["i"] = i0
            ma["a"] = a0
            ma["p"] = planet0_star_ratio
            ma["linLimb"] = linLimb_coefficient
            ma["quadLimb"] = quadLimb_coefficient
            ma["b"] = b0
            ma["T0"] = TT0 + F0_planet0[x]

            ma_frac = ma.evaluate(current_transit)
            ma0_transits = np.append(ma0_transits, ma_frac)

            current_transit = ([])

        for i in range(len(transit_indices)):
            F0_P0[int(transit_indices[i])] = ma0_transits[i]

        ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1

        F0_planet1 = [transpose(data_ttvfaster[1])[i] - linear_ephemeris1[i] for i in range(len(transpose(data_ttvfaster[1])))]

        # Generating a TTV signal and a subsequent light-curve (planet 0)
        F0_P1 = np.ones(len(time))
        ma1_transits = np.array([])

        current_transit = np.array([])
        transit_indices = np.array([])

        r = 0
        mark = 0

        for x in range(len(F0_planet1)):

            mark = 0

            for i in range(len(time)):
                if (np.abs(time[i] - p1 * x - TT1) < p1 / 10):
                    current_transit = np.append(current_transit, time[i])
                    transit_indices = np.append(transit_indices, i)
                    r = i
                    mark = 1

                elif (mark == 1):
                    break

            ma["per"] = p1
            ma["i"] = i1
            ma["a"] = a1
            ma["p"] = planet1_star_ratio
            ma["linLimb"] = linLimb_coefficient
            ma["quadLimb"] = quadLimb_coefficient
            ma["b"] = b1
            ma["T0"] = TT1 + F0_planet1[x]

            ma_frac = ma.evaluate(current_transit)
            ma1_transits = np.append(ma1_transits, ma_frac)

            current_transit = ([])

        for i in range(len(transit_indices)):
            F0_P1[int(transit_indices[i])] = ma1_transits[i]

    if (x == 1):  # Fey - Eccentricity in the x direction (Pericenter perpendicular to the observer)

        ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0

        Fey_planet0 = [transpose(data_ttvfaster[0])[i] - linear_ephemeris0[i] for i in range(len(transpose(data_ttvfaster[0])))]

        # Generating a TTV signal and a subsequent light-curve (planet 0)
        Fey_P0 = np.ones(len(time))
        ma0_transits = np.array([])

        current_transit = np.array([])
        transit_indices = np.array([])

        r = 0
        mark = 0

        for x in range(len(Fey_planet0)):

            mark = 0

            for i in range(len(time)):
                if (np.abs(time[i] - p0 * x - TT0) < p0 / 10):
                    current_transit = np.append(current_transit, time[i])
                    transit_indices = np.append(transit_indices, i)
                    r = i
                    mark = 1

                elif (mark == 1):
                    break

            ma["per"] = p0
            ma["i"] = i0
            ma["a"] = a0
            ma["p"] = planet0_star_ratio
            ma["linLimb"] = linLimb_coefficient
            ma["quadLimb"] = quadLimb_coefficient
            ma["b"] = b0
            ma["T0"] = TT0 + Fey_planet0[x]

            ma_frac = ma.evaluate(current_transit)
            ma0_transits = np.append(ma0_transits, ma_frac)

            current_transit = ([])

        for i in range(len(transit_indices)):
            Fey_P0[int(transit_indices[i])] = ma0_transits[i]

        ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1

        Fey_planet1 = [transpose(data_ttvfaster[1])[i] - linear_ephemeris1[i] for i in
                       range(len(transpose(data_ttvfaster[1])))]

        # Generating a TTV signal and a subsequent light-curve (planet 0)
        Fey_P1 = np.ones(len(time))
        ma1_transits = np.array([])

        current_transit = np.array([])
        transit_indices = np.array([])

        r = 0
        mark = 0

        for x in range(len(Fey_planet1)):

            mark = 0

            for i in range(len(time)):
                if (np.abs(time[i] - p1 * x - TT1) < p1 / 10):
                    current_transit = np.append(current_transit, time[i])
                    transit_indices = np.append(transit_indices, i)
                    r = i
                    mark = 1

                elif (mark == 1):
                    break

            ma["per"] = p1
            ma["i"] = i1
            ma["a"] = a1
            ma["p"] = planet1_star_ratio
            ma["linLimb"] = linLimb_coefficient
            ma["quadLimb"] = quadLimb_coefficient
            ma["b"] = b1
            ma["T0"] = TT1 + Fey_planet1[x]

            ma_frac = ma.evaluate(current_transit)
            ma1_transits = np.append(ma1_transits, ma_frac)

            current_transit = ([])

        for i in range(len(transit_indices)):
            Fey_P1[int(transit_indices[i])] = ma1_transits[i]

    if (x == 2):  # Fex - Eccentricity in the x direction (Pericenter towards the observer)

        ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0  ############### Planet 0

        Fex_planet0 = [transpose(data_ttvfaster[0])[i] - linear_ephemeris0[i] for i in
                       range(len(transpose(data_ttvfaster[0])))]

        # Generating a TTV signal and a subsequent light-curve (planet 0)
        Fex_P0 = np.ones(len(time))
        ma0_transits = np.array([])

        current_transit = np.array([])
        transit_indices = np.array([])

        r = 0
        mark = 0

        for x in range(len(Fey_planet0)):

            mark = 0

            for i in range(len(time)):
                if (np.abs(time[i] - p0 * x - TT0) < p0 / 10):
                    current_transit = np.append(current_transit, time[i])
                    transit_indices = np.append(transit_indices, i)
                    r = i
                    mark = 1

                elif (mark == 1):
                    break

            ma["per"] = p0
            ma["i"] = i0
            ma["a"] = a0
            ma["p"] = planet0_star_ratio
            ma["linLimb"] = linLimb_coefficient
            ma["quadLimb"] = quadLimb_coefficient
            ma["b"] = b0
            ma["T0"] = TT0 + Fex_planet0[x]

            ma_frac = ma.evaluate(current_transit)
            ma0_transits = np.append(ma0_transits, ma_frac)

            current_transit = ([])

        for i in range(len(transit_indices)):
            Fex_P0[int(transit_indices[i])] = ma0_transits[i]

        ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1 ############### Planet 1

        Fex_planet1 = [transpose(data_ttvfaster[1])[i] - linear_ephemeris1[i] for i in
                       range(len(transpose(data_ttvfaster[1])))]

        # Generating a TTV signal and a subsequent light-curve (planet 0)
        Fex_P1 = np.ones(len(time))
        ma1_transits = np.array([])

        current_transit = np.array([])
        transit_indices = np.array([])

        r = 0
        mark = 0

        for x in range(len(Fey_planet1)):

            mark = 0

            for i in range(len(time)):
                if (np.abs(time[i] - p1 * x - TT1) < p1 / 10):
                    current_transit = np.append(current_transit, time[i])
                    transit_indices = np.append(transit_indices, i)
                    r = i
                    mark = 1

                elif (mark == 1):
                    break

            ma["per"] = p1
            ma["i"] = i1
            ma["a"] = a1
            ma["p"] = planet1_star_ratio
            ma["linLimb"] = linLimb_coefficient
            ma["quadLimb"] = quadLimb_coefficient
            ma["b"] = b1
            ma["T0"] = TT1 + Fex_planet1[x]

            ma_frac = ma.evaluate(current_transit)
            ma1_transits = np.append(ma1_transits, ma_frac)

            current_transit = ([])

        for i in range(len(transit_indices)):
            Fex_P1[int(transit_indices[i])] = ma1_transits[i]

################## Mode data ################## Mode data ################## Mode data ################## Mode data ################## Mode data ################## Mode data ################## Mode data ################## Mode data

# Generating mode residuals and orthogonalizing

F0_P0_resid = [F0_P0[i] - ma0_linear[i] for i in range(len(time))]
Fey_P0_resid = [Fey_P0[i] - ma0_linear[i] for i in range(len(time))]
Fex_P0_resid = [Fex_P0[i] - ma0_linear[i] for i in range(len(time))]

F0_P1_resid = [F0_P1[i] - ma1_linear[i] for i in range(len(time))]
Fey_P1_resid = [Fey_P1[i] - ma1_linear[i] for i in range(len(time))]
Fex_P1_resid = [Fex_P1[i] - ma1_linear[i] for i in range(len(time))]

G0_p0 = [F0_P0_resid[i] / mu1 for i in range(len(time))]
G0_p1 = [F0_P1_resid[i] / mu0 for i in range(len(time))]

Fey_p0 = [(Fey_P0_resid[i] - mu1 * G0_p0[i]) / (mu1 * ey) for i in range(len(time))]
Fey_p1 = [(Fey_P1_resid[i] - mu0 * G0_p1[i]) / (mu0 * ey) for i in range(len(time))]

Fex_p0 = [(Fex_P0_resid[i] - mu1 * G0_p0[i]) / (mu1 * ex) for i in range(len(time))]
Fex_p1 = [(Fey_P1_resid[i] - mu0 * G0_p1[i]) / (mu0 * ex) for i in range(len(time))]

A0ex = np.dot(G0_p0, Fex_p0) / np.dot(Fex_p0, Fex_p0)
A1ex = np.dot(G0_p1, Fex_p1) / np.dot(Fex_p1, Fex_p1)
#
A0ey = np.dot(G0_p0, Fey_p0) / np.dot(Fey_p0, Fey_p0)
A1ey = np.dot(G0_p1, Fey_p1) / np.dot(Fey_p1, Fey_p1)

F0_p0 = [G0_p0[i] - A0ex * Fex_p0[i] - A0ey * Fey_p0[i] for i in range(len(time))]
F0_p1 = [G0_p1[i] - A1ex * Fex_p1[i] - A0ey * Fey_p1[i] for i in range(len(time))]

# Generating a 6-rowed matrix of the orthogonalized Mode residual vectors

matrix = np.zeros((6, len(time)))

for i in range(6):
    for j in range(len(time)):
        if (i == 0):
            matrix[i][j] = F0_p0[j]

        if (i == 1):
            matrix[i][j] = Fex_p0[j]

        if (i == 2):
            matrix[i][j] = Fey_p0[j]

        if (i == 3):
            matrix[i][j] = F0_p1[j]

        if (i == 4):
            matrix[i][j] = Fex_p1[j]

        if (i == 5):
            matrix[i][j] = Fey_p1[j]

matrix = transpose(matrix)

params = np.linalg.pinv(matrix)@(real_data)

# Extracting physical parameters of planet mass and orthogonal eccentricity components
mu_1 = params[0]
mu_0 = params[3]

ex0 = (params[1] / mu_0)
ex1 = (params[4] / mu_1)

ey0 = params[2] / mu_0
ey1 = params[5] / mu_1

mass0 = mu_0 / earth_mass # Normalizing mass to earth-mass
mass1 = mu_1 / earth_mass # Normalizing mass to earth-mass

best_fit = params@(np.transpose(matrix)) # Generating a best-fit model to our data

print('mass0: ', mass0)
print('mass1: ', mass1)

print('ex0: ', ex0)
print('ex1: ', ex1)

print('ey0: ', ey0)
print('ey1: ', ey1)

chi_squared = np.sum([((best_fit[i] - best_fit[i]) / 1e-4) ** 2 for i in range(len(time))]) # Calculating chi-squared with a constant error of 1e-4

output = [mass0, mass1, ex0, ex1, ey0, ey1, chi_squared]
