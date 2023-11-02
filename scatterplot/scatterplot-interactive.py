# bokeh serve scatterplot.py
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Button, LabelSet, HoverTool
from bokeh.models import Slider, ColumnDataSource, FactorRange, Select
from bokeh.layouts import column
import random

import pandas as pd
import numpy as np
from dominance import compare_min 
from nds import nds 
import json

method = 'Distance'
selection_type = 'Interactive'

def update_method(attr, old, new):
    global method
    clear_points()
    method = method_dropdown.value

def update_selection_type(attr, old, new):
    global selection_type 
    clear_points()
    selection_type = selection_type_dropdown.value


def distance_method(df, x, y):
    # Normalization procedure:
    # Step 1: You have the obtained ND set F. Find F_i^min and F_i^max for
    # each obj i from the set. Normalize each F_i as follows:
    # NF_i = (F_i - F_i^min)/(F_i^Max - F_i^min), for both objs: i=1,2
    min_cost = df['Cost'].min()
    max_cost = df['Cost'].max()
    
    min_loads = df['Loads'].min()
    max_loads = df['Loads'].max()
    
    # Perform Min-Max scaling for the "Cost" and "Loads" columns
    df['CostNorm'] = (df['Cost'] - min_cost) / (max_cost - min_cost)
    df['LoadsNorm'] = (df['Loads'] - min_loads) / (max_loads - min_loads)

    # Step 2: Also normalize the reference point R (supplied by DM) as follows:
    # NR_i = (R_i - F_i^min)/(F_i^Max - F_i^min), for both objs: i=1,2
    x_norm = (x - min_cost) / (max_cost - min_cost)
    y_norm = (y - min_loads) / (max_loads - min_loads)


    # Step 3: Find the closes PO solution:
    # ID = argmin_(j=1)^N sqrt(sum_(i=1)^2 (NR_i - NF_i)^2)
    # Chosen BMP = ID-th member on the obtained ND set.
    df['EuclideanDistance'] = np.sqrt((df['CostNorm'] - x_norm)**2 + (df['LoadsNorm'] - y_norm)**2)
    # Find the row with the minimum Euclidean distance
    closest_solution = df.loc[df['EuclideanDistance'].idxmin()]

    print(closest_solution)


    #Step 4: Find two neighboring BMPs to the chosen BMP above:
    #ID1 = argmin_(j=1)^N sqrt(sum_(i=1)^2 (NF_i(ID) - NF_i)^2), with NF_1 <=
    #NF_1(ID) && sqrt(sum_(i=1)^2 (NF_i(ID) - NF_i)^2) >= eps
    #
    #and
    #
    #ID2 = argmin_(j=1)^N sqrt(sum_(i=1)^2 (NF_i(ID) - NF_i)^2), with NF_2 <=
    #NF_2(ID) && sqrt(sum_(i=1)^2 (NF_i(ID) - NF_i)^2) >= eps
    #
    #That's it. Create a small code in which you would input the ND set,
    #R-vector and an eps. The output would be the three BMP allocations.
    #
    #This can be changed with the ASF distance, instead of Euclidean distance
    #in Step 3, as the second MCDM method:
    #
    #ID = argmin_(j=1)^N max_(i=1)^2 (NF_i - NR_i)/w_i
    #(you can use w_i=1).
    #
    #Step 4 can still be used with Euclidean distance.
    n = 3
    nearest_solutions = df.sort_values(by='EuclideanDistance').head(n)
    return nearest_solutions

def extract_pf(objs):
    objs_len = len(objs)
    cnstrs = np.zeros((objs_len,1))
    filtered_objs = objs[:, :-1]
    fronts, ranks = nds(objs, cnstrs, compare_min)
    first_front = objs[fronts[0], :]
    return first_front

def pf_to_df(sols_file, description):
    objs = np.genfromtxt(sols_file, delimiter=' ')
    # conver first_front to dataframe
    first_front = extract_pf(objs)
    df = pd.DataFrame(first_front, columns=['Cost', 'Loads'])
    df['Description'] = description
    return df

def compute_loads(filename):
    # Load the JSON file
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    
    # Extract the lists of floats
    sum_load_invalid = data['sum_load_invalid']
    sum_load_valid = data['sum_load_valid']
    
    total_sums = []
    # Check if the lists have the same length
    if len(sum_load_invalid) != len(sum_load_valid):
        print("Error: The lists have different lengths.")
    else:
        # Initialize a list to store the sums
    
        # Iterate through the lists and calculate the sums by index
        for i in range(len(sum_load_invalid)):
            total_sums.append(sum_load_invalid[i] + sum_load_valid[i])
    
    return total_sums

def filter_gpoint(df, x, y):
    df_ge = df[(df['Cost'] >= x) & (df['Loads'] >= y)]
    df_le = df[(df['Cost'] <= x) & (df['Loads'] <= y)]
    if not df_le.empty:
        return df_le
    else:
        return df_ge

# Function to add random points (in yellow)
def add_random_points():

    for _ in range(3):
        new_x = random.uniform(0, 6)  # Generate a random x-coordinate between 0 and 6
        new_y = random.uniform(0, 6)  # Generate a random y-coordinate between 0 and 6
        new_desc = random.choice(descriptions)  # Randomly choose a description from the list
        new_data = {'x': [new_x], 'y': [new_y], 'desc': [new_desc]}
        source_yellow.stream(new_data)

def add_points(df):
    for index, row in df.iterrows():
        x = row['Cost']
        y = row['Loads']

        new_data = {'x': [x], 'y': [y], 'desc': ["Filtered Point"]}
        source_yellow.stream(new_data)

# Function to handle mouse click events and add red points
def add_point(event):
    x, y = event.x, event.y
    new_data = {'x': [x], 'y': [y], 'desc': ["Aspiration Point"]}
    source_red.stream(new_data)
    global method
    global selection_type
    if selection_type == 'Interactive':
        df = df4
    else:
        df = df_initial_scatter
    if method == 'Distance':
        #df = distance_method(df4, x, y)
        #df = distance_method(df_initial_scatter, x, y)
        df = distance_method(df, x, y)
    else:
        #df = filter_gpoint(df4, x, y)
        #df = filter_gpoint(df_initial_scatter, x, y)
        df = filter_gpoint(df, x, y)
    add_points(df)

def clear_points():
    source_red.data = {'x': [], 'y': [], 'desc': []}
    source_yellow.data = {'x': [], 'y': [], 'desc': []}

path = '/home/gtoscano/projects/CastPSO/build/20_runs/lc-all'
pf_prefix_bmp = f'{path}/front/pareto_front.txt'
pf_ef_min = f'{path}/ipopt/ipopt_results-all-sols-min/pareto_front_ipopt.txt'
pf_ef_median = f'{path}/ipopt/ipopt_results-all-sols-median/pareto_front_ipopt.txt'
pf_ef_max = f'{path}/ipopt/ipopt_results-all-sols-max/pareto_front_ipopt.txt'
pf_ef_only = f'{path}/../../pareto_front-nelson-efficiency-sorted.out'
df_initial_scatter = pf_to_df(pf_ef_only, 'Initial Efficiency BMPs')
df_animated_scatter = pf_to_df(pf_prefix_bmp, 'Land Conversion BMPs')
df1 = pf_to_df(pf_ef_min, 'LC + Eff BMPs (min)')
df2 = pf_to_df(pf_ef_median, 'LC + Eff BMPs (median)')
df3 = pf_to_df(pf_ef_max, 'LC + Eff BMPs (max)')

df_combined = pd.concat([df1, df2, df3, df_initial_scatter, df_animated_scatter], ignore_index=True)

df_combined_filtered = df_combined[['Cost', 'Loads']]
first_front = extract_pf(df_combined_filtered.values)
df4 = pd.DataFrame(first_front, columns=['Cost', 'Loads'])
df4 = df4.sort_values(by="Cost")

# Create a list of x and y coordinates for initial points
x_coords = [1, 2, 3, 4, 5]
y_coords = [5, 4, 3, 2, 1]
descriptions = ["A", "B", "C", "D", "E"]

descriptions = [f"({x}, {y})" for x, y in zip(df4['Cost'], df4['Loads'])] 


# Create a scatter plot for initial points (in blue)
#plot = figure(title="Interactive Scatter Plot")
# Create a scatter plot for initial points (in blue)
plot = figure(
    title="Interactive Scatter Plot",
    width=1600,  # Set the width of the plot (in pixels)
    height=1200,  # Set the height of the plot (in pixels)
    tools="pan,box_zoom,reset,save"
)
# Create a ColumnDataSource to hold the data for initial points (in blue)

source_blue = ColumnDataSource(data={'x': df_initial_scatter["Cost"], 'y': df_initial_scatter['Loads']})#, 'desc': descriptions})

scatter_blue = plot.scatter(x='x', y='y', source=source_blue, size=8, color="blue")

# Create a source for red points
source_red = ColumnDataSource(data={'x': [], 'y': [], 'desc': []})

# Create a source for random points (in yellow)
source_yellow = ColumnDataSource(data={'x': [], 'y': [], 'desc': []})

# Create a LabelSet for displaying descriptions
labels = LabelSet(x='x', y='y', text='desc', source=source_blue, x_offset=5, y_offset=5, text_font_size="12pt")


plot.on_event('tap', add_point)


# Create a button to add random points
add_random_button = Button(label="Clear Aspiratin Points")
add_random_button.on_click(add_random_points)

clear_button = Button(label="Clear Aspiratin Points")
clear_button.on_click(clear_points)

method_dropdown = Select(title="MCDM Method", value="Distance", options=["Distance", "g-Dominance"])  # Add more methods to options as needed.
method_dropdown.on_change('value', update_method)
selection_type_dropdown = Select(title="MCDM type", value="Interactive", options=["Interactive", "Current"])  # Add more selection_types to options as needed.
selection_type_dropdown.on_change('value', update_selection_type)

# Create scatter plots for red points (in red) and random points (in yellow)
scatter_red = plot.scatter(x='x', y='y', source=source_red, size=8, color="red")
scatter_yellow = plot.scatter(x='x', y='y', source=source_yellow, size=8, color="green")

# Create a HoverTool to display descriptions as tooltips
hover = HoverTool()
hover.tooltips = [("Description", "@desc"), ("(x,y)", "(@x, @y)")]
plot.add_tools(hover)

# Add the plot and the button to the current document
layout = column(method_dropdown, selection_type_dropdown, plot, clear_button)
curdoc().add_root(layout)
curdoc().add_root(labels)

