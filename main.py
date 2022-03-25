from forms.form_generator import generate_form

clusters = ['balrog', 'curator', 'demo', 'morty', 'ocp-prod', 'ocp-staging', 'osc-cl1', 'osc-cl2', 'rick', 'smaug']
envs = ['dev', 'emea', 'moc', 'octo', 'osc']

generate_form(clusters, envs)