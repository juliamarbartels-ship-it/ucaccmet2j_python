
# This script analyzes rain over time in Seattle. The output is a json file including the station, state, 
# total and relative monthly precipitation, and total and monthly yearly precipitation per State

# import packages
import json

# load in files
with open('precipitation.json', encoding='utf-8') as file:
    precipitation_data = json.load(file)
with open("stations.csv", encoding= "utf-8") as file:  
    first_line = file.readline()        # disregard line of column names
    stations = file.readlines()         

# 1. make dictionary of stations to summarize results
stations_dict = {}
for line in stations:      # for each line, add information into dictionary so key = city, value = dictionary (with keys for station and state)
    city, state, station = line.split(",")
    stations_dict[city] = {"state": state, "station": station.strip()}


# 2. loop over all cities to analyze each
for city in stations_dict:

    total_precipitation = 0  # for step 2.6: initialize total precipitation across all cities 

    # 2.1 access station and state of current city
    city_dict = stations_dict[city]
    station = city_dict["station"]
    state = city_dict["state"]

    # 2.2 select measurements for current city
    city_precipitation = []
    for observation in precipitation_data:
        if observation["station"] == station:
            city_precipitation.append(observation)
        
        # for step 2.6: calculate total precipitation across all cities
        total_precipitation += observation["value"]

    # 2.3 calculate total monthly precipitation 
    # make dictionary with key = month, value = total precipitation
    total_monthly_precipitation = {}                         # initialize dictionary
    for observation in city_precipitation:                   # each observation contains station, date, precipitation
        observation_date = observation["date"].split('-')
        observation_month = int(observation_date[1])         # access month per observation
        if observation_month not in total_monthly_precipitation:
            month_precipitation = 0 
        month_precipitation += observation["value"]          # add up precipitation per month
        total_monthly_precipitation[observation_month] = month_precipitation      # append to dictionary

    # convert dictionary to a list
    total_monthly_precipitation_list = list(total_monthly_precipitation.values())

    # 2.4 calculate yearly precipitation 
    total_yearly_precipitation = 0
    for observation_month in total_monthly_precipitation:        # loop through monthly precipitation dictionary and add values
        month_precipitation = total_monthly_precipitation[observation_month]
        total_yearly_precipitation += month_precipitation

    # 2.5 calculate relative monthly precipitation (proportion of yearly rain per month)
    relative_monthly_precipitation = {}
    for observation_month in total_monthly_precipitation:        # loop through monthly precipitation dictionary 
        month_relative_precipitation = total_monthly_precipitation[observation_month]/total_yearly_precipitation  # divide by yearly precipitation
        relative_monthly_precipitation[observation_month] = month_relative_precipitation

    # convert the dictionary to a list
    relative_monthly_precipitation_list = list(relative_monthly_precipitation.values())

    # 2.6 calculate relative yearly precipitation
    relative_yearly_precipitation = total_yearly_precipitation/total_precipitation

    # 2.7 add results to existing dictionary
    stations_dict[city] = {
    "station": station,
    "state": state,
    "total_monthly_precipitation": total_monthly_precipitation_list,
    "total_yearly_precipitation": total_yearly_precipitation,
    "relative_monthly_precipitation": relative_monthly_precipitation_list,
    "relative_yearly_precipitation": relative_yearly_precipitation
    }

# 3. write results to json file
with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(stations_dict, file, indent=4)