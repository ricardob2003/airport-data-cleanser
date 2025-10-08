# Airport Network Data Processor

A Python script that transforms raw airport and route data into a clean, structured network representation suitable for graph analysis and visualization.

## Overview

This project processes airport and flight route data to create a mathematical representation of the global airport network. It takes raw data files containing airport information and flight routes, then generates two output files representing nodes (airports) and edges (routes with distances) in a graph network format.

## Features

-   **Data Cleaning**: Removes inconsistent tab formatting and standardizes data structure
-   **Geographic Distance Calculation**: Uses the Haversine formula to calculate great-circle distances between airports
-   **Graph Network Creation**: Generates nodes and edges for network analysis
-   **Data Normalization**: Removes duplicates and ensures data integrity
-   **Output Generation**: Exports clean, structured data for further analysis

## Input Data

The script expects two input files in the `input_data/` directory:

-   `airports.dat`: Contains airport information (ID, name, latitude, longitude, etc.)
-   `routes.dat`: Contains flight route information (source airport, destination airport, etc.)

## Output Data

The script generates two files in the `cleaned_data/` directory:

### nodes.txt

Contains unique airports represented as nodes in the network:

```
airport-id,airport-name
```

### edges.txt

Contains flight routes with calculated distances between airports:

```
source-airport,destination-airport,distance-in-miles
```

**Example:**

```
MAO,CIZ,225
JFK,LAX,2475
LHR,CDG,214
```

Each line represents a connection between two airports (nodes) where:

-   **First value**: Source airport code
-   **Second value**: Destination airport code
-   **Third value**: Distance in miles between the airports (calculated using the Haversine formula)

The distance represents the shortest path between two airports "as the crow flies" - the great-circle distance across the Earth's surface.

## How It Works

1. **Data Cleaning**: Reads and cleans the input files by normalizing tab separators
2. **Data Merging**: Combines airport and route data using airport IDs
3. **Distance Calculation**: Calculates distances between airports using the Haversine formula:
    - Uses Earth's radius (3,956 miles)
    - Converts coordinates to radians
    - Applies the Haversine formula for great-circle distance
4. **Network Processing**:
    - Creates nodes from unique airports
    - Creates edges from routes with calculated distances
    - Removes duplicate routes and self-referencing connections
    - Normalizes bidirectional routes (A→B and B→A become one edge)
    - Filters out invalid routes (zero distance or same source/destination)

## Installation

1. Clone or download this repository
2. Install required dependencies:
    ```bash
    pip install pandas numpy
    ```

## Usage

1. Place your input data files in the `input_data/` directory:

    - `airports.dat`
    - `routes.dat`

2. Run the script:

    ```bash
    python scraper.py
    ```

3. The processed data will be saved in the `cleaned_data/` directory:
    - `nodes.txt`
    - `edges.txt`

## Dependencies

-   Python 3.x
-   pandas
-   numpy

## Use Cases

This processed data is ideal for:

-   **Flight Network Analysis**: Analyze connectivity patterns in global aviation
-   **Graph Theory Applications**: Study network properties and algorithms
-   **Route Optimization**: Find shortest paths and optimize flight routes
-   **Geographic Network Visualization**: Create maps and visualizations of airport networks
-   **Transportation Research**: Study air transportation networks and hub analysis

## Data Format Details

The output files use comma-separated values (CSV) format without headers, making them easy to import into various analysis tools, databases, or visualization software.

The distance calculations use the Haversine formula, which provides accurate great-circle distances between any two points on Earth given their latitude and longitude coordinates.

## File Structure

```
airport-cleaner/
├── input_data/
│   ├── airports.dat
│   └── routes.dat
├── cleaned_data/
│   ├── nodes.txt
│   └── edges.txt
├── scraper.py
├── Pipfile
├── Pipfile.lock
└── README.md
```
