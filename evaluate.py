#%% set up
from operator import index
import pandas as pd
import numpy as np
from pandas.core.reshape.merge import _MergeOperation
from seaborn.external.husl import max_chroma

path = 'data/nc_final_geo_votes.csv'
df = pd.read_csv(path, index_col=0)

#%% federal population metrics
def is_equal_pop_fed():
    district_pop_sum_df = df.groupby('district')['population'].sum()
    min_pop = district_pop_sum_df.min()
    max_pop = district_pop_sum_df.max()
    ratio = min_pop/max_pop
    return ratio >= 0.90, ratio
pop_federal, pop_federal_ratio = is_equal_pop_fed()

#%% nc population metrics
def is_equal_pop_nc():
    district_pop_sum_df = df.groupby('district')['population'].sum()
    total_pop = district_pop_sum_df.sum()
    max_diff = -1
    min_diff = 1
    avg_diff = 0
    for pop in district_pop_sum_df:
        percent_diff = min(total_pop, pop)/max(total_pop, pop)
        if percent_diff > max_diff: max_diff = percent_diff
        if percent_diff < min_diff: min_diff = percent_diff
        avg_diff += percent_diff/len(district_pop_sum_df)
    return max_diff <= 0.05, avg_diff, min_diff, max_diff
pop_nc, pop_nc_avg_diff, pop_nc_min_diff, pop_nc_max_diff = is_equal_pop_nc()

#%% county splitting metrics - districts/counties
def county_split_count():
    county_split_df = df.groupby('county')['district'].unique()
    avg_count = 0
    min_count = 100
    max_count = -1
    for i in range(len(county_split_df)):
        district_count = len(county_split_df.iloc[i])
        avg_count += district_count/len(county_split_df)
        if district_count < min_count: min_count = district_count
        if district_count > max_count: max_count = district_count
    return avg_count, min_count, max_count
avg_county_split, min_county_split, max_county_split = county_split_count()


#%% competitiveness metrics
def competitiveness_lean():
    county_lean = df.groupby('district')['lean'].sum()
    return county_lean

def competitiveness_rawish():
    county_raw_votes = df.groupby('district')['rep_votes'].sum() - df.groupby('district')['dem_votes'].sum()
    return county_raw_votes

print(f'REPORT FOR {path}')
print(f'FEDERAL POPULATION EQUALITY: {pop_federal}, with {pop_federal_ratio} min:max')
print(f'NC POPULATION EQUAL: {pop_nc}, with average {pop_nc_avg_diff}, min {pop_nc_min_diff}, max {pop_nc_max_diff} % difference')
print(f'DISTRICTS PER COUNTY: average {avg_county_split}, with min {min_county_split}, max {max_county_split}')