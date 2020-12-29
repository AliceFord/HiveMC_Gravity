import requests

r = requests.get('https://api.hivemc.com/v1/player/TechieHelper/GRAV')

mainData = []
for data in r.json()['maprecords']:
	mainData.append('\'' + data + '\'')

mainData.sort()

print('[', end='')
for datapoint in mainData:
	print(datapoint, end=', ')
print(']')