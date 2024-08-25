from website import create_app
# import flask_whooshalchemy as wa
# from flask_sqlalchemy import SQLAlchemy


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
