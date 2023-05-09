#!/usr/bin/env python
# coding: utf-8

# # Grass growth anomalies
#
# - Weighted means take into account the number of days in each month

# import libraries
from datetime import datetime, timezone
import climag.plot_stats as cstats
import importlib
import xarray as xr
import matplotlib.pyplot as plt
import climag.plot_configs as cplt
import glob
import itertools
import os
import sys
import numpy as np

# season_list = ["DJF", "MAM", "JJA", "SON"]
exp_list = ["historical", "rcp45", "rcp85"]
model_list = ["CNRM-CM5", "EC-EARTH", "HadGEM2-ES", "MPI-ESM-LR"]
dataset_list = ["EURO-CORDEX", "HiResIreland"]
# stat_list = ["mean", "std", "max", "min"]

importlib.reload(cstats)


def keep_minimal_vars(data):
    """
    Drop variables that are not needed
    """

    # data = data.assign(prod=data["i_bm"] + data["h_bm"])

    data = data.drop_vars(
        [
            "bm_gv",
            "bm_gr",
            "bm_dv",
            "bm_dr",
            "age_gv",
            "age_gr",
            "age_dv",
            "age_dr",
            "omd_gv",
            "omd_gr",
            "lai",
            "env",
            "wr",
            "aet",
            "sen_gv",
            "sen_gr",
            "abs_dv",
            "abs_dr",
            "c_bm",
            "bm",
            "pgro",
            "i_bm",
            "h_bm",
        ]
    )

    return data


def combine_datasets(dataset_dict, dataset_crs):
    dataset = xr.combine_by_coords(
        dataset_dict.values(), combine_attrs="override"
    )
    dataset.rio.write_crs(dataset_crs, inplace=True)

    return dataset


def generate_stats(ensemble=True):
    eurocordex = {}
    eurocordex_lta = {}
    hiresireland = {}
    hiresireland_lta = {}

    for exp, model, dataset in itertools.product(
        exp_list, model_list, dataset_list
    ):
        # auto-rechunking may cause NotImplementedError with object dtype where it
        # will not be able to estimate the size in bytes of object data
        if model == "HadGEM2-ES":
            CHUNKS = 300
        else:
            CHUNKS = "auto"

        ds = xr.open_mfdataset(
            glob.glob(
                os.path.join(
                    "data",
                    "ModVege",
                    dataset,
                    exp,
                    model,
                    f"*{dataset}*{model}*{exp}*.nc",
                )
            ),
            chunks=CHUNKS,
            decode_coords="all",
        )

        if dataset == "EURO-CORDEX":
            crs_eurocordex = ds.rio.crs
        else:
            crs_hiresireland = ds.rio.crs

        # convert HadGEM2-ES data back to 360-day calendar
        # this ensures that the correct weighting is applied when
        # calculating the weighted average
        if model == "HadGEM2-ES":
            ds = ds.convert_calendar("360_day", align_on="year")

        # remove spin-up year
        if exp == "historical":
            ds = ds.sel(time=slice("1976", "2005"))
        else:
            ds = ds.sel(time=slice("2041", "2070"))

        # assign new coordinates and dimensions
        ds = ds.assign_coords(exp=exp)
        ds = ds.expand_dims(dim="exp")
        ds = ds.assign_coords(model=model)
        ds = ds.expand_dims(dim="model")

        # drop unnecessary variables
        ds = keep_minimal_vars(data=ds)

        # weighted mean growth
        ds_1 = ds.copy()
        # calculate the weights by grouping month length by season
        weights = (
            ds_1["time"].dt.days_in_month.groupby("time.year")
            / ds_1["time"].dt.days_in_month.groupby("time.year").sum()
        )
        # test that the sum of weights for each season is one
        np.testing.assert_allclose(
            weights.groupby("time.year").sum().values,
            np.ones(len(set(weights["year"].values))),
        )
        # calculate the weighted average
        ds_1 = (ds_1 * weights).groupby("time.year").sum(dim="time")
        if ensemble:
            ds_1 = ds_1.mean(dim="model", skipna=True)

        # long-term average
        if ensemble:
            ds_2 = ds.mean(dim=["time", "model"], skipna=True)
        else:
            ds_2 = ds.mean(dim="time", skipna=True)

        if dataset == "EURO-CORDEX":
            eurocordex[f"{dataset}_{model}_{exp}"] = ds_1.copy()
            eurocordex_lta[f"{dataset}_{model}_{exp}"] = ds_2.copy()
        else:
            hiresireland[f"{dataset}_{model}_{exp}"] = ds_1.copy()
            hiresireland_lta[f"{dataset}_{model}_{exp}"] = ds_2.copy()

    eurocordex = combine_datasets(eurocordex, crs_eurocordex)
    hiresireland = combine_datasets(hiresireland, crs_hiresireland)
    eurocordex_lta = combine_datasets(eurocordex_lta, crs_eurocordex)
    hiresireland_lta = combine_datasets(hiresireland_lta, crs_hiresireland)

    return eurocordex, hiresireland, eurocordex_lta, hiresireland_lta


