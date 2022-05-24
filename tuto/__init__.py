import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    """
    instance_relative_config=True tells the app that configuration files 
    are relative to the instance folder. 
    The instance folder is located outside the tuto package and can hold 
    local data that shouldn’t be committed to version control, such as 
    configuration secrets and the database file.
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tuto.sqlite')
    )

    if test_config is None:
        # load instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed
        app.config.from_mapping(test_config)


    """
    os.makedirs() ensures that app.instance_path exists. 
    Flask doesn’t create the instance folder automatically, 
    but it needs to be created because your project will create 
    the SQLite database file there.
    """
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple route to start
    @app.route('/hola')
    def hola():
        return 'Hola, mundo!'

    from . import db
    db.init_app(app)

    from . import mongo
    mongo.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import escuelas
    app.register_blueprint(escuelas.bp)

    return app