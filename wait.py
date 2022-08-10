from index import app
from waitress import serve

#if __name__ == "__main__":
#    app.title = 'Litmus'
#    app.run_server(debug=False)
serve(app.server, host="0.0.0.0", port=8050)
