from ipywidgets import interact, interactive, widgets, Button, Layout

wtypes = []

def render(spec):
    if isinstance(spec, dict):
        accumulate = []
        for i in spec:
            accumulate += render(spec[i])
        return [accumulate]

    elif isinstance(spec, list):
        accumulate = []
        for i in spec:
            accumulate += render(i)
        return [accumulate]

    # Base case
    elif any([isinstance(spec, i) for i in wtypes]):
        return [spec]
    else:
        return []


def add_btn_clicked(linebox, f):
    def callback(arg):
        # Assume that the spec has lists where "add more" extends only first item.
        # linebox.children = (linebox.children[0], f()[0]) + linebox.children
        linebox.children = (linebox.children[0], f()[0]) + linebox.children[1:]
    return callback

def delete_btn_clicked(b):
    b.parent.layout.display = 'none'

def create_vbox(spec):

    if isinstance(spec, dict):
        box = []
        for key in spec:
            box.append(create_vbox(spec[key]))
        box.append(widgets.Output(layout={'border': '1px solid black'}))
        return widgets.VBox(box)

    elif isinstance(spec, list):
        add = widgets.Button(description="Add More", icon="plus-circle")

        def create_section():
            section = []
            delete_button = widgets.Button(icon="trash")
            delete_button.on_click(delete_btn_clicked)
            for i in spec:
                element = create_vbox(i)
                section.append(element)
            section.append(delete_button)
            return section

        section = create_section()
        section.append(add)
        input_box = widgets.VBox(section)
        add.on_click(add_btn_clicked(input_box, create_section))
        return input_box

    # Base case
    else:
        return spec


def generate_form(clusters, envs):
    global wtypes
    wtypes = [widgets.Dropdown, widgets.Text, widgets.Textarea]
    spec = {
        "cluster": widgets.Dropdown(options=clusters, value=clusters[0], description='Cluster:'),
        "env": widgets.Dropdown(options=envs, value=envs[0], description='Environment:'),
        "team_name": widgets.Text(value='team-name', description='Team:'),
        "project_description": widgets.Textarea(value='your project description here', description='Description:'),
        "users": [
            widgets.Text(value='github-username', description='GitHub Username:')
        ],
        "namespaces": [
            {
                "name": widgets.Text(value='Your-Namespace-Name', description='Namespace:'),
                "custom_quota": {
                    "requests.cpu": widgets.Text(value='2', description='requests.cpu'),
                    "requests.memory": widgets.Text(value='2Gi', description='requests.memory'),
                    "limits.cpu": widgets.Text(value='4', description='limits.cpu'),
                    "limits.memory": widgets.Text(value='4Gi', description='limits.memory.'),
                    "requests.storage": widgets.Text(value='8Gi', description='requests.storage'),
                    "count/objectbucketclaims.objectbucket.io": widgets.BoundedIntText(value=4, min=0, max=100, description='Bucketclaims'),
                }
            },
            {
                "name": widgets.Text(value='Your-Nafdsamespace-Name', description='Namespace:'),
                "custom_quota": {
                    "requests.cpu": widgets.Text(value='2', description='requests.cpu'),
                    "requests.memory": widgets.Text(value='2Gi', description='requests.memory'),
                    "limits.cpu": widgets.Text(value='4', description='limits.cpu'),
                    "limits.memory": widgets.Text(value='4Gi', description='limits.memory.'),
                    "requests.storage": widgets.Text(value='8Gi', description='requests.storage'),
                    "count/objectbucketclaims.objectbucket.io": widgets.BoundedIntText(value=4, min=0, max=100,
                                                                                       description='Bucketclaims'),
                }
            }
        ]
    }


    # r = render(spec)
    formbox = create_vbox(spec)
    return formbox


