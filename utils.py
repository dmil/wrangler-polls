import pandas as pd
import numpy as np

def download_pres_results():
	# TODO: read from daily kos
	dkos = pd.read_csv('dailykos_pres_results.csv')

	df = pd.DataFrame(dkos[dkos.columns[0]].iloc[1:])
	df['state'] = df['Year']
	del df['Year']

	dfs = []
	for i in range(1,50,4):
		year_df = dkos[dkos.columns[range(i,i+4)]]
		year = int(year_df.columns[0])
		year_df = year_df.iloc[1:]
		year_df.columns = ['DEM','REP','PVI','VAL']
		year_df = year_df.fillna('')
		year_df['year'] = year
		year_df['PVI'] = year_df['PVI'].astype(str) + year_df['VAL'].astype(str)
		del year_df['VAL']
		year_df['state'] = df['state']
		dfs.append(year_df)

	results_df = pd.concat(dfs)
	results_df['DEM'] = pd.to_numeric(results_df['DEM'], downcast='float')
	results_df['REP'] = pd.to_numeric(results_df['REP'], downcast='float')
	results_df['d_margin'] = results_df['DEM'] - results_df['REP']
	results_df.to_csv('pres_results.csv', index=False)
	return results_df