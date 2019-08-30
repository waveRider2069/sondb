import os

from flask import Flask
from datetime import timedelta
from math import log2


# binascii.hexlify(os.urandom(16)).decode()
# 产生随机字符串


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     # SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.db')
    # )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.cfg', silent=True)
        app.config.from_mapping(PERMANENT_SESSION_LIFETIME=timedelta(days=1), SECRET_KEY='Sm9obiBTY2hyb20ga2lja3MgYXNz',
                                DEBUG=True, ENV='development')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth, db, projects, subject, consult
    db.init_app(app)
    # app.teardown_appcontext(db.close_db())
    # def close_database():
    #     db.close_db()
    app.register_blueprint(auth.bp)
    app.register_blueprint(subject.bp)
    app.register_blueprint(consult.bp)
    app.register_blueprint(projects.bp)

    @app.template_filter('log2')
    def mathlog2(x):
        return log2(x)

    # app.register_blueprint(consult.bp)
    # with app.test_client() as c:
    #     rv = c.get('/?vodka=42')
    #     assert request.args['vodka'] == '42'

    return app

# # create and configure the app
# app = Flask(__name__, instance_relative_config=True)
# # app.config.from_mapping(
# #     # SECRET_KEY='dev',
# #     DATABASE=os.path.join(app.instance_path, 'flaskr.db')
#
# test_config = None
# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.cfg', silent=True)
#     app.config.from_mapping(PERMANENT_SESSION_LIFETIME=timedelta(days=1), SECRET_KEY='Sm9obiBTY2hyb20ga2lja3MgYXNz',
#                             DEBUG=True, ENV='development')
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)
# # ensure the instance folder exists
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass
# import sondb.auth as auth
# import sondb.db as db
# import sondb.projects as projects
# import sondb.subject as subject
# import sondb.consult as consult
#
# # from . import auth, db, projects, subject, consult
# db.init_app(app)
# # app.teardown_appcontext(db.close_db())
# # def close_database():
# #     db.close_db()
# app.register_blueprint(auth.bp)
# app.register_blueprint(subject.bp)
# app.register_blueprint(consult.bp)
# app.register_blueprint(projects.bp)
#
# @app.template_filter('log2')
# def mathlog2(x):
#     return log2(x)
#
# # app.register_blueprint(consult.bp)
# # with app.test_client() as c:
# #     rv = c.get('/?vodka=42')
# #     assert request.args['vodka'] == '42'
# if __name__ == '__main__':
#     app.run()