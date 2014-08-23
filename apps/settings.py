"""
settings.py

Configuration for Flask app

"""


class Config(object):
	# Set secret key to use session
	SECRET_KEY = "likelion-flaskr-secret-key"
	debug = False


class Production(Config):
	debug = True
	CSRF_ENABLED = False
	ADMIN = "ksb5529@gmail.com"
	SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///blog?instance=kimsangbum890616:ll-personal-blog4'
	migration_directory = "migrations"

