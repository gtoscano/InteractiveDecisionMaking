# bokeh serve multiplotall.py --port 5007
import pandas as pd
from bokeh.models import LabelSet
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot, column, row
from bokeh.models import Slider, ColumnDataSource, FactorRange, Select
from bokeh.models import CDSView, BooleanFilter

import numpy as np

from mcdm import vikor, topsis, gdominance, distance
from bokeh.transform import factor_cmap
from bokeh.layouts import layout
from bokeh.io import curdoc

method = 'VIKOR'
y_axis_method = 'Percentage'
select_options_lbs = [['Cost','NLoadEos'],['Cost','PLoadEos'],['Cost','SLoadEos'], ['NLoadEos', 'PLoadEos'],['NLoadEos', 'SLoadEos'],['PLoadEos', 'SLoadEos']]
select_options_percentage = [['Cost','NLoadEosP'],['Cost','PLoadEosP'],['Cost','SLoadEosP'], ['NLoadEosP', 'PLoadEosP'],['NLoadEosP', 'SLoadEosP'],['PLoadEosP', 'SLoadEosP']]
axis_label = {'Cost':'Cost (US Dollars)', 'NLoadEos':'Nitrogen Loads (lbs)', 'PLoadEos':'Phosphorous Loads (lbs)', 'SLoadEos':'Sediments Loads (lbs)', 'NLoadEosP':'Nitrogen Percentage Reduction (%)', 'PLoadEosP':'Phosphorous Percentage Reduciton (%)', 'SLoadEosP':'Sediments Percentage Reduction (%)'}



def create_plots(selected_options):
    plots_temp = []
    for x_col, y_col in selected_options:
        plot = figure(title=f"{x_col} vs {y_col}")
        
        plot.circle(x=x_col, y=y_col, source=source, 
                    color='color', 
                    legend_field='set', size=12)

        labels = LabelSet(x=x_col, y=y_col, text='ranking', level='glyph',
                          x_offset=5, y_offset=5, source=source)
        plot.add_layout(labels)
        plot.legend.location = "bottom_right"
        
        plot.xaxis.axis_label = axis_label[x_col]
        plot.yaxis.axis_label = axis_label[y_col]
        # For axis labels
        plot.xaxis.axis_label_text_font_size = "16pt"
        plot.yaxis.axis_label_text_font_size = "16pt"
        
        # For axis tick labels
        plot.xaxis.major_label_text_font_size = "12pt"
        plot.yaxis.major_label_text_font_size = "12pt"
        
        # For plot title
        plot.title.text_font_size = "18pt"
        
        # If you have a legend
        plot.legend.label_text_font_size = "14pt"

        plots_temp.append(plot)

    return plots_temp

def indices_to_rankings(indices):
    indices_list = indices.tolist()  # Convert numpy array to list
    return [indices_list.index(i) for i in range(len(indices_list))]

def update_method(attr, old, new):
    global method
    method = method_dropdown.value
# Modify the update_y_axis_method function
def update_y_axis_method(attr, old, new):
    global y_axis_method 
    y_axis_method = y_axis_method_dropdown.value
    
    # Choose the options based on the new dropdown value
    if new == 'Percentage':
        selected_options = select_options_percentage
    else:
        selected_options = select_options_lbs
    
    # Use the helper function to get the updated plots
    updated_plots = create_plots(selected_options)
    
    # Update the layout with the new plots
    grid = []
    for i in range(0, len(updated_plots), 3):
        grid.append([updated_plots[i], updated_plots[i + 1], updated_plots[i + 2]])

    main_layout.children[0] = gridplot(grid)


# Create a sample DataFrame with your data (replace this with your actual data)
data = {
    "Cost": [10, 20, 30, 40, 50],
    "Nitrogen": [5, 15, 25, 35, 45],
    "Phosphorous": [8, 18, 28, 38, 48],
    "Sediments": [2, 12, 22, 32, 42]
}

# Cost,NLoadEos,PLoadEos,SLoadEos,NLoadEor,PLoadEor,SLoadEor,NLoadEot,PLoadEot,SLoadEot

init_load = [1206902.23971666, 168643.173170355, 306396334.368122, 884965.79194369, 94560.0038687795, 87152977.072462, 657042.079737883, 84455.0212445554, 105408036.583014]
init_load_df = pd.DataFrame([init_load], columns=['NLoadEos','PLoadEos','SLoadEos','NLoadEor','PLoadEor','SLoadEor','NLoadEot','PLoadEot','SLoadEot'])
init_load_df['Cost'] = 0.0


