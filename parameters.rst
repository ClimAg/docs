Parameters
==========

.. note::
   This page is still being worked on, so there may be some incomplete items.

ModVege is a mechanistic, dynamic pasture model.
ModVege has four compartments representing the structural components of herbage:

- Green vegetative (GV) - green leaves and sheath
- Dead vegetative (DV) - dead leaves and sheath
- Green reproductive (GR) - green stems and flowers
- Dead reproductive (DR) - dead stems and flowers

The compartments are described using the:

- Standing biomass (BM) [kg DM ha⁻¹]
- Age of biomass (AGE) [°C d] (degree day - units of thermal time)
- Organic matter digestibility (OMD)

Implementation
--------------

The Python implementation of the `ModVege <https://code.europa.eu/agri4cast/modvege>`_ pasture model adapted for use in this project was translated from Java to Python by Y. Chemin of `JRC Ispra <https://joint-research-centre.ec.europa.eu/jrc-sites-across-europe/jrc-ispra-italy_en>`_.
This Python implementation was originally published as public domain software on GitHub under the `Unlicence license <https://github.com/ClimAg/modvege>`_.
The Java model was provided by R. Martin of `INRAE <https://www.inrae.fr/en>`_ UREP Clermont-Ferrand for the original Python implementation.
The original ModVege pasture model was developed by `Jouven et al. <https://doi.org/10.1111/j.1365-2494.2006.00515.x>`_

References
----------

- Jouven, M., Carrère, P., and Baumont, R. (2006a). 'Model predicting dynamics
  of biomass, structure and digestibility of herbage in managed permanent
  pastures. 1. Model description', Grass and Forage Science, vol. 61, no. 2,
  pp. 112-124. DOI: 10.1111/j.1365-2494.2006.00515.x.
- Jouven, M., Carrère, P., and Baumont, R. (2006b). 'Model predicting dynamics
  of biomass, structure and digestibility of herbage in managed permanent
  pastures. 2. Model evaluation', Grass and Forage Science, vol. 61, no. 2,
  pp. 125-133. DOI: 10.1111/j.1365-2494.2006.00517.x.

A full list of references is available here:
https://www.zotero.org/groups/4706660/climag/library

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   parameters/input_parameters
   parameters/input_meteorology
   parameters/variables_time_series
