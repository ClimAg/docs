Input parameters
================

.. note::
   This page is still being worked on, so there may be some incomplete items.

See Tables 2 and 3 in [#Jouven]_ for estimates of the input
parameters. Temperate grasses have been classified into four groups based
on their functional traits. The four groups have been parameterised for
the temperate, mountainous Auvergne region in France.

Functional group A is relevant to Ireland: Species found in fertile sites,
adapted to frequent defoliation,
which has high specific leaf area, high digestibility, short leaf lifespan,
and early reproductive growth and flowering.
An example is perennial ryegrass (*Lolium perenne*).

The nitrogen nutritional index (NNI) is site-specific.

Variables
---------

These vary spatially.

.. csv-table::
   :header: Variable, Description, Units
   :delim: ;

   bm_gv; Initial biomass of GV; kg DM ha⁻¹
   bm_gr; Initial biomass of GR; kg DM ha⁻¹
   bm_dv; Initial biomass of DV; kg DM ha⁻¹
   bm_dr; Initial biomass of DR; kg DM ha⁻¹
   age_gv; Initial GV age; °C d
   age_gr; Initial GR age; °C d
   age_dv; Initial DV age; °C d
   age_dr; Initial DR age; °C d
   ni; Nitrogen nutritional index :math:`(NNI)`
   whc; Soil water-holding capacity :math:`(WHC)`; mm
   sr; Stocking rate
   st_h1; Sum of temperatures at the beginning of the harvest; °C d
   st_g2; Sum of temperatures at the end of the grazing season; °C d
   st_1; Sum of temperatures at the beginning of the reproductive period; °C d
   st_2; Sum of temperatures at the end of the reproductive period; °C d

Constants
---------

.. csv-table::
   :header: Constant, Description, Value, Units
   :delim: ;

   sla; Specific leaf area :math:`(SLA)`; 0.033; m² g⁻¹
   pct_lam; Percentage of laminae in the green vegetative compartment :math:`(\%LAM)`; 0.68
   max_sea; Maximum seasonal effect :math:`(maxSEA)`; 1.20
   min_sea; Minimum seasonal effect :math:`(minSEA)`; 0.80
   lls; Leaf lifespan :math:`(LLS)`; 500; °C d
   bd_gv; Bulk density of the green vegetative compartment :math:`(BD_{GV})`; 850; g DM m⁻³
   bd_dv; Bulk density of the dead vegetative compartment :math:`(BD_{DV})`; 500; g DM m⁻³
   bd_gr; Bulk density of the green reproductive compartment :math:`(BD_{GR})`; 300; g DM m⁻³
   bd_dr; Bulk density of the dead reproductive compartment :math:`(BD_{DR})`; 150; g DM m⁻³
   sigma_gv; Rate of biomass loss with respiration for the green vegetative compartment :math:`(\sigma_{GV})`; 0.4
   sigma_gr; Rate of biomass loss with respiration for the green reproductive compartment :math:`(\sigma_{GR})`; 0.2
   t_0; Minimum temperature for growth :math:`(T_0)`; 4; °C
   t_1; Minimum temperature for optimal growth :math:`(T_1)`; 10; °C
   t_2; Maximum temperature for optimal growth :math:`(T_2)`; 20; °C
   t_max; Maximum temperature for growth :math:`(T_{max})`; 40; °C
   k_gv; Basic senescence rate for the green vegetative compartment :math:`(K_{GV})`; 0.002
   k_gr; Basic senescence rate for the green reproductive compartment :math:`(K_{GR})`; 0.001
   kl_dv; Basic abscission rate for the dead vegetative compartment :math:`(Kl_{DV})`; 0.001
   kl_dr; Basic abscission rate for the dead reproductive compartment :math:`(Kl_{DR})`; 0.0005
   rue_max; Maximum radiation use efficiency :math:`(RUE_{max})`; 3; g DM MJ⁻¹
   max_omd_gv; Maximum organic matter digestibility of the green vegetative compartment :math:`(maxOMD_{GV})`; 0.90
   min_omd_gv; Minimum organic matter digestibility of the green vegetative compartment :math:`(minOMD_{GV})`; 0.75
   max_omd_gr; Maximum organic matter digestibility of the green reproductive compartment :math:`(maxOMD_{GR})`; 0.90
   min_omd_gr; Minimum organic matter digestibility of the green reproductive compartment :math:`(minOMD_{GR})`; 0.65
   omd_dv; Organic matter digestibility for the dead vegetative compartment :math:`(OMD_{DV})`; 0.45
   omd_dr; Organic matter digestibility for the dead reproductive compartment :math:`(OMD_{DR})`; 0.40
   h_grass; Minimum residual grass height after cutting. See sec. "Harvested biomass" in [#Jouven]_; 0.05; m
   i_bm_lu; Maximum biomass ingestion per livestock unit; 13; kg DM LU⁻¹

References
----------

.. [#Jouven] Jouven, M., Carrère, P., and Baumont, R. (2006). ‘Model
   predicting dynamics of biomass, structure and digestibility of herbage in
   managed permanent pastures. 1. Model description’, Grass and Forage
   Science, 61(2), pp. 112–124.
   https://doi.org/10.1111/j.1365-2494.2006.00515.x.
