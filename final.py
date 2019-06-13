import csv
import sys
import pandas as pd
import googlemaps
import gmplot


csv.field_size_limit(sys.maxsize)
gmaps_key = googlemaps.Client(key = "AIzaSyB4x9akA4u_lj-f5SlHACWpARLSjIWqvng")

zoom = 8

def get_ticket_data():
	ticket_list = []
	with open('test.csv') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			ticket_dict = {'number': row[0],
					'location': row[11] + ', Los Angeles',
					'fine': row[16]}
			ticket_list.append(ticket_dict)
	return ticket_list


def get_lat_lgt(df, lat_list, lng_list):
	df["lat"] = None
	df["lng"] = None
	
	for i in range(len(df)):
		geocode_result = gmaps_key.geocode(df.loc[i, 'location'])
		try:
			lat = geocode_result[0]["geometry"]["location"]["lat"]
			lng = geocode_result[0]["geometry"]["location"]["lng"]
			df.loc[i, 'lat'] = lat
			df.loc[i, 'lng'] = lng
			lat_list.append(lat)
			lng_list.append(lng)
		except:
			lat = None
			lng = None


if __name__ == '__main__':
	ticket_data = get_ticket_data()
	lat_list = []
	lng_list = []
	
	geocode_result = gmaps_key.geocode('Los Angeles')[0]
	center_lat = geocode_result['geometry']['location']['lat']
	center_lng = geocode_result['geometry']['location']['lng']

	gmap = gmplot.GoogleMapPlotter(center_lat, center_lng, zoom)
	gmap.apikey = "AIzaSyB4x9akA4u_lj-f5SlHACWpARLSjIWqvng"

	df = pd.DataFrame(ticket_data)
	coordinates = get_lat_lgt(df, lat_list, lng_list)

	gmap.heatmap(lat_list, lng_list)
	gmap.scatter(lat_list, lng_list, 'r', marker=False)

	gmap.draw("heatmap.html")


