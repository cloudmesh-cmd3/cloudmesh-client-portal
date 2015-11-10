import pygal
from pprint import pprint
import os

clusters = [
    {
        'name': "free",
        'total': 20,
        'status': {
            'up': 5,
            'down': 10,
            'unkown': 5,
        }
    },
    {
        'name': "v1",
        'total': 15,
        'status': {
            'up': 5,
            'down': 5,
            'unkown': 5,
        }
    },
    {
        'name': "v2",
        'total': 15,
        'status': {
            'up': 10,
            'down': 2,
            'unkown': 3,
        }
    },
]

from pygal.style import BlueStyle
# chart = pygal.StackedLine(fill=True, interpolate='cubic', style=BlueStyle)

pprint(clusters)


def cluster_overview_pie(clusters):
    chart = pygal.Pie(fill=True,
                      style=BlueStyle(
                          font_family='googlefont:Source Sans Pro',
                          value_font_size=30,
                          label_font_size=30,
                          value_label_font_size=30,
                          title_font_size=30,
                          major_label_font_size=30,
                          tooltip_font_size=30,
                          legend_font_size=30,
                          no_data_font_size=30),
                      print_labels=True,
                      print_values=True)
    chart.title = 'Comet Virtual Cluster Nodes used by Projects'

    for cluster in clusters:
        chart.add(cluster['name'], cluster['total'])
    return chart


def cluster_overview_pie_vector(clusters):
    chart = pygal.Pie(fill=True,
                      style=BlueStyle(
                          font_family='googlefont:Source Sans Pro',
                          value_font_size=30,
                          label_font_size=30,
                          value_label_font_size=30,
                          title_font_size=30,
                          major_label_font_size=30,
                          tooltip_font_size=30,
                          legend_font_size=30,
                          no_data_font_size=30),
                      print_labels=True,
                      print_values=True)
    chart.title = 'Comet Virtual Cluster Nodes used by Projects with Status'

    for cluster in clusters:
        state = cluster['status']
        # data = [state["up"], state["down"], state['unkown']]
        data = [
            {'value': state["up"], 'color': 'green', 'value_font_size': '24'},
            {'value': state["down"], 'color': 'red'},
            {'value': state["unkown"], 'color': 'white'},
        ]

        chart.add(cluster['name'], data)
    return chart


def cluster_overview_radar(clusters):
    chart = pygal.Radar(fill=True,
                        style=BlueStyle(
                            font_family='googlefont:Source Sans Pro',
                            value_font_size=30,
                            label_font_size=30,
                            value_label_font_size=30,
                            title_font_size=30,
                            major_label_font_size=30,
                            tooltip_font_size=30,
                            legend_font_size=30,
                            no_data_font_size=30), )
    chart.title = 'Comet Virtual Cluster Radar for Status of the Nodes'

    chart.x_labels = ['up', 'down', 'unkown', 'total']

    for cluster in clusters:
        state = cluster['status']
        data = [state["up"], state["down"], state['unkown'], cluster['total']]
        chart.add(cluster['name'], data)
    return chart


# pie_chart.render_to_file('pie.svg')

def to_path(name):
    path = os.path.join("..", "..", "static", "cloudmesh_portal", name)
    return path


cluster_overview_pie(clusters).render_to_file(to_path('pie.svg'))
cluster_overview_radar(clusters).render_to_file(to_path('radar.svg'))
cluster_overview_pie_vector(clusters).render_to_file(to_path('pie_vector.svg'))

# cluster_overview_pie(clusters).render_in_browser()
# cluster_overview_radar(clusters).render_in_browser()
# cluster_overview_pie_vector(clusters).render_in_browser()
