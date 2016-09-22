from cloudmesh_client.cloud.launcher import Launcher
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.util import path_expand
from django.shortcuts import render
from sqlalchemy.orm import sessionmaker


# noinspection PyPep8Naming
def Session():
    from aldjemy.core import get_engine
    engine = get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()


session = Session()


def cloudmesh_launcher_start(request):
    parameters = dict(request.POST)
    for key in parameters:
        try:
            parameters[key] = parameters[key][0]
        except:
            pass
    if 'csrfmiddlewaretoken' in parameters:
        del parameters['csrfmiddlewaretoken']

    response = 'error'
    if parameters["name"]:
        name = parameters["name"]

        launcher_config = ConfigDict(path_expand("~/.cloudmesh/cloudmesh_launcher.yaml"))
        recipe = dict(launcher_config["cloudmesh.launcher.recipes"])[name]

        print(json.dumps(recipe, indent=4))

        response = "error"

        if recipe["script"]["type"] in ["sh", "shell"]:
            script = recipe["script"]["value"].format(**parameters)
            print (script)
            launcher = Launcher("shell")
            print (type(launcher))
            response = launcher.run(script=script)
            parameters["script"] = script

    else:
        parameters = "error"

    context = {
        'title': '<div><i class="fa fa-rocket"></i> Cloudmesh Launcher</div>',
        "response": response,
        "parameters": parameters,
    }

    return render(request,
                  'cloudmesh_portal/launcher/mesh_launch_response.jinja',
                  context)
