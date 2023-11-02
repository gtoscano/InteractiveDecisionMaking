import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot, column
from bokeh.models import Slider, ColumnDataSource, FactorRange, Select

import numpy as np

from mcdm import vikor, topsis, gdominance, distance
# Create a sample DataFrame with your data (replace this with your actual data)
data = {
    "Cost": [10, 20, 30, 40, 50],
    "Nitrogen": [5, 15, 25, 35, 45],
    "Phosphorous": [8, 18, 28, 38, 48],
    "Sediments": [2, 12, 22, 32, 42]
}

# Cost,NLoadEos,PLoadEos,SLoadEos,NLoadEor,PLoadEor,SLoadEor,NLoadEot,PLoadEot,SLoadEot

df = pd.read_csv('data.csv')
df = df[['Cost','NLoadEos','PLoadEos','SLoadEos']]
#df = pd.DataFrame(data)


# Create a Bokeh ColumnDataSource from your DataFrame
source = ColumnDataSource(df)

# Get the column names
columns = df.columns

for col in columns:
    df[col+'_norm'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# Convert column names to a list of tuples for Select options
select_options = [(col, col) for col in columns]
select_options = [['Cost','NLoadEos'],['Cost','PLoadEos'],['Cost','SLoadEos'], ['NLoadEos', 'PLoadEos'],['NLoadEos', 'SLoadEos'],['PLoadEos', 'SLoadEos']]

# Create a grid of scatter plots for the lower triangular combinations of columns
plots = []

for x_col,y_col in select_options:
    plot = figure(title=f"{x_col} vs {y_col}")
    plot.circle(x=x_col, y=y_col, source=source)
    plot.xaxis.axis_label = x_col
    plot.yaxis.axis_label = y_col
    plots.append(plot)

# Create Select widgets for X-axis and Y-axis columns
select_x = Select(title="X-axis", options=select_options, value=columns[0])
select_y = Select(title="Y-axis", options=select_options, value=columns[1])

# Define a callback function to update the scatter plots
def update_plot(attrname, old_val, new_val):
    x_column = select_x.value
    y_column = select_y.value
    for plot in plots:
        plot.xaxis.axis_label = x_column
        plot.yaxis.axis_label = y_column

# Attach the callback function to the Select widgets
select_x.on_change('value', update_plot)
select_y.on_change('value', update_plot)

# Create a layout for the Select widgets and the scatter plots
# Organize the plots in two rows with three plots in each row
grid = []
for i in range(0, len(plots), 3):
    grid.append([plots[i], plots[i + 1], plots[i + 2]])

# Create sliders for each preference
cost_slider = Slider(title="Cost Weight", value=0.5, start=0, end=1, step=0.01)
nitrogen_slider = Slider(title="Nitrogen Weight", value=0.5, start=0, end=1, step=0.01)
phosphorous_slider = Slider(title="Phosphorous Weight", value=0.5, start=0, end=1, step=0.01)
sediments_slider = Slider(title="Sediments Weight", value=0.5, start=0, end=1, step=0.01)

# Function to update the DataFrame based on slider values
def update_data(attr, old, new):
    Cost = cost_slider.value
    Nitrogen = nitrogen_slider.value
    Phosphorous = phosphorous_slider.value 
    Sediments = sediments_slider.value
    df_current = df[['Cost','NLoadEos','PLoadEos','SLoadEos']]
    weights = [Cost, Nitrogen, Phosphorous, Sediments]
    benefit_criteria =  [False, False, False, False]
    method = 'Vikor'
    if method == 'Topsis':
        ranking_order = topsis(df_current.values, weights, benefit_criteria)
    elif method == 'Vikor': 
       v = 0.7
       compromise_solutions = vikor(df_current.values, weights, benefit_criteria, v)
       print (compromise_solutions)

# Attach the update function to the slider's value change event
cost_slider.on_change("value", update_data)
nitrogen_slider.on_change("value", update_data)
phosphorous_slider.on_change("value", update_data)
sediments_slider.on_change("value", update_data)


layout = gridplot(grid)

# Create a layout for the Select widgets
widget_layout = gridplot([[select_x, select_y]])

slider_layout = column(cost_slider, nitrogen_slider, phosphorous_slider, sediments_slider)
# Add both layouts to the current document
curdoc().add_root(slider_layout)
#curdoc().add_root(widget_layout)
curdoc().add_root(layout)

# To display the plot in a standalone HTML file, you can use the following command:
# show(widget_layout)

