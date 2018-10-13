import io
import us
import csv
import itertools
import requests
import pandas as pd
import numpy as np

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

# Sheet 1: 29622862
# Sheet 2: 1024689221

response = requests.get("https://docs.google.com/spreadsheets/d/1D-edaVHTnZNhVU840EPUhz3Cgd7m39Urx7HM8Pq6Pus/export?format=csv&id=1D-edaVHTnZNhVU840EPUhz3Cgd7m39Urx7HM8Pq6Pus&gid=1024689221")

output = []

with io.StringIO(response.text) as f:
	reader = csv.reader(f)
	
	header1 = next(reader)

	year_start_indicies = []
	for i, col in enumerate(header1):
		# print(i, repr(col))
		if col == "1952": break
		if col.startswith('20') or col.startswith('19'):
			year_start_indicies.append((col, i,))

	# print(year_start_indicies)

	header2 = next(reader)

	for row in reader:

		# end of states, starts regions next
		if row[0] == '': break

		for ((year, index), (next_year, next_index)) in pairwise(year_start_indicies):
			if row[0] == 'Nationwide':
				state = 'US'
			elif row[0] == 'Washington DC':
				state = 'DC'
			else:
				state = us.states.lookup(row[0]).abbr
			out = {
				'year': int(year), 
				'state': state,
				'dem': row[index],
				'rep': row[index+1],
				# 'pvi': row[next_index-2] + row[next_index-1],
				}
			# print(out)
			output.append(out)

output = sorted(output, key=lambda x: (-x['year'], x['state']))

with open('pres_results.csv', 'w') as f: 
	writer = csv.DictWriter(f, fieldnames=output[0].keys())
	writer.writeheader()
	writer.writerows(output)
