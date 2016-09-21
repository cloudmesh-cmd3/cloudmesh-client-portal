import os

import pygal
from pygal.style import BlueStyle

clusters = [
    {
        'name': "free",
        'total': 20,
        'status': {
            'active': 5,
            'down': 10,
            'pending': 0,
            'unkown': 5,
        }
    },
    {
        'name': "v1",
        'total': 15,
        'status': {
            'active': 5,
            'pending': 0,
            'down': 5,
            'unkown': 5,
        }
    },
    {
        'name': "v2",
        'total': 15,
        'status': {
            'active': 10,
            'pending': 0,
            'down': 2,
            'unkown': 3,
        }
    },
]


# chart = pygal.StackedLine(fill=True, interpolate='cubic', style=BlueStyle)


class Chart(object):
    path = os.path.join("static", "cloudmesh_portal")

    @classmethod
    def to_path(cls, name):
        return os.path.join(cls.path, name)

    @classmethod
    def cluster_overview_pie(cls, clusters, filename=None):
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
            # chart.add(cluster['name'], cluster['total'])
            chart.add(cluster['name'],
                      [{'value': cluster['total'],
                        'label': '{}'.format(cluster['total'])
                        }
                       ]
                      )

        if filename is not None:
            chart.render_to_file(cls.to_path(filename))
        return chart

    @classmethod
    def cluster_overview_pie_vector(cls, clusters, filename=None):
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
        chart.title = 'Comet Virtual Cluster Nodes ' \
                      'used by Projects with Status'

        for cluster in clusters:
            state = cluster['status']
            # data = [state["up"], state["down"], state['unkown']]
            data = [
                {'value': state["active"], 'color': 'green',
                 'value_font_size': '24'},
                {'value': state["down"], 'color': 'red'},
                {'value': state["pending"], 'color': 'yellow'},
                {'value': state["unkown"], 'color': 'white'},
            ]

            chart.add(cluster['name'], data)
        if filename is not None:
            chart.render_to_file(cls.to_path(filename))
        return chart

    @classmethod
    def cluster_overview_radar(cls, clusters, filename=None):
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

        chart.x_labels = ['pending', 'active', 'unkown', 'down', 'total']

        for cluster in clusters:
            state = cluster['status']
            data = [state["active"],
                    state["down"],
                    state['pending'],
                    cluster['total']]
            chart.add(cluster['name'], data)
        if filename is not None:
            chart.render_to_file(cls.to_path(filename))
        return chart

# cluster_overview_pie(clusters).render_to_file(to_path('pie.svg'))
# cluster_overview_radar(clusters).render_to_file(to_path('radar.svg'))
# cluster_overview_pie_vector(clusters).render_to_file(to_path(
# 'pie_vector.svg'))

# cluster_overview_pie(clusters).render_in_browser()
# cluster_overview_radar(clusters).render_in_browser()
# cluster_overview_pie_vector(clusters).render_in_browser()
