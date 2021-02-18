import pygal
from django import template

register = template.Library()

@register.simple_tag
def render_pie(data):
    # Make a pie chart
    pie_chart = pygal.Pie()
    # Add the data to the pie chart
    for key, value in data.items():
        pie_chart.add(key, int(value))
    # Render
    return pie_chart.render_data_uri()

@register.simple_tag
def render_bar(data):
    # Make a pie chart
    bar_chart = pygal.HorizontalBar()
    # Add the data to the pie chart
    for key, value in data.items():
        bar_chart.add(key, int(value))
    # Render
    return bar_chart.render_data_uri()
