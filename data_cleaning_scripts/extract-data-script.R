library(tidyverse)
library(sf)
library(janitor)
library(here)

extract_data_block <- function(state){
  data_raw <- read_csv(here(paste0("data_files/", state, "_pl2020_b/", state, "_pl2020_b.csv")))
  
  data <- data_raw %>%
    clean_names() %>%
    mutate(pop100 = as.numeric(pop100)) %>%
    filter(pop100 > 0) %>%
    as_tibble() %>%
    select(geoid, county, pop100, intptlat, intptlon)
  
  write_csv(data, paste0("data/", state, "_input.csv"))
  
}

extract_data <- function(state){
  # download data from https://redistrictingdatahub.org/data/download-data/#state-menu
  data_raw <- read_csv(
    here(paste0("data_files/", state, "_pl2020_t/", state, "_pl2020_t.csv")),
    show_col_types = FALSE
    )
  
  data <- data_raw %>%
    clean_names() %>%
    mutate(tract_new = paste0(county, tract)) %>%
    group_by(tract_new) %>%
    summarize(
      county = max(county),
      pop100 = sum(pop100),
      intptlat = mean(intptlat),
      intptlon = mean(intptlon),
      tract = max(tract),
      .groups = "drop"
    ) %>%
    filter(pop100 > 0)
  
  write_csv(data, here(paste0("data/", state, "_input_t.csv")))
  
}

# data <- extract_data('tx')
