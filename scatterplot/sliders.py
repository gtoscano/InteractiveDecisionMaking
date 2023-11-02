from bokeh.layouts import column
from bokeh.plotting import curdoc, figure
from bokeh.models import Slider, ColumnDataSource, FactorRange
import pandas as pd

# Create an initial DataFrame with some example data
data = {
    "Cost": [0.2, 0.3, 0.4, 0.1],
    "Nitrogen": [0.1, 0.2, 0.3, 0.4],
    "Phosphorous": [0.4, 0.2, 0.1, 0.3],
    "Sediments": [0.3, 0.1, 0.4, 0.2],
}
df = pd.DataFrame(data)

# Convert the index to strings
df.index = df.index.astype(str)

# Create a ColumnDataSource to hold the data for plotting
source = ColumnDataSource(data=df)

# Create sliders for each preference
cost_slider = Slider(title="Cost Weight", value=0.5, start=0, end=1, step=0.01)
nitrogen_slider = Slider(title="Nitrogen Weight", value=0.5, start=0, end=1, step=0.01)
phosphorous_slider = Slider(title="Phosphorous Weight", value=0.5, start=0, end=1, step=0.01)
sediments_slider = Slider(title="Sediments Weight", value=0.5, start=0, end=1, step=0.01)

# Function to update the DataFrame based on slider values
def update_data(attr, old, new):
    df["Cost"] = [cost_slider.value * weight for weight in df["Cost"]]
    df["Nitrogen"] = [nitrogen_slider.value * weight for weight in df["Nitrogen"]]
    df["Phosphorous"] = [phosphorous_slider.value * weight for weight in df["Phosphorous"]]
    df["Sediments"] = [sediments_slider.value * weight for weight in df["Sediments"]]
    source.data = df

# Attach the update function to the slider's value change event
cost_slider.on_change("value", update_data)
nitrogen_slider.on_change("value", update_data)
phosphorous_slider.on_change("value", update_data)
sediments_slider.on_change("value", update_data)

# Create a list of the categories for the x-axis (assuming your index is categorical)
categories = df.index.tolist()

# Create a FactorRange for the x-axis
x_range = FactorRange(factors=categories)

# Create a plot to visualize the updated data (you can customize this plot)
plot = figure(x_range=x_range, height=300, title="Weighted Preferences")
plot.vbar(x="index", top="Cost", source=source, width=0.2, color="blue", legend_label="Cost")
plot.vbar(x="index", top="Nitrogen", source=source, width=0.2, color="green", legend_label="Nitrogen", line_color="white")
plot.vbar(x="index", top="Phosphorous", source=source, width=0.2, color="orange", legend_label="Phosphorous", line_color="white")
plot.vbar(x="index", top="Sediments", source=source, width=0.2, color="red", legend_label="Sediments", line_color="white")
plot.legend.location = "top_right"
plot.legend.title = "Preferences"

# Create a layout for the app
layout = column(cost_slider, nitrogen_slider, phosphorous_slider, sediments_slider, plot)

# Add the layout to the current document
curdoc().add_root(layout)
