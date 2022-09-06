import math

def jouven():
    Tmean =  # mean daily temperature
    Tsum_begin =  # sum of temperatures at the beginning of the reproductive period
    Tsum_end =  # sum of temperatures at the end of the reproductive period
    T0 = 0

    # standing biomass
    BMgv =
    BMgr =
    BMdv =
    BMdr =

    pct_LAM =
    SLA =
    PARi =
    RUEmax =
    LAI = SLA * BMgv/10 * pct_LAM  # leaf area index
    PGRO = PARi * RUEmax * (1 - math.exp(-.6 * LAI)) * 10

    PET =
    AET = min(PET, PET * LAI/3)  # actual evapotranspiration
    WR = max(0, WR + PP - AET)  # water reserves
    W = WR/WHC  # water stress

    ENV = NI * fPARi * fTmean * fW
    GRO = PGRO * ENV * SEA  # total growth
    CUT =
    REP = .25 + ((1 - .25) * (NI - .35))/(1 - .35) * CUT  # reproductive function
    LLS =  # leaf lifespan for GV

    # growth
    GROgv = GRO * (1 - REP)
    GROgr = GRO * REP

    # age in units of thermal time
    AGEgv =
    AGEgr =
    AGEdv =

    # organic matter digestibility
    maxOMDgv =
    minOMDgv =
    maxOMDgr =
    minOMDgr =
    OMDdv =  # constant for dead compartments
    OMDdr =  # constant for dead compartments
    OMDgv = maxOMDgv - (AGEgv * (maxOMDgv - minOMDgv))/LLS
    OMDgr = maxOMDgr - (AGEgr * (maxOMDgr - minOMDgr))/(Tsum_end - Tsum_begin)

    # senescence
    if Tmean >= T0:  # using >= instead of >
        SENgv = Kgv * BMgv * Tmean * fAGEgv
        SENgr = Kgr * BMgr * Tmean * fAGEgr
    else:
        SENgv = Kgv * BMgv * math.fabs(Tmean)
        SENgr = Kgr * BMgr * math.fabs(Tmean)

    # abscission
    ABSdv = Kldv * BMdv * Tmean * fAGEdv
    ABSdr = Kldr * BMdr * Tmean * fAGEdr

    # biomass losses through respiration during senescence
    SIGgv =
    SIGgr =

    # biomass of the green vegetative compartment (GV)
    dBMgv_dt = GROgv - SENgv

    # biomass of the green reproductive compartment (GR)
    dBMgr_dt = GROgr - SENgr

    # biomass of the dead vegetative compartment (DV)
    dBMdv_dt = (1 - SIGgv) * SENgv - ABSdv

    # biomass of the dead reproductive compartment (DR)
    dBMdr_dt = (1 - SIGgr) * SENgr - ABSdr

    # mean age of the biomass in each compartment
    if Tmean >= T0:
        AGEgv_in = (AGEgv + Tmean)
        AGEgr_in = (AGEgr + Tmean)
        AGEdv_in = (AGEdv + Tmean)
        AGEdr_in = (AGEdr + Tmean)
    else:
        AGEgv_in = AGEgv
        AGEgr_in = AGEgr
        AGEdv_in = AGEdv
        AGEdr_in = AGEdr

    dAGEgv_dt = (BMgv - SENgv)/(BMgv - SENgv + GROgv) * AGEgv_in - AGEgv
    dAGEgr_dt = (BMgr - SENgr)/(BMgr - SENgr + GROgr) * AGEgr_in - AGEgr
    dAGEdv_dt = (
        (BMdv - ABSdv)/(BMdv - ABSdv + (1 - SIGgv) * SENgv) * AGEdv_in - AGEdv
    )
    dAGEdr_dt = (
        (BMdr - ABSdr)/(BMdr - ABSdr + (1 - SIGgr) * SENgr) * AGEdr_in - AGEdr
    )

    BDgv =
    resBMgv = .05 * 10 * BDgv
