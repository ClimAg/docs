# georeference screenshot of the 7-cluster agroclimatic regions map from
# Holden and Brereton (2004)
# Holden, N. M. and Brereton, A. J. (2004). ‘Definition of agroclimatic
# regions in Ireland using hydro-thermal and crop yield data’, Agricultural
# and Forest Meteorology, vol. 122, no. 3, pp. 175–191.
# DOI: 10.1016/j.agrformet.2003.09.010.

gdal_translate -of GTiff -gcp 484.656 117.3 665879 939165 -gcp 489.711 782.459 673316 597501 -gcp 146.949 827.329 490923 570073 -gcp 211.252 335.908 525775 824434 -gcp 230.659 558.076 537836 710807 -gcp 611.761 597.123 734325 692496 -gcp 593.322 370.719 724129 807354 "data/climatic-regions/holden_brereton_2004_regions.png" "/tmp/holden_brereton_2004_regions.png"
gdalwarp -r cubic -order 1 -co COMPRESS=  -t_srs EPSG:2157 "/tmp/holden_brereton_2004_regions.png" "data/climatic-regions/holden_brereton_2004_regions.tif"