# def plot_diff(data, lta, levels):
#     for exp in exp_list:
#         data_plot = data - lta
#         data_plot = data_plot.sel(exp=exp)
#         if exp == "historical":
#             data_plot = data_plot.sel(year=slice("1976", "2005"))
#         else:
#             data_plot = data_plot.sel(year=slice("2041", "2070"))
#         print(exp)
#         fig = data_plot["gro"].plot.contourf(
#             x="rlon", y="rlat", col="year", col_wrap=5,
#             cmap="BrBG", extend="both", robust=True,
#             # levels=cstats.colorbar_levels(levels),
#             subplot_kws={"projection": cplt.plot_projection},
#             transform=cplt.rotated_pole_transform(data),
#             xlim=(-1.775, 1.6),
#             ylim=(-2.1, 2.1),
#             # figsize=(12, 9.25),
#             cbar_kwargs = {
#                 "label": "Anomaly [kg DM ha⁻¹ day⁻¹]",
#                 "aspect": 30,
#                 "location": "bottom",
#                 "fraction": 0.085,
#                 "shrink": 0.85,
#                 "pad": 0.05,
#                 "extendfrac": "auto",
#                 # "ticks": cstats.colorbar_ticks(levels)
#             }
#         )
#         for axis in fig.axs.flat:
#             cstats.ie_bbox.to_crs(cplt.plot_projection).plot(
#                 ax=axis, edgecolor="darkslategrey", color="white",
#                 linewidth=.5
#             )
#         fig.set_titles("{value}", weight="semibold", fontsize=14)
#         plt.show()

# def calculate_diff(data):
#     data_out = xr.combine_by_coords([
#         (
#             data.sel(exp="rcp45") - data.sel(exp="historical")
#         ).assign_coords(exp="rcp45 - historical").expand_dims(dim="exp"),
#         (
#             data.sel(exp="rcp85") - data.sel(exp="historical")
#         ).assign_coords(exp="rcp85 - historical").expand_dims(dim="exp")
#     ])
#     return data_out

# ## Mean growth

eurocordex, hiresireland, eurocordex_lta, hiresireland_lta = generate_stats()
# eurocordex_diff = calculate_diff(eurocordex)
# hiresireland_diff = calculate_diff(hiresireland)

eurocordex

eurocordex_lta

eurocordex_diff = eurocordex - eurocordex_lta

hiresireland_diff = hiresireland - hiresireland_lta

eurocordex_diff


def plot_diff(data, levels):
    for exp in exp_list:
        print(exp)
        if exp == "historical":
            data_plot = data.sel(year=slice("1976", "2005"))
        else:
            data_plot = data.sel(year=slice("2041", "2070"))
        fig = data_plot.sel(exp=exp)["gro"].plot.contourf(
            x="rlon",
            y="rlat",
            col="year",
            col_wrap=10,
            subplot_kws={"projection": cplt.plot_projection},
            transform=cplt.rotated_pole_transform(data),
            xlim=(-1.775, 1.6),
            ylim=(-2.1, 2.1),
            figsize=(15, 7.25),
            extend="both",
            robust=True,
            cmap="BrBG",
            levels=cstats.colorbar_levels(levels),
            cbar_kwargs={
                "label": "Anomaly [kg DM ha⁻¹ day⁻¹]",
                "aspect": 40,
                "location": "bottom",
                "fraction": 0.085,
                "shrink": 0.85,
                "pad": 0.05,
                "extendfrac": "auto",
                "ticks": cstats.colorbar_ticks(levels),
            },
        )
        for axis in fig.axs.flat:
            cstats.ie_bbox.to_crs(cplt.plot_projection).plot(
                ax=axis,
                edgecolor="darkslategrey",
                color="white",
                linewidth=0.5,
            )
        fig.set_titles("{value}", weight="semibold", fontsize=14)
        plt.show()


plot_diff(eurocordex_diff, 8)

plot_diff(hiresireland_diff, 8)
