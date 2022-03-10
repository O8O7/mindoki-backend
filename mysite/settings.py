from pathlib import Path
from datetime import timedelta, datetime
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'djoser',
    'markdownx',
    'friendship',
    'rest_framework',
    'rest_framework.authtoken',

    'account',
    'article',
    'portfolio',
    'question',
    'common',

    # AWS S3用パッケージ
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': '',
        'HOST': 'host',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# collectstatic展開用の静的ファイルを収集するディレクトリへの絶対パス
STATIC_ROOT = BASE_DIR / 'staticfiles/'
# STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.UserAccount'

CORS_ORIGIN_WHITELIST = (
    'http://localhost',
    'http://localhost:3000',
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
)

# 自分独自の設定
DJANGO_DOMAIN = ('http://localhost:8000')

DOMAIN = ('localhost:3000')


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 10件ごとにページが分けられる
    'PAGE_SIZE': 3,
    # 認証が必要
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # JWT認証
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.TokenAuthentication",
    ],
    'DATETIME_FORMAT': '%Y/%m/%d/%H:%M',
}

SIMPLE_JWT = {
    # アクセストークン(1時間)
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    # リフレッシュトークン(3日)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    # 認証タイプ
    'AUTH_HEADER_TYPES': ('JWT', ),
    # 認証トークン
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', ),
}


DJOSER = {
    # メールアドレスでログイン
    'LOGIN_FIELD': 'email',
    # アカウント本登録メール
    'SEND_ACTIVATION_EMAIL': True,
    # アカウント本登録完了メール
    'SEND_CONFIRMATION_EMAIL': True,
    # メールアドレス変更完了メール
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    # パスワード変更完了メール
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    # アカウント登録時に確認用パスワード必須
    'USER_CREATE_PASSWORD_RETYPE': True,
    # メールアドレス変更時に確認用メールアドレス必須
    'SET_USERNAME_RETYPE': True,
    # パスワード変更時に確認用パスワード必須
    'SET_PASSWORD_RETYPE': True,
    # 'USERNAME_RESET_CONFIRM_RETYPE': True,
    # 確認用メールがない場合は400エラーが出る
    # 'USERNAME_RESET_SHOW_EMAIL_NOT_FOUND': True,
    # アカウント本登録用URL
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    # メールアドレスリセット完了用URL
    'USERNAME_RESET_CONFIRM_URL': 'email_reset/{uid}/{token}',
    # パスワードリセット完了用URL
    'PASSWORD_RESET_CONFIRM_URL': 'password_reset/{uid}/{token}',
    # カスタムユーザー用シリアライザー
    'SERIALIZERS': {
        'user_create':  'account.serializers.UserSerializer',
        'user':         'account.serializers.UserSerializer',
        # 'current_user': 'account.serializers.UserSerializer',
        'current_user': 'account.serializers.UserProfileSerializer',
    },
    'EMAIL': {
        # アカウント本登録
        'activation':                    'account.email.ActivationEmail',
        # アカウント本登録完了
        'confirmation':                  'account.email.ConfirmationEmail',
        # パスワードリセット
        'password_reset':                'account.email.PasswordResetEmail',
        # パスワードリセット完了
        'password_changed_confirmation': 'account.email.PasswordChangedConfirmationEmail',
        # メールアドレスリセット完了
        'username_changed_confirmation': 'account.email.UsernameChangedConfirmationEmail',
        # メールアドレスリセット
        'username_reset':                'account.email.UsernameResetEmail',
    }
}

# markdownxのオプション設定
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',    # テーブル、コードハイライト
    'markdown.extensions.toc',      # 目次
    'markdown.extensions.nl2br',    # 改行
]

# markdownxの画像保存パス
MARKDOWNX_MEDIA_PATH = datetime.now().strftime('markdownx/%Y/%m/%d')

try:
    from .local_settings import *
except ImportError:
    pass

if not DEBUG:
    # SendGrid
    SECRET_KEY = os.environ['SECRET_KEY']
    EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
    # 送信元メールアドレス
    DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
    # # SendGridのAPIキー
    SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
    # # 本番環境用
    SENDGRID_SANDBOX_MODE_IN_DEBUG = False
    # # URLのトラッキングをOFF
    # # SENDGRID_TRACK_CLICKS_PLAIN = False
    SENDGRID_TRACK_CLICKS_PLAIN = True
    SENDGRID_ECHO_TO_STDOUT = False
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = S3_URL
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None

    import django_heroku
    django_heroku.settings(locals())

    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES['default'].update(db_from_env)
