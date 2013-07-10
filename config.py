places = {
          'Melbourne': {'coords': [114.18, -38.19, 145.68, -37.52],
                        'weather_sources': [], 'country': 'Australia'},
          'Brisbane': {'coords': [152.9075, -27.705415, 153.283782, -27.29613],
                       'weather_sources': [], 'country': 'Australia'},
          'Adelaide': {'coords': [138.29019, -35.33081, 138.776336, -34.69759],
                       'weather_sources': [], 'country': 'Australia'},
          'Sydney': {'coords': [150.583892, -34.083375, 151.37903,-33.611188],
                     'weather_sources': [], 'country': 'Australia'},
          'Perth': {'coords': [115.71054, -32.466902, 116.062102, -31.656888],
                    'weather_sources': [], 'country': 'Australia'},
          'Darwin': {'coords': [130.78389, -12.531775, 131.046188, -12.360125],
                     'weather_sources': [], 'country': 'Australia'},
          'Canberra': {'coords': [148.93605, -35.47689, 149.22787, -35.158653],
                     'weather_sources': [], 'country': 'Australia'},
          'Berlin': {'coords': [13.344269, 52.486125, 13.480225, 52.549219],
                     'weather_sources': [], 'country': 'Germany'},
          'London': {'coords': [-0.69, 51.28, 0.35, 51.77],
                     'weather_sources': [], 'country': 'UK'},
          'New York': {'coords': [-74, 40, -73, 41],
                       'weather_sources': [], 'country': 'USA'},
          'San Francisco': {'coords': [-122.75, 36.8, -121.75, 37.8],
                            'weather_sources': [], 'country': 'USA'}
          }

for l in places:
    box = places[l]['coords']
    loose_box = []
    for b in box[:2]:
        if b < 0:
            loose_box.append(b * 1.05)
        else:
            loose_box.append(b * 0.95)

    for b in box[2:]:
        if b < 0:
            loose_box.append(b * 0.95)
        else:
            loose_box.append(b * 1.05)
    places[l]['loose_box'] = loose_box

loca_time_api = 'get local time from here'
languages = ['en', 'de']
dictionary = 'dictionary_file_name'
db_name = 'tweet_weather'







