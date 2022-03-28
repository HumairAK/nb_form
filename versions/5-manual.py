from ipywidgets import interact, interactive, widgets, Button, Layout
import yaml


def done_action(s):

    def callback(e):
        data = {
            'env': s['env'].value,
            'target_cluster': s['cluster'].value,
            'team_name': s['team_name'].value,
            'project_description': s['project_description'].value,
            'users': [],
            'namespaces': []
        }

        for user in s['users']:
            data['users'].append(user.value)

        d = yaml.safe_dump(data)
        print(d)
    return callback


def create_users():
    pass



def generate_form(clusters, envs):
    spec = {
        "cluster": widgets.Dropdown(options=clusters, value=clusters[0], description='Cluster:'),
        "env": widgets.Dropdown(options=envs, value=envs[0], description='Environment:'),
        "team_name": widgets.Text(value='team-name', description='Team:'),
        "project_description": widgets.Textarea(value='your project description here', description='Description:'),

        "users": [
            widgets.Text(value='github-username', description='GitHub Username:'),
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

    divider = widgets.Output(layout={'border': '1px solid black'})

    # Users:
    users = spec['users'][0]

    # Namespaces

    # Done Button
    done_button = widgets.Button(description='Generate PR', button_style='', tooltip='Click me', )
    done_button.on_click(done_action(spec))

    form = [
        spec['cluster'],
        spec['env'],
        spec['team_name'],
        spec['project_description'],
        divider,
        users,
        # DONE
        done_button,
    ]

    return widgets.VBox(form), spec


