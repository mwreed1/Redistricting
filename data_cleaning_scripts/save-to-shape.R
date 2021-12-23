library(tidyverse)
library(sf)
library(here)
library(janitor)
library(geojsonio)
library(rmapshaper)
library(rjson)

write_to_sf <- function(state, num){
  # download data from https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2021&layergroup=Census+Tracts
  tract_raw <- read_csv(here(paste0("data/", state, "_final_tract.csv")))
  input <- read_csv(here(paste0("data/", state, "_input_t.csv")))
  shape <- st_read(here(paste0("data_files/tl_2021_", num, "_tract/tl_2021_", num, "_tract.shp")))
  
  
  tract <- tract_raw %>%
    clean_names() %>%
    inner_join(input, by = c(lat = 'intptlat',  long = 'intptlon')) %>%
    select(district, county.x, tract, population) %>%
    rename(c("county" = county.x)) %>%
    mutate(
      county = as.numeric(county),
      tract = as.numeric(tract)
    )
  
  state_data <- shape %>%
    clean_names() %>%
    mutate(
      county = as.numeric(countyfp),
      tract = as.numeric(tractce)
    ) %>%
    merge(tract, by.x = c("county", "tract"), by.y = c("county", "tract")) %>%
    select(countyfp, tractce, district, population, geometry)
  
  shape <- state_data %>%
    group_by(district) %>%
    summarize() %>%
    st_cast("MULTIPOLYGON")
  
  path <- here(paste0("data/", state, "_final_shape"))
  shape <- st_as_sf(shape)
  json_st <- geojson_json(shape, geometry = "polygon")
  write(json_st, paste0(path, ".json"))
  return(json_st)
}


tx <- write_to_sf("tx", "48")

