from matplotlib import pyplot as plt
from pytrends.request import TrendReq
import numpy as np


def parse_data(data: list, blocks: int, items: int) -> list:
	'''This function parses data from pytrends in order to be used with matplotlib
	
	Parameters:
		data: list=The data to be parsed
		blocks: int=How many segments to split the data into
		items: int=Length of items to be plotted'''

	chunks = np.array_split(data, blocks)
	product = list()

	for chunk in chunks:
		temp = list()

		for index in range(items):
			x = np.average([c[index] for c in chunk])
			temp.append(x)

		product.append(temp)

	# rearranging numbers in separate tuples
	final = list(zip(*product))
	
	return final


def main():
	'''Main function where all the action happens'''

	# setting the `y axis`
	# each key is a different item to be plotted
	# this dict will be passed as **kwargs
	languages = {
		'Python': {
			'color': '#1c8aeb',
			'label': 'Python'
		},
		'Javascript': {
			'color': '#f7d111',
			'label': 'Javascript'
		},
		'Ruby': {
			'color': '#e0115f',
			'label': 'Ruby'
		},
		'PHP': {
			'color': '#796bb0',
			'label': 'PHP'
		}
	}
	
	# setting the `x axis`
	years = range(2014, 2020)

	# requesting data from Google Trends in a timespan of 5 years
	# global, all categories
	pytrends = TrendReq()
	pytrends.build_payload(languages, timeframe='today 5-y')
	data = pytrends.interest_over_time().values

	# parsing data to be used with matplotlib
	product = parse_data(data, blocks=6, items=len(languages))

	# setting some matplotlib configs
	plt.style.use('seaborn-colorblind')
	plt.xlabel('Anos')
	plt.ylabel('Média de pesquisa')
	plt.title('Média de pesquisa de linguagem ao longo dos anos')

	# plotting the items
	for index, language in enumerate(languages):
		plt.plot(years, product[index], **languages[language])

	plt.legend()
	plt.grid(True)

	plt.show()


main()
