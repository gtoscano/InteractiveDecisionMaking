# bokeh_plot.py
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components
from bokeh.models import TapTool, CustomJS

def create_scatter_plot():
    # Sample data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    descriptions = ["A", "B", "C", "D", "E"]

    source = ColumnDataSource(data=dict(x=x, y=y, desc=descriptions))

    #plot = figure(plot_width=400, plot_height=400, tools="tap", title="Scatter Plot")
    plot = figure(width=800, height=400, tools="tap", title="Scatter Plot")
    plot.scatter('x', 'y', source=source, size=10)

    #hover = HoverTool()
    #hover.tooltips = [("Description", "@desc"), ("(x,y)", "(@x, @y)")]
    #plot.add_tools(hover)


    # JavaScript code that runs when the canvas is clicked
    callback = CustomJS(args=dict(source=source), code="""
        const data = source.data;
        const coords = cb_obj.geometry;
        
        // Append the coordinates to the existing data
        data['x'].push(coords.x);
        data['y'].push(coords.y);
        data['desc'].push("New");

        // Notify the DataSource of the change
        source.change.emit();
    """)

    tap_tool = TapTool(callback=callback)
    plot.add_tools(tap_tool)
    plot.toolbar.active_tap = tap_tool  # Make TapTool the active tool

    return components(plot)
