extract-data-script.R: first download state data from https://redistrictingdatahub.org/ using the tract-level 2020 census data. 
Place in folder called data_files. Run script by calling `extract_data_tract` and inputting the state code (for example North Carolina - `extract_data_tract('nc')`)

This data is ready to be loaded into the k-means.py script

save-to-shape.R: first download shape data from https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2021&layergroup=Census+Tracts 
place in data_files folder. Run script by calling `write_to_sf` using the two letter state code and the FIPS state number (found here: https://www.nrcs.usda.gov/wps/portal/nrcs/detail/?cid=nrcs143_013696) 
(for example North Carolina - `write_to_sf('nc', 37)`)

Once the shape data has been created, use https://mapshaper.org/ to convert into geoJSON for use in https://davesredistricting.org
