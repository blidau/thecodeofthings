from .base import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["thecodeofthings.com", "www.thecodeofthings.com"]

try:
    from .local import *
except ImportError:
    pass
