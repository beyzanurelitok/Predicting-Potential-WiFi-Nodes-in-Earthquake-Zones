# Determining Potential WiFi Points During Earthquakes

This project aims to determine potential WiFi points during earthquakes by using earthquake data obtained from Kandilli Observatory. In the event of a natural disaster like an earthquake, identifying nearby WiFi points for users could be crucial for maintaining communication.

## Project Purpose

In disaster scenarios, especially earthquakes, communication networks are often disrupted. This project identifies potential WiFi points around the user's location based on earthquake data and calculates the proximity of these points to the user. 

## Features

- Dataset: Earthquake data from Kandilli Observatory.
- Geospatial Data: Shapefile containing Turkey’s provincial boundaries.
- Genetic Algorithm: Finds optimal WiFi points.
- Visualization: Displays earthquake data and WiFi points on a map.
- Distance Calculation: Uses Geopy to calculate distance between user and WiFi points.

## How It Works

1. The user inputs their geographical coordinates (longitude and latitude).
2. The 5 nearest earthquake data points to the user’s location are identified.
3. A genetic algorithm is used to find the best potential WiFi locations.
4. The distances between the user’s location and the WiFi points are calculated, and the points within 10 km are highlighted.
5. All results are visualized on a map.

## Requirements

- Python 3.x
- Pandas
- GeoPandas
- DEAP
- Geopy
- Matplotlib
- Shapely

## Usage

1. Add the earthquake data and shapefile to the project directory.
2. Run the Python script and input your coordinates.
3. View the results on the map and see the distances to the WiFi points.
