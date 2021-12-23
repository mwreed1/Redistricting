import pandas as pd 
tsv_file='../data_files/results_pct_20201103.txt'
csv_table=pd.read_table(tsv_file,sep='\t')
csv_table.to_csv('../data_files/results_pct_20201103.csv',index=False)