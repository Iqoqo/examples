#!/usr/bin/env python3.6

from pylab import *
import os
from PyAstronomy.modelSuite import forTrans as ft
import pymultinest
import scipy
import pandas as pd
import warnings
from ttvfaster import run_ttvfaster
from PyAstronomy import funcFit as fuf
import sys

DropboxFolderVar = '' 
DataFolder = ''

# read file names form arg
if len(sys.argv) == 3:
    params_file_name = sys.argv[2]
    data_file_name = sys.argv[1]
else:
    sys.exit('Error! should have two parameters')

# PARAMETERS
KOI_Systems = [1576]  # Currently all are executed - even if more than the number of cores (no "queue")
KeplerCadence = 1765.5/86400  # see KeplerData Characteristics Handbook, sec. 1.1 par. 1 at: http://archive.stsci.edu/kepler/manuals/Data_Characteristics.pdf
earth_mass = 0.000003003  # Fractional Solar mass
integrate_days = 0  # if zero then auto-determined from the data
EccentricitySigma = 0.02
SamplingEfficiency = 0.5
EvidenceTolerance = 0.1    # lower value => more sample points
FitEccentricity = True
#DataFolder = '/Exoplanets/TTV_masses_data/Kepler light curves/'  # path relative to Dropbox folder

def TTV_circ_LC (time, TTV_signal, TT0, p, a, inc, b, linLimb_coefficient, quadLimb_coefficient, planet_star_ratio, transit_width, ReBin_N=1, ReBin_dt=0):

    # ma = ft.MandelAgolLC(orbit="circular",ld="quad")  # Setting Mandel-Agol function to circular orbit with a quadratic limb darkening model

    ma_ttv = np.ones(len(time))

    i_transits = [int(i) for i in range(len(time)) if abs(((time[i] - TT0 + (p / 2)) % p) - (p / 2)) < p * transit_width] # Indices of transists for the entire light curve
    t_transits = time[i_transits] # Times of transits for the entire light curve
    j_transits = t_transits // p # Index of each transit event assigned assigned to relevant indices of each transit

    # j is the index of the transit
    # ma["a"] = a
    # ma["p"] = planet_star_ratio
    # ma["linLimb"] = linLimb_coefficient
    # ma["quadLimb"] = quadLimb_coefficient
    # ma["b"] = b
    # ma["T0"] = TT0

    TTV_signal = np.array(TTV_signal)
    shifted_times = t_transits

    j_indices = ((t_transits - TT0 + p / 2) // p)
    j_indices = np.array([int(i) for i in j_indices])
    for i in range(len(j_indices)):
        if (j_indices[i] >= 0):
            shifted_times[i] = shifted_times[i] - TTV_signal[j_indices[i]]

    # ma_transits = ma.evaluate(shifted_times)
    ma_transits = ma_with_oversmpling(Time=shifted_times, per=p, Tmid=TT0, p=planet_star_ratio, a=a, i=inc, linLimb=linLimb_coefficient, quadLimb=quadLimb_coefficient, orbit="circular", ld="quad", b=b, ReBin_N=ReBin_N, ReBin_dt=ReBin_dt, ToPlot=False)
    ma_ttv[i_transits] = ma_transits

    return (ma_ttv)

def ma_with_oversmpling(Time, per, Tmid, p, a, i, linLimb, quadLimb, orbit="circular", ld="quad", b=0, ReBin_N=1, ReBin_dt=0, ToPlot=False):
# Added ReBin_N, ReBin_dt to allow for finite integration time calculation by re-binning. These are the PyAstronomy parameters for the number of subsamples and the duration of the original samples

    if ReBin_N>1 and ReBin_dt>0:
        MA_Rebin = fuf.turnIntoRebin(ft.MandelAgolLC)
        ma = MA_Rebin()
        ma.setRebinArray_Ndt(Time, ReBin_N, ReBin_dt)
    else:
        ma = ft.MandelAgolLC()

    ma.pars._Params__params={"orbit":orbit, "ld":ld, "per":per, "i":i, "a":a, "p":p, "linLimb":linLimb, "quadLimb":quadLimb, "b":b, "T0":Tmid}
    model= ma.evaluate(Time)

    if ToPlot:
        plt.plot((Time - Tmid + per/2) % per - per/2, model, '.')
        plt.xlabel("Time since T_mid [d]")
        #plt.show()
    return model

def TTV_Signal_Generator_nPl (p_vec, T_vec, m_vec, i_vec, ex_vec, ey_vec, stellar_mass, t_min, t_max): # Running TTVFaster in an n_Planet scenario

    ################# Generating TTV signal ################## Generating TTV signal ################## Generating TTV signal ################## Generating TTV signal ################## Generating TTV signal ################## Generating TTV signal

    nPl = len(p_vec)  # Assessing number of planets
    params = [stellar_mass]

    # Setting integration time and mass-constants (TTVFast requires masses in Stellar-mass units)

    for j in range(nPl):    # optional alternative: params=np.asarray(([a.transpose(), b.transpose(), c.transpose()]))

        params.append(m_vec[j])
        params.append(p_vec[j])
        params.append(ex_vec[j])
        params.append(i_vec[j])
        params.append(- np.pi / 2)
        params.append(ey_vec[j])
        params.append(T_vec[j])

    data_ttvfaster = (run_ttvfaster(nPl, params, t_min, t_max, 10))  # Generating TTVFaster data [days]

    OC_list = []
    for j in range(nPl):

        linear_this = np.array([i for i in range(len(data_ttvfaster[j]))]) * p_vec[j] + T_vec[j]
        OC_this = data_ttvfaster[j] - linear_this
        OC_list.append(OC_this)

    return OC_list

def ReadKOIsTable(FileName=''):
    warnings.simplefilter(action="ignore", category=RuntimeWarning)

    if FileName is None or len(FileName) == 0:
        FileName = params_file_name

    if not(os.path.isfile(FileName)):
        print("ERROR: File {} does not exist.".format(FileName))
        return None

    # read the data, change the "kepoi_name" column label to "koi" (my personal choice), and make it a list of numbers (not strings)
    KOIs = pd.read_csv(FileName, comment='#')
    KOIs = KOIs.rename(columns={'kepoi_name': 'koi'})
    koi_numbers=KOIs["koi"]
    koi_numbers=[koi_numbers.values[i][1:] for i in range(len(koi_numbers.values))]  # remove initial letter "K" from each string
    koi_numbers=[float(koi_numbers[i]) for i in range(len(koi_numbers))]  # convert to float
    KOIs["koi"]=koi_numbers

    warnings.simplefilter('default')
    return KOIs

def input_quality_control(LC, PlanetParams, StarParams, SearchParams):
    # Input quality control
    if not (any(np.isreal(LC))):
        print("ERROR: not all LC values are real.")
        return -1.1

    if not (any(np.isreal(PlanetParams))):
        print("ERROR: not all PlanetParams values are real.")
        return -2.1

    if not (any(np.isreal(StarParams))):
        print("ERROR: not all StarParams values are real.")
        return -3.1

    if not (any(np.isreal(SearchParams))):
        print("ERROR: not all SearchParams values are real.")
        return -4.1

    # if not(isinstance(PlanetParams[i] in range(len(PlanetParams)), dict)):
    #     return -2.2
    #
    # if not(isinstance(StarParams[i] in range(len(StarParams)), dict)):
    #     return -3.2
    #
    # if not(isinstance(SearchParams[i] in range(len(SearchParams)), dict)):
    #     return -4.2

    return 0


def run(LC, PlanetParams, StarParams, SearchParams):


    def model(mass, exd, eyd):
        """
        mass, ex and ey for each planet (each is a vector).
        However, planet0 is forced to have zero eccentricity so the rest of the eccentricities are actually eccentricities-differences in the x- and y- directions
        """
        t_min = LC[0].min()
        t_max = LC[0].max()

        #OC = TTV_Signal_Generator_nPl(SearchParams["integrate_days"], per_list, Tmid_list,  mass, inc_list, exd, eyd, StarParams["StarMass"])  # time units)
        OC = TTV_Signal_Generator_nPl(per_list, Tmid_list, mass, inc_list, exd, eyd, StarParams["StarMass"], t_min = 0, t_max = 1600)  # time units)

        MAmodels = np.zeros([nPl, len(LC[0])])
        for j in range(nPl):
            MAmodels[j][:] = TTV_circ_LC(LC[0], OC[j], PlanetParams[j]["Tmid"], PlanetParams[j]["per"], PlanetParams[j]["a"], PlanetParams[j]["inc"], PlanetParams[j]["PlanetFlux"], StarParams["LDcoeff1"], StarParams["LDcoeff2"], PlanetParams[j]["r"], SearchParams["transit_width"], PlanetParams[j]["ReBin_N"], SearchParams["ReBin_dt"])
        MA_combined = MAmodels.sum(axis=0) - nPl + 1

        chi_squared = np.sum(((MA_combined - LC[1]) / LC[2]) ** 2)

        if len(BaseName) > 0:
            tmp = np.concatenate((np.asarray(mass) / earth_mass, np.asarray(exd[1:]), np.asarray(eyd[1:]), np.asarray([chi_squared])))
            np.savetxt(fid, tmp.reshape(1, 3 * nPl - 1))

        return chi_squared

    # Defining prior function
    def prior(cube, nDim, nPar):
        """
        the hypercube has: nPl masses, followed by (nPl-1) x-eccentricities, followed by (nPl-1) y-eccentricities,
        """
        for j in range(nPl):
            cube[j] = cube[j] * PlanetParams[j]["MaxMass"] * earth_mass  # uniform distribution for the masses
        for j in range(nPl - 1):
            cube[nPl + j] = SearchParams["EccentricitySigma"] * sqrt(2) * scipy.special.erfinv(2 * cube[nPl + j] - 1)  # Gaussian distribution for ex(j)-ex(j-1)
        for j in range(nPl - 1):
            cube[2 * nPl - 1 + j] = SearchParams["EccentricitySigma"] * sqrt(2) * scipy.special.erfinv(2 * cube[2 * nPl - 1 + j] - 1)  # Gaussian distribution for ey(j)-ey(j-1)


    # Defining a likelihood function
    def loglike(cube, nDim, nPar):
        """
        cube is a vector of: [nPl masses, nPl x-eccenctricities,nPl y-eccenctricities]
        However, planet0 is forced to have zero eccentricity so the rest of the eccentricities are actually eccentricities-differences in the x- and y- directions
        """
        mass = [cube[j] for j in range(nPl)]
        if SearchParams["FitEccentricity"]:
            exd = [cube[j] for j in range(nPl, 2 * nPl - 1)]
            eyd = [cube[j] for j in range(2 * nPl - 1, 3 * nPl - 2)]
        else:
            exd = np.zeros(nPl-1)
            eyd = np.zeros(nPl-1)
        exd.insert(0, 0)  # add eccentricity zero for inner planet
        eyd.insert(0, 0)  # add eccentricity zero for inner planet

        ModelChi2 = model(mass, exd, eyd)  # , LC, PlanetParams, StarParams, SearchParams)
        loglikelihood = -0.5 * ModelChi2  # Total sum of Chi-squared of the specific model
        return loglikelihood


    nPl = len(PlanetParams)
    # nPar = 4 * (nPl-1)
    # nDim = 4 * (nPl-1)
    nPar = 3 * nPl - 2
    nDim = 3 * nPl - 2

    # remove data points that occur before the very first transit in the system (and slightly before)
    # EarliestTime = min([PlanetParams[j]["Tmid"] - SearchParams["transit_width"] * PlanetParams[j]["per"] for j in range(nPl)])
    # LC = LC[:, LC[0] > EarliestTime]

    ErrorCode = input_quality_control(LC, PlanetParams, StarParams, SearchParams)
    if ErrorCode < 0:
        print("ERROR identified in input. Error code = " + ErrorCode.__str__())
        return ErrorCode

    # Standard output files base name
    BaseName=SearchParams["SystemName"] + 'Photodynamic_MCMC_'
    if SearchParams["FitEccentricity"]:
        CircStr = ''
    else:
        CircStr = 'circular_'
    if len(BaseName) > 0:
        if os.path.isfile(BaseName + '.AllParams.txt'):
            os.remove(BaseName + CircStr + '.AllParams.txt')
        fid = open(BaseName + '.AllParams.txt', 'ab')

    per_list=[PlanetParams[j]["per"] for j in range(len(PlanetParams))]
    Tmid_list = [PlanetParams[j]["Tmid"] for j in range(len(PlanetParams))]
    inc_list = [PlanetParams[j]["inc"] for j in range(len(PlanetParams))]

    # Initiating MultiNest
    pymultinest.run(loglike, prior, n_dims=nDim, n_params=nPar, outputfiles_basename=BaseName, sampling_efficiency=SearchParams["sampling_efficiency"], evidence_tolerance=SearchParams["evidence_tolerance"], resume=False, verbose=True)
    if len(BaseName) > 0:
        fid.close()

# moved this code down for visibility, Eli Shvartsman
# prepare input variables to Photodynamic_TTVFaster
KOIs = ReadKOIsTable()
LC, PlanetParams, StarParams, SearchParams = [{} for _ in range(len(KOI_Systems))], [{} for _ in range(len(KOI_Systems))], [{} for _ in range(len(KOI_Systems))], [{} for _ in range(len(KOI_Systems))]

for s in range(len(KOI_Systems)):

    # INPUT DATA
    # data of all planets in columns: [Time Flux FluxErr LinearModel_0 LinearModel_1 LinearModel_2 ....].
    # Linear models are optional - for perturbative approach (NOT implemented)
    PhotometryFileName = data_file_name # Eli Shvartsman
    if os.path.isfile(PhotometryFileName):
        LC[s] = np.transpose(np.loadtxt(PhotometryFileName))
    else:
        print("ERROR: File " + PhotometryFileName + " does not exist.")
        exit()

    # Choose objects - automatically (all KOIs around host) or manually.
    KOIsToModel = KOIs["koi"].loc[np.floor(KOIs['koi']) == KOI_Systems[s]].values  # can also be manually input, if some object needs to be skipped.
    nPl = len(KOIsToModel)
    if integrate_days == 0:
        integrate_days = LC[0].max() - LC[0].min()

    # ====================== END OF USER PARAMETERS ============================

    per, Tmid, inc, a, r, PlanetFlux, ReBin_N = np.zeros(nPl), np.zeros(nPl), np.zeros(nPl), np.zeros(nPl), np.zeros(nPl), np.zeros(nPl), np.zeros(nPl)
    # PlanetParams = [{} for _ in range(nPl)]
    # StarParams = {}
    # SearchParams = {}


    for i in range(nPl):

        tmp = KOIs[KOIs['koi'] == KOIsToModel[i]][["koi_period", "koi_time0bk", "koi_incl", "koi_dor", "koi_ror"]].values[0]
        per[i], Tmid[i], inc[i], a[i], r[i] = tmp[0:len(tmp)]
        PlanetFlux[i] = 0
        ReBin_N[i] = 1
        PlanetParams[s][i] = {'NameStr': "KOI-" + KOIsToModel[i].__str__(), 'per': per[i], 'Tmid': Tmid[i], 'inc':inc[i], 'a': a[i], 'r': r[i], 'ReBin_N': ReBin_N[i], 'PlanetFlux': 0, 'MaxMass': 100}

        if i == 0:
            tmp = KOIs[KOIs['koi'] == KOIsToModel[i]][["koi_smass", "koi_ldm_coeff1", "koi_ldm_coeff2", "koi_ldm_coeff3", "koi_ldm_coeff4"]].values[0]
            StarParams[s] = dict(StarMass=tmp[0], LDcoeff1=tmp[1], LDcoeff2=tmp[2], LDcoeff3=tmp[3], LDcoeff4=tmp[4], L3=0)

    # sort by period -- in a kinda non-pythonic code
    idx = np.argsort([PlanetParams[s][i]["per"] for i in range(len(PlanetParams[s]))])
    PlanetParams[s] = [PlanetParams[s][idx[i]] for i in range(len(PlanetParams[s]))]

    # PlanetParams[s] = sorted(PlanetParams[s], key=lambda k: k['per'])  # should be more pythonic, bud doesn't work?

    SearchParams[s] = dict(SystemName=DropboxFolderVar + DataFolder + KOI_Systems[s].__str__() + '_system', ReBin_dt=KeplerCadence, integrate_days=integrate_days, FitEccentricity = FitEccentricity, EccentricitySigma=EccentricitySigma, transit_width=0.05,  sampling_efficiency=SamplingEfficiency, evidence_tolerance=EvidenceTolerance)
    # SearchParams["SystemName"] = 'whatever'

    print("Prepared inputs for KOI system {}".format(KOI_Systems[s]))

    [run(LC[s], PlanetParams[s], StarParams[s], SearchParams[s]) for s in range(len(KOI_Systems))] # Eli Shvartsman

