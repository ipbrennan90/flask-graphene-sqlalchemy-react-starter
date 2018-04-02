from flask import Flask, render_template
from flask_graphql import GraphQLView

from models.foundation import db_session
from graph.schema import schema

import logging

app = Flask(__name__, static_folder="../static/dist",
            template_folder="../static")
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


@app.route('/')
def index():
    return render_template("index.html")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