df = pd.read_csv('data.csv')
df = df[['Cost','NLoadEos','PLoadEos','SLoadEos']]
df['color'] = 'blue' # default color
df['ranking'] = ' ' 
df['set'] = df['color'].map({'blue': 'PF', 'red': 'Selected'})
for col in ['NLoadEos','PLoadEos','SLoadEos']:
    df[col+'P'] = (init_load_df[col].values[0] - df[col]) / init_load_df[col].values[0] * 100
#df = pd.DataFrame(data)


# Create a Bokeh ColumnDataSource from your DataFrame
source = ColumnDataSource(df)

# Get the column names
columns = df.columns

#for col in columns:
#    df[col+'_norm'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# Convert column names to a list of tuples for Select options

# Create a grid of scatter plots for the lower triangular combinations of columns
plots = []

# Modify your plot creation to use the color field from source

#for x_col, y_col in select_options:
#    plot = figure(title=f"{x_col} vs {y_col}")
#    plot.circle(x=x_col, y=y_col, source=source, color='color', legend_field='color', size=12)
#    
#    labels = LabelSet(x=x_col, y=y_col, text='ranking', level='glyph',
#                  x_offset=5, y_offset=5, source=source)
#    plot.add_layout(labels)
#    
#    plot.xaxis.axis_label = x_col
#    plot.yaxis.axis_label = y_col
#    plots.append(plot)





unique_sets = df['set'].unique().tolist()
color_map = factor_cmap('set', palette=['blue', 'red'], factors=unique_sets)


# Adjust the part where you first create the plots
if y_axis_method == 'Percentage':
    selected_options = select_options_percentage
else:
    selected_options = select_options_lbs
plots = create_plots(selected_options)


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
method_dropdown = Select(title="MCDM Method", value="VIKOR", options=["VIKOR", "TOPSIS"])  # Add more methods to options as needed.
y_axis_method_dropdown = Select(title="Display", value="Percentage", options=["Percentage", "Lbs"])  # Add more y_axis_methods to options as needed.



# Function to update the DataFrame based on slider values
def update_data(attr, old, new):
    Cost = cost_slider.value
    Nitrogen = nitrogen_slider.value
    Phosphorous = phosphorous_slider.value 
    Sediments = sediments_slider.value
    weights = [Cost, Nitrogen, Phosphorous, Sediments]
    benefit_criteria =  [False, False, False, False]

    df_values = df[['Cost','NLoadEos','PLoadEos','SLoadEos']].values
    global method
    if method == 'TOPSIS':
        benefit_criteria =  [True, True, True, True]
        ranking_order = topsis(df_values, weights, benefit_criteria)
        idx = indices_to_rankings(ranking_order)
        df['ranking'] = idx
        df['color'] = ['red' if idx[i] == 0 else 'blue' for i in range(len(ranking_order))]
        print(ranking_order)
    elif method == 'VIKOR': 
        v = 0.0
        compromise_solutions = vikor(df_values, weights, v)
        df['color'] = ['red' if i in compromise_solutions else 'blue' for i in range(len(df))]
        #df['set'] = ['Selected' if i in compromise_solutions else 'PF' for i in range(len(df))]
        df['set'] = df['color'].map({'blue': 'PF', 'red': 'Selected'})
        df['ranking'] = ' ' 
        print (compromise_solutions)

    # Update the data source with the new DataFrame
    source.data = df

# Attach the update function to the slider's value change event
cost_slider.on_change("value", update_data)
nitrogen_slider.on_change("value", update_data)
phosphorous_slider.on_change("value", update_data)
sediments_slider.on_change("value", update_data)

method_dropdown.on_change('value', update_method)
y_axis_method_dropdown.on_change('value', update_y_axis_method)

main_layout = column(gridplot(grid))

slider_layout = row(y_axis_method_dropdown, method_dropdown, cost_slider, nitrogen_slider, phosphorous_slider, sediments_slider)
# Add both layouts to the current document
curdoc().add_root(slider_layout)
#curdoc().add_root(widget_layout)
curdoc().add_root(main_layout)
# Adding dropdown to the layout.
# To display the plot in a standalone HTML file, you can use the following command:
# show(widget_layout)


