import csv
import os
import re
from math import radians, sin, cos, sqrt, atan2
from io import StringIO
import numpy as np
import pandas as pd

def haversine(lat1, lon1, lat2, lon2):
    R = 3956  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return int(round(R * c, 0))

def clean_file(input_path):
    """
    Reads the contents of the file at input_path,
    replaces multiple consecutive tabs with a single tab,
    and returns the cleaned content as a string.
    """
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    cleaned_lines = [re.sub(r'\t+', '\t', line.strip()) for line in lines]
    return "\n".join(cleaned_lines)

def scrape_dat_files(input_dir):
    # Define paths for the input files
    airports_path = os.path.join(input_dir, 'airports.dat')
    routes_path = os.path.join(input_dir, 'routes.dat')

    # Clean the airports data by calling a helper function that removes unwanted characters
    cleaned_airports_data = clean_file(airports_path)

    # Use StringIO to read the cleaned data into a DataFrame (a two dimensional array) without saving to a file
    airports_df = pd.read_csv(StringIO(cleaned_airports_data), sep='\t', dtype=str)
    airports_df[['latitude', 'longitude']] = airports_df[['latitude', 'longitude']].astype(float)

    # Load the routes data directly from the file
    routes_df = pd.read_csv(routes_path, sep='\t', dtype=str)

    # Merge both dataframes using the airport IDs to get one complete dataframe containing all the information
    merged = routes_df.merge(airports_df, left_on='from', right_on='airport-id') \
                      .merge(airports_df, left_on='to', right_on='airport-id', suffixes=('_src', '_dst'))

    # Using the merged DataFrame, calculate the distance between the source and destination airports
    # The haversine function is used to calculate the distance based on latitude and longitude
    merged['distance'] = merged.apply(lambda row: haversine(
        row['latitude_src'], row['longitude_src'],
        row['latitude_dst'], row['longitude_dst']), axis=1)

    # Prepare nodes and edges DataFrames for output
    # Nodes DataFrame contains unique airports with their IDs and names
    # Edges DataFrame contains unique routes with distances
    nodes_df = airports_df[['airport-id', 'airport-name']].drop_duplicates()
    edges_df = merged[['from', 'to', 'distance']].rename(columns={
        'from': 'endpoint1', 'to': 'endpoint2'
    })

    # Clean the edges DataFrame by removing duplicates, ensure data integrity and correct types
    edges_df.drop_duplicates(inplace=True)
    edges_df = edges_df[edges_df['endpoint1'] != edges_df['endpoint2']]
    edges_df = edges_df[edges_df['distance'] > 0]
    edges_df['distance'] = edges_df['distance'].astype(int)

    # Normalize the endpoints to ensure that (A, B) and (B, A) are treated as the same edge
    edges_df['norm_endpoints'] = np.where(
    edges_df['endpoint1'] <= edges_df['endpoint2'],
    edges_df['endpoint1'] + "_" + edges_df['endpoint2'],
    edges_df['endpoint2'] + "_" + edges_df['endpoint1']
)

    # Drop duplicates based on the normalized endpoints and remove the temporary column
    edges_df.drop_duplicates(subset=['norm_endpoints'], inplace=True)
    edges_df.drop(columns=['norm_endpoints'], inplace=True)


    return nodes_df, edges_df

def write_to_txt(nodes_df, edges_df, output_dir):
    nodes_df.to_csv(os.path.join(output_dir, 'nodes.txt'), index=False, header=False)
    edges_df.to_csv(os.path.join(output_dir, 'edges.txt'), index=False, header=False)

def main():
    input_dir = 'input_data'
    output_dir = 'cleaned_data'
    print("Starting the scraping process...")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Scrape data (cleaning is done in memory, so no extra file is produced)
    nodes_df, edges_df = scrape_dat_files(input_dir)
    print("Data scraped successfully.")

    # Print the first few rows of the dataframes for verification
    print("Nodes DataFrame:")
    print(nodes_df.head())
    print("Edges DataFrame:")
    print(edges_df.head())

    # Write nodes and edges to text files
    write_to_txt(nodes_df, edges_df, output_dir)

if __name__ == "__main__":
    main()
