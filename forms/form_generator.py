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

        for i in s['users']:
            data['users'].append(s['_toYaml']['users'](i))

        for i in s['namespaces']:
            data['namespaces'].append(s['_toYaml']['namespaces'](i))

        with open('output.yaml', 'w') as f:
            yaml.safe_dump(data, f)


    return callback


def add_btn_clicked(spec_entries, box, widget_creator):
    def callback(b):
        widget = widget_creator()
        spec_entries.append(widget)

        delete_button = widgets.Button(icon="trash")
        delete_button.on_click(delete_btn_clicked(widget, spec_entries))

        entry = widgets.HBox([widget, delete_button])
        delete_button.parent = entry

        box.children = (box.children[0], entry) + box.children[1:]
    return callback


def delete_btn_clicked(widget, spec_entries):
    def callback(b):
        spec_entries.remove(widget)
        b.parent.layout.display = 'none'
    return callback


def dyamic_line(spec_entries, widget_creator):
    add = widgets.Button(description="Add", icon="plus-circle")
    input_box = widgets.VBox([add])
    cb = add_btn_clicked(spec_entries, input_box, widget_creator)
    add.on_click(cb)
    cb(input_box)
    return input_box


def generate_form(clusters, envs):
    spec = {
        "cluster": widgets.Dropdown(options=clusters, value=clusters[0], description='Cluster:'),
        "env": widgets.Dropdown(options=envs, value=envs[0], description='Environment:'),
        "team_name": widgets.Text(value='team-name', description='Team:'),
        "project_description": widgets.Textarea(value='your project description here', description='Description:'),
        # Dynamic entries
        "users": lambda: widgets.Text(value='github-username', description='GitHub Username:'),
        "namespaces": lambda: widgets.VBox([
            widgets.Text(value='Your-Namespace-Name', description='Namespace:'),
            widgets.Text(value='false', description='Disable limit range:'),
            widgets.Text(value='display-name', description='Project display name:'),
            widgets.Text(value='small', description='Quota tier:'),
            widgets.VBox([
                widgets.Text(value='2', description='requests.cpu'),
                widgets.Text(value='2Gi', description='requests.memory'),
                widgets.Text(value='4', description='limits.cpu'),
                widgets.Text(value='4Gi', description='limits.memory.'),
                widgets.Text(value='8Gi', description='requests.storage'),
                widgets.BoundedIntText(value=4, min=0, max=100, description='Bucketclaims')
            ]),
            widgets.Output(layout={'border': '1px solid black'})

        ]),


        # Meta custom converters
        "_toYaml": {
            "users": lambda w: w.value,
            "namespaces": lambda w: {
                "name": w.children[0].value,
                "enable_monitoring": "false", # TODO: remove, monitoring switched to UWM
                "disable_limit_range": w.children[1].value,
                "project_display_name": w.children[2].value,
                "quota": w.children[3].value,
                "custom_quota": {
                    "limits.cpu": w.children[4].children[0].value,
                    "requests.cpu": w.children[4].children[1].value,
                    "limits.memory": w.children[4].children[2].value,
                    "requests.memory": w.children[4].children[3].value,
                    "requests.storage": w.children[4].children[4].value,
                    "count/objectbucketclaims.objectbucket.io": w.children[4].children[5].value
                },

            }
        }
    }

    divider = widgets.Output(layout={'border': '1px solid black'})

    # Users:
    user_creator = spec['users']
    spec['users'] = []
    users = dyamic_line(spec['users'], user_creator)

    # Namespaces
    ns_creator = spec['namespaces']
    spec['namespaces'] = []
    namespaces = dyamic_line(spec['namespaces'], ns_creator)

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
        divider,
        namespaces,
        # DONE
        done_button,
    ]



    return widgets.VBox(form), spec
