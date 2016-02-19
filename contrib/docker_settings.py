import os

DEBUG = False
ASSETS_DEBUG = False
CACHE = False
SECRET_KEY = os.environ.get('ALEPH_SECRET_KEY')

APP_TITLE = os.environ.get('ALEPH_APP_TITLE', 'Aleph')
APP_NAME = os.environ.get('ALEPH_APP_NAME', 'aleph')
FAVICON = 'https://investigativedashboard.org/static/favicon.ico'

ELASTICSEARCH_URL = os.environ.get('ALEPH_ELASTICSEARCH_URI')

SQLALCHEMY_DATABASE_URI = os.environ.get('ALEPH_DATABASE_URI')
PREFERRED_URL_SCHEME = 'http'

MAIL_FROM = os.environ.get('MAIL_FROM')
MAIL_HOST = os.environ.get('MAIL_HOST')
MAIL_ADMINS = [os.environ.get('MAIL_ADMIN')]
MAIL_CREDENTIALS = (os.environ.get('MAIL_USERNAME'),
                    os.environ.get('MAIL_PASSWORD'))

CELERY_BROKER_URL = os.environ.get('ALEPH_BROKER_URI')
CELERY_SEND_TASK_ERROR_EMAILS = True
ADMINS = ((APP_TITLE, MAIL_ADMINS[0]),)
SERVER_EMAIL = MAIL_FROM
EMAIL_HOST = MAIL_HOST
EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = MAIL_CREDENTIALS
EMAIL_USE_TLS = True

CELERY_RESULT_PERSISTENT = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_IGNORE_RESULT = True
CELERYD_MAX_TASKS_PER_CHILD = 100

ARCHIVE_TYPE = os.environ.get('ALEPH_ARCHIVE_TYPE')
ARCHIVE_AWS_KEY_ID = os.environ.get('ALEPH_AWS_ACCESS_KEY_ID')
ARCHIVE_AWS_SECRET = os.environ.get('ALEPH_AWS_SECRET_ACCESS_KEY')
ARCHIVE_BUCKET = os.environ.get('ALEPH_ARCHIVE_BUCKET')
ARCHIVE_PATH = os.environ.get('ALEPH_ARCHIVE_PATH')
ARCHIVE_B2_ACCOUNT_ID = os.environ.get('ALEPH_B2_ACCOUNT_ID')
ARCHIVE_B2_KEY = os.environ.get('ALEPH_B2_KEY')

TWITTER_API_KEY = os.environ.get('ALEPH_TWITTER_API_KEY')
TWITTER_API_SECRET = os.environ.get('ALEPH_TWITTER_API_SECRET')

FACEBOOK_APP_ID = os.environ.get('ALEPH_FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.environ.get('ALEPH_FACEBOOK_APP_SECRET')

SPINDLE_URL = os.environ.get('ALEPH_SPINDLE_HOST', 'https://search.occrp.org/')
SPINDLE_API_KEY = os.environ.get('ALEPH_SPINDLE_API_KEY')

ID_HOST = 'https://www.investigativedashboard.org/'
ID_USERNAME = os.environ.get('ALEPH_ID_USERNAME')
ID_PASSWORD = os.environ.get('ALEPH_ID_PASSWORD')


OAUTH = {
    'consumer_key': os.environ.get('ALEPH_OAUTH_KEY'),
    'consumer_secret': os.environ.get('ALEPH_OAUTH_SECRET'),
    'request_token_params': {
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    'base_url': 'https://www.googleapis.com/oauth2/v1/',
    'request_token_url': None,
    'access_token_method': 'POST',
    'access_token_url': 'https://accounts.google.com/o/oauth2/token',
    'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
}
