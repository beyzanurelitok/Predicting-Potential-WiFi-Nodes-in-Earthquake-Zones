import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import random
import numpy as np
from deap import base, creator, tools, algorithms
from shapely.geometry import Point
from geopy.distance import geodesic

# Prevent memory leak
os.environ['OMP_NUM_THREADS'] = '2'

# Load earthquake data
file_path = 'C:/anaconda/envs/Staj12/earthquakeData/bdtim_mt.csv'
earthquakeData = pd.read_csv(file_path, delimiter=';', usecols=['Longitude', 'Latitude'])

# Convert earthquake data to numpy array (Longitude, Latitude)
data = earthquakeData[['Longitude', 'Latitude']].values

# Load Turkey's provinces shapefile
shapefile_path_provinces = 'C:/anaconda/envs/Staj12/ShapeFileTR/gadm41_TUR_1.shp'  # Provincial boundaries
trData_provinces = gpd.read_file(shapefile_path_provinces)

# Set CRS for the shapefile
trData_provinces.set_crs(epsg=4326, inplace=True)

# Determine the number of WiFi points the user wants to select
num_clusters = 2  # Find the nearest 2 WiFi points according to the user

# Ask the user for their coordinates
user_longitude = float(input("Enter your Longitude (in EPSG:4326 format): "))
user_latitude = float(input("Enter your Latitude (in EPSG:4326 format): "))
user_point = np.array([user_longitude, user_latitude])

# Find the nearest 5 earthquake data points to the user
def distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))

distances_to_user = np.array([distance(user_point, point) for point in data])
nearest_indices = distances_to_user.argsort()[:5]
user_nearest_data = data[nearest_indices]

# Define the fitness function
def fitness(individual):
    centroids = np.array(individual).reshape(num_clusters, 2)
    total_distance = 0
    penalty = 0
    for point in user_nearest_data:
        total_distance += min(distance(point, centroid) for centroid in centroids)
    for centroid in centroids:
        if distance(user_point, centroid) > 0.09:  # 10 km = 0.09 degree approx. for latitude
            penalty += 1000
    return total_distance + penalty,

# Check if the classes are already created
if not hasattr(creator, "FitnessMin"):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_long", random.uniform, user_point[0] - 0.12, user_point[0] + 0.12)
toolbox.register("attr_lat", random.uniform, user_point[1] - 0.09, user_point[1] + 0.09)
toolbox.register("individual", tools.initCycle, creator.Individual, 
                 (toolbox.attr_long, toolbox.attr_lat), n=num_clusters)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.01, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", fitness)

# Create initial population
population = toolbox.population(n=200)

# Apply the genetic algorithm
algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=5,  # Genetic algorithm probabilities 
                    stats=None, halloffame=None, verbose=True)         #for crossover and mutation

# Extracting the best solution
best_individual = tools.selBest(population, 1)[0]
wifi_centroids = np.array(best_individual).reshape(num_clusters, 2)

# Convert WiFi centroids to GeoDataFrame
wifi_gdf = gpd.GeoDataFrame(
    wifi_centroids, columns=['Longitude', 'Latitude'],
    geometry=gpd.points_from_xy(wifi_centroids[:, 0], wifi_centroids[:, 1])
)

# Set CRS for WiFi data
wifi_gdf.set_crs(epsg=4326, inplace=True)

# Check if WiFi locations are within Turkey's boundaries
wifi_within_boundaries = wifi_gdf.within(trData_provinces.unary_union)
wifi_gdf = wifi_gdf[wifi_within_boundaries]

# Calculate the distance between the user's point and WiFi points
wifi_points = wifi_centroids
distances = [geodesic((user_latitude, user_longitude), (lat, lon)).km for lon, lat in wifi_points]

# Print the results
for i, dist in enumerate(distances, 1):
    print(f"Distance between WN{i} and user: {dist:.2f} km")

# Check if they are within 10 km
for i, dist in enumerate(distances, 1):
    if dist <= 10:
        print(f"WN{i} is within 10 km of the user.")
    else:
        print(f"WN{i} is outside of 10 km from the user.")

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))
earthquake_gdf = gpd.GeoDataFrame(
    earthquakeData, geometry=gpd.points_from_xy(earthquakeData['Longitude'], earthquakeData['Latitude']))
earthquake_gdf.set_crs(epsg=4326, inplace=True)
earthquake_gdf.plot(ax=ax, color='red', markersize=5, alpha=0.5, label='Earthquake Data')

# User point
user_gdf = gpd.GeoDataFrame(
    {'Longitude': [user_longitude], 'Latitude': [user_latitude]},
    geometry=[Point(user_longitude, user_latitude)]
)
user_gdf.set_crs(epsg=4326, inplace=True)
user_gdf.plot(ax=ax, color='green', markersize=100, marker='o', alpha=0.7, label='User Location')

# Proposed WiFi points
wifi_gdf.plot(ax=ax, color='purple', markersize=100, marker='X', alpha=0.7, label='Proposed WiFi Points')

# Annotating WiFi points
for i, (x, y) in enumerate(zip(wifi_gdf['Longitude'], wifi_gdf['Latitude']), 1):
    ax.annotate(f'WN{i}', xy=(x, y), xytext=(5, 5), textcoords='offset points')

# Add the list of WiFi points with their coordinates in the bottom right corner
annot_text = "\n".join([f"WN{i} = ({lon}, {lat})" for i, (lon, lat) in enumerate(zip(wifi_gdf['Longitude'], wifi_gdf['Latitude']), 1)])
plt.text(0.50, 0.05, annot_text, transform=ax.transAxes, verticalalignment='bottom', horizontalalignment='left', fontsize=10, bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))

plt.title('Proposed WiFi Points and Earthquake Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()

print("Done")

