import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column

# Create a sample DataFrame with your data (replace this with your actual data)
data = {
    "Cost": [10, 20, 30, 40, 50],
    "Nitrogen": [5, 15, 25, 35, 45],
    "Phosphorous": [8, 18, 28, 38, 48],
    "Sediments": [2, 12, 22, 32, 42]
}

df = pd.DataFrame(data)

# Create a Bokeh ColumnDataSource from your DataFrame
source = ColumnDataSource(df)

# Create a Bokeh figure for the scatter plot
plot = figure(title="Scatter Plot")

# Define a function to update the scatter plot based on the selected columns
def update_plot(attrname, old_value, new_value):
    x = select_x.value
    y = select_y.value

    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # Clear previous renderers
    plot.renderers = []

    plot.circle(x=x, y=y, source=source)

# Create two Select widgets for selecting the x and y columns
select_x = Select(title="X-axis", options=["Cost", "Nitrogen", "Phosphorous", "Sediments"], value="Cost")
select_y = Select(title="Y-axis", options=["Cost", "Nitrogen", "Phosphorous", "Sediments"], value="Nitrogen")

# Attach the update_plot function to the on_change event of the Select widgets
select_x.on_change('value', update_plot)
select_y.on_change('value', update_plot)

# Initialize the scatter plot with the default values
update_plot(None, None, None)

# Create a layout for the Select widgets and the scatter plot
layout = column(select_x, select_y, plot)

# Add the layout to the current document
curdoc().add_root(layout)

# To display the plot in a standalone HTML file, you can use the following command:
# show(layout)
