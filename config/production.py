import dotenv
import os
from .settings import *

dotenv.load_dotenv()

DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': SUPABASE_USER,
        'PASSWORD': SUPABASE_PASSWORD,
        'HOST': 'aws-0-ap-northeast-1.pooler.supabase.com',
        'PORT': '5432',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'