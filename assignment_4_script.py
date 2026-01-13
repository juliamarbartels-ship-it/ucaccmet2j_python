
# This script analyzes rain over time in Seattle. 
# The output is a json file including the station, state, 
# total and relative monthly precipitation, and total and monthly
# yearly precipitation per State

# Part 1: Monthly Precipitation

# import packages
import json

# load in files
# with open("stations.csv", encoding= "utf-8") as file:  
#     stations = file.read()
with open('precipitation.json', encoding='utf-8') as file:
    precipitation_data = json.load(file)

# 0. loop over each station
# 0.1 make dictionary of all stations (key: city, value: station name)
stations_dict = {
    "Cincinnati": {
        "state": "OH",
        "station": "GHCND:USW00093814"}, 
    "Seattle": {
        "state": "WA",
        "station": "GHCND:US1WAKG0038"}, 
    "Maui": {
        "state": "HI",
        "station": "GHCND:USC00513317"},
    "San Diego": {
        "state": "CA",
        "station": "GHCND:US1CASD0032"}
}
print(stations_dict["Cincinnati"])
# initialize dictionary for json output file
precipitation_summary = {}

# 0.2 loop over all cities
for city in stations_dict:
    #access station and state of each city
    city_dict = stations_dict[city]
    station = city_dict["station"]
    state = city_dict["state"]

    # select measurements for Seattle
    station_precipitation = []
    for observation in precipitation_data:
        if observation["station"] == station:
            station_precipitation.append(observation)

    # calculate list of total precipitation per month (plan: iterate over each item, check if it's
    #  in a given month, if yes add, if no add to new month)
    # total_monthly_precipitation = []     # initialize list for monthly precipitation
    # month = 0                            # initialize month so can iterate over 12 months
    # while month < 12:                    # for 12 months
    #     month_precipitation = 0           # initialize variable for total precipitation in a month
    #     month += 1                       
    #     for day in seattle_precipitation:
    #         observation_date = day["date"].split('-')
    #         observation_month = int(observation_date[1])
    #         if observation_month == month:    # if day in current month
    #             month_precipitation += day["value"]    # add day's precipitation to total of that month
    #     total_monthly_precipitation.append(month_precipitation)   # append to list of all months

    # 1. calculate total monthly precipitation in Seattle
    # iterate over observations, check month, and make dictionary with key = month, value = total precipitation
    total_monthly_precipitation = {}
    for observation in station_precipitation:
        observation_date = observation["date"].split('-')
        observation_month = int(observation_date[1])
        if observation_month not in total_monthly_precipitation:
            month_precipitation = 0
        month_precipitation += observation["value"]
        total_monthly_precipitation[observation_month] = month_precipitation

    # convert thisdictionary to a list
    total_monthly_precipitation_list = list(total_monthly_precipitation.values())

    # 2. calculate yearly precipitation using monthly precipitation dictionary
    total_yearly_precipitation = 0
    for observation_month in total_monthly_precipitation:
        month_precipitation = total_monthly_precipitation[observation_month]
        total_yearly_precipitation += month_precipitation

    # 3. calculate relative monthly precipitation (proportion of yearly rain per month)
    relative_monthly_precipitation = {}
    for observation_month in total_monthly_precipitation:
        month_relative_precipitation = total_monthly_precipitation[observation_month]/total_yearly_precipitation
        relative_monthly_precipitation[observation_month] = month_relative_precipitation

    # convert the dictionary to a list
    relative_monthly_precipitation_list = list(relative_monthly_precipitation.values())

    # add this to existing dictionary


    
    # convert into needed format and write into json file
    precipitation_summary[city] = {
    "station": station,
    "state": state,
    "total_monthly_precipitation": total_monthly_precipitation_list,
    "total_yearly_precipitation": total_yearly_precipitation,
    "relative_monthly_precipitation": relative_monthly_precipitation_list,
    "relative_yearly_precipitation": 0
    }

with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(precipitation_summary, file, indent=4)