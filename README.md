# Determining Potential WiFi Points During Earthquakes
This project aims to determine potential WiFi points during earthquakes by using earthquake data obtained from Kandilli Observatory. In the event of a natural disaster like an earthquake, identifying nearby WiFi points for users could be crucial for maintaining communication.

# Project Purpose
In disaster scenarios, especially earthquakes, communication networks are often disrupted. This project identifies potential WiFi points around the user's location based on earthquake data and calculates the proximity of these points to the user.

# Features
Dataset: The project utilizes earthquake data retrieved from Kandilli Observatory.
Geospatial Data: A shapefile containing Turkey’s provincial boundaries is used to check if the WiFi points remain within the country’s borders.
Genetic Algorithm: A genetic algorithm is applied to find the optimal WiFi points based on proximity to earthquake data.
Visualization with Matplotlib: The nearest WiFi points and earthquake data are visualized on a map.
Geopy and Shapely Libraries: Geopy is used to calculate the distance between the user’s location and the nearest WiFi points.
How It Works
The user inputs their geographical coordinates (longitude and latitude).
The 5 nearest earthquake data points to the user’s location are identified.
A genetic algorithm is used to find the best potential WiFi locations.
The distances between the user’s location and the WiFi points are calculated, and the points within 10 km are highlighted.
All results are visualized on a map.

# Requirements
Python 3.x
Pandas
GeoPandas
DEAP
Geopy
Matplotlib
Shapely

# Usage
Add the earthquake data and shapefile to the project directory.
Run the Python script and input your coordinates.
View the results on the map and see the distances to the WiFi points.
