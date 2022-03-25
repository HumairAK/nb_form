from ipywidgets import interact, interactive, widgets, Button, Layout

wtypes = []


def render(spec):
    if isinstance(spec, dict):
        accumulate = []
        for i in spec:
            accumulate += render(spec[i])
        return accumulate

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


def create_vbox(form):
    box = []
    for i in form:
        if isinstance(i, list):
            out = widgets.Output(layout={'border': '1px solid black'})
            # out.append_stdout("test")
            box.append(out)
            box.append(widgets.VBox(i))
        else:
            box.append(i)
    return widgets.VBox(box)


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
        ]
    }


    r = render(spec)
    formbox = create_vbox(r)
    return formbox


