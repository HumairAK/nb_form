from ipywidgets import interact, interactive, widgets


def generate_form_a(clusters, envs):
    form = {
        'clusters': widgets.Dropdown(options=clusters, value=clusters[0], description='Cluster:', disabled=False),
        'env': widgets.Dropdown(options=envs, value=envs[0], description='Environment:', disabled=False),
        'desc': widgets.Textarea(value='Enter your project description here.', description='Description:',
                                 disabled=False, ),

    }
    silence_out = [display(i) for i in form.values()]

    namespaces = []

    def add_btn_clicked(b):
        input_box.children = (input_box.children[0], line()) + input_box.children[1:]

    def delete_btn_clicked(b):
        b.parent.layout.display = 'none'

    def line():
        deleteButton = widgets.Button(icon="trash")
        deleteButton.on_click(delete_btn_clicked)

        namespaces = []
        namespaces.append(widgets.Text(value='Your-Namespace-Name', description='Namespace:'))
        namespaces.append(widgets.Checkbox(value=False, description='Monitoring:'))
        namespaces.append(widgets.Dropdown(options=['small', 'large', 'custom'], description='Quota:'))
        container = widgets.HBox()
        deleteButton.parent = container
        for widg in namespaces:
            widg.parent = container
        children = namespaces + [deleteButton]
        container.children = children
        return container

    add = widgets.Button(description="Add Namespace", icon="plus-circle")
    add.on_click(add_btn_clicked)

    input_box = widgets.VBox([line(), add])

    display(input_box)