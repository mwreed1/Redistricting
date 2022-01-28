library(reticulate)
library(here)
# library(broom)
source_python(here("k-means.py"))
source(here("data_cleaning_scripts/extract-data-script.R"))
source(here("data_cleaning_scripts/save-to-shape.R"))



turn_to_df <- function(clusters){
  names <- c("district", "county", "population", "lat", "long")
  df = data.frame()
  data = clusters[[1]]
  for(i in seq(length(data))){
    for(val in data[[i]]){
      df <- rbind(df, list(i, val[1], val[2], val[3], val[4]))
    }
  }
  colnames(df) <- names
  return(df)
}



evaluate <- function(state, num, k, a, b, g, it, t){
  setwd(here())
  data_raw <- extract_data(state)
  data <- read_data(state)
  kmeans_ret <- kmeans(data, as.integer(k), a, b, g, it, t)
  clusters <- kmeans_ret[2]
  df <- turn_to_df(clusters)
  # write_csv(df, here(paste0("data/", state, "_final_tract.csv")))
  # shp <- write_to_sf(state, num)
  return(df)
}

data <- evaluate("az", "04", 9, 11.4, 0.9, 1.6, 100, 0.01)
data %>%
  group_by(district) %>%
  summarize(tot_pop = sum(population)) %>%
  summarize(pop_dif = min(tot_pop)/max(tot_pop)) %>%
  pull()




