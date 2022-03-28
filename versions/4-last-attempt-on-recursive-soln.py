import copy

from ipywidgets import interact, interactive, widgets, Button, Layout

wtypes = []


def add_btn_clicked(linebox, f):

    def callback(arg):
        # Assume that the spec has lists where "add more" extends only first item.
        # linebox.children = (linebox.children[0], f()[0]) + linebox.children
        linebox.children = (linebox.children[0], f()[0]) + linebox.children[1:]
    return callback


def delete_btn_clicked(b):
    b.parent.layout.display = 'none'


def create_form(spec, o):

    if isinstance(spec, dict):
        o = {}
        box = []
        for key in spec:
            o[key] = spec[key]
            box.append(create_form(spec[key], o))
        box.append(widgets.Output(layout={'border': '1px solid black'}))
        return widgets.VBox(box)

    elif isinstance(spec, list):
        add = widgets.Button(description="Add More", icon="plus-circle")
        o = []

        def create_section():
            section = []
            delete_button = widgets.Button(icon="trash")
            delete_button.on_click(delete_btn_clicked)
            for i in spec:
                o.append(i)
                element = create_form(i, o)
                section.append(widgets.VBox([element, delete_button]))
            return section

        section = create_section()
        addbox = widgets.VBox([add])
        section.append(addbox)
        input_box = widgets.VBox(section)
        add.on_click(add_btn_clicked(input_box, create_section))
        return input_box

    # Base case
    else:
        w = spec()
        o = w
        return w # Note: this might result in lists with copies ref, if that happens try to return a copy of spec


def generate_form(clusters, envs):
    global wtypes
    wtypes = [widgets.Dropdown, widgets.Text, widgets.Textarea]
    spec = {
        "cluster": lambda: widgets.Dropdown(options=clusters, value=clusters[0], description='Cluster:'),
        "env": lambda: widgets.Dropdown(options=envs, value=envs[0], description='Environment:'),
        "team_name": lambda: widgets.Text(value='team-name', description='Team:'),
        "project_description": lambda: widgets.Textarea(value='your project description here', description='Description:'),
        "users": [
            lambda: widgets.Text(value='github-username', description='GitHub Username:'),
            lambda: widgets.Text(value='github-username', description='GitHub Username:')
        ],

        "namespaces": [
            {
                "name": lambda: widgets.Text(value='Your-Namespace-Name', description='Namespace:'),
                "custom_quota": {
                    "requests.cpu": lambda: widgets.Text(value='2', description='requests.cpu'),
                    "requests.memory": lambda: widgets.Text(value='2Gi', description='requests.memory'),
                    "limits.cpu": lambda: widgets.Text(value='4', description='limits.cpu'),
                    "limits.memory": lambda: widgets.Text(value='4Gi', description='limits.memory.'),
                    "requests.storage": lambda: widgets.Text(value='8Gi', description='requests.storage'),
                    "count/objectbucketclaims.objectbucket.io": lambda: widgets.BoundedIntText(value=4, min=0, max=100, description='Bucketclaims'),
                }
            },
            {
                "name": lambda: widgets.Text(value='Your-Namespace-Name', description='Namespace:'),
                "custom_quota": {
                    "requests.cpu": lambda: widgets.Text(value='2', description='requests.cpu'),
                    "requests.memory": lambda: widgets.Text(value='2Gi', description='requests.memory'),
                    "limits.cpu": lambda: widgets.Text(value='4', description='limits.cpu'),
                    "limits.memory": lambda: widgets.Text(value='4Gi', description='limits.memory.'),
                    "requests.storage": lambda: widgets.Text(value='8Gi', description='requests.storage'),
                    "count/objectbucketclaims.objectbucket.io": lambda: widgets.BoundedIntText(value=4, min=0, max=100, description='Bucketclaims'),
                }
            }
        ]
    }
    out = {}
    formbox = create_form(spec, out)
    return formbox


