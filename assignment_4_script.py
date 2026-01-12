
# This script analyzes rain over time in Seattle. 
# The output is a json file including the station, state, 
# total and relative monthly precipitation, and total and monthly
# yearly precipitation per State

# Part 1: Monthly Precipitation

# import packages
import json

# load in files
with open("stations.csv", encoding= "utf-8") as file:  
    stations = file.read()
with open('precipitation.json', encoding='utf-8') as file:
    precipitation_data = json.load(file)

# select measurements for Seattle
seattle_precipitation = []
for day in precipitation_data:
    if day["station"] == "GHCND:US1WAKG0038":
        seattle_precipitation.append(day)

# calculate list of total precipitation per month (plan: iterate over each item, check if it's
#  in a given month, if yes add, if no add to new month)
total_monthly_precipitation = []     # initialize list for monthly precipitation
month = 0                            # initialize month so can iterate over 12 months
month_precipitation = 0              # initialize variable for total precipitation in a month
while month < 13:                    # for 12 months
    month += 1                       
    for day in seattle_precipitation:
        date = day["date"]
        if date.startswith(f"2010-0{month}"):      # if day in current month
            month_precipitation += day["value"]    # add day's precipitation to total of that month
    total_monthly_precipitation.append(month_precipitation)   # append to list of all months
print(total_monthly_precipitation)

# write into json file
with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(total_monthly_precipitation, file, indent=4)