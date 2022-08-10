import dash

app = dash.Dash(__name__)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server = app.server
