from django.shortcuts import render
from .bokeh_plot import create_scatter_plot

def scatter_view(request):
    script, div = create_scatter_plot()
    return render(request, "scatterplot/plot.html", {"script": script, "div": div})

