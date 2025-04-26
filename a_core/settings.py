import dj_database_url
from pathlib import Path
from environ import Env
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent

# ENVIRONMENT VARIABLE.

env = Env()
Env.read_env(".env")

ENVIRONMENT = env("ENVIRONMENT", default="development")


# SECURITY KEY.

SECRET_KEY = env("SECRET_KEY", default=None)
if SECRET_KEY is None:
    raise ImproperlyConfigured("SECRET_KEY is missing!")

ENCRYPT_KEY = env("ENCRYPT_KEY", default=None)
if ENCRYPT_KEY is None:
    raise ImproperlyConfigured("ENCRYPT_KEY is missing!")


# SECURITY MODE.

DEBUG = ENVIRONMENT == "development"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INTERNAL_IPS = ["127.0.0.1"]

if not DEBUG:
    LIVE_HOST = env("LIVE_HOST", None)
    if LIVE_HOST is None:
        raise ImproperlyConfigured("LIVE_HOST is missing!")

    ALLOWED_HOSTS.append(LIVE_HOST)

    CSRF_TRUSTED_ORIGINS = [f"https://{LIVE_HOST}"]


# APPLICATION DEFINITION.

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "django.contrib.sites",
    "django_cleanup.apps.CleanupConfig",
    "django_htmx",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.twitter",
    "allauth.socialaccount.providers.facebook",
    "a_posts",
    "a_users",
    "a_inbox",
    "a_rtchat",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "a_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# SOCIAL ACCOUNT.

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env("OAUTH_GOOGLE_CLIENT_ID"),
            "secret": env("OAUTH_GOOGLE_CLIENT_SECRET"),
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online", "prompt": "consent"},
    },
    "github": {
        "APP": {
            "client_id": env("OAUTH_GITHUB_CLIENT_ID"),
            "secret": env("OAUTH_GITHUB_CLIENT_SECRET"),
        }
    },
    "twitter": {
        "APP": {
            "client_id": env("OAUTH_TWITTER_CLIENT_ID"),
            "secret": env("OAUTH_TWITTER_CLIENT_SECRET"),
        }
    },
    "facebook": {
        "APP": {
            "client_id": env("OAUTH_FACEBOOK_CLIENT_ID"),
            "secret": env("OAUTH_FACEBOOK_CLIENT_SECRET"),
        }
    },
}

SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_EMAIL_AUTHENTICATION = False

SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = False

SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

ACCOUNT_ADAPTER = "a_users.adapters.CustomAccountAdapter"

SOCIALACCOUNT_ADAPTER = "a_users.adapters.CustomSocialAccountAdapter"


# WEBSOCKET CONFIGURATION.

# WSGI_APPLICATION = "a_core.wsgi.application"

ASGI_APPLICATION = "a_core.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}


# DATABASE.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

USE_REMOTE_DATABASE_LOCALLY = False

if not DEBUG or USE_REMOTE_DATABASE_LOCALLY:
    DATABASE_URL = env("DATABASE_URL", default=None)
    if DATABASE_URL is None:
        raise ImproperlyConfigured("DATABASE_URL is missing!")

    DATABASES["default"] = dj_database_url.parse(DATABASE_URL)


# PASSWORD VALIDATION.

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# INTERNATIONALIZATION.

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# STATIC FILES (CSS, JAVASCRIPT, IMAGES).

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"

if not DEBUG or USE_REMOTE_DATABASE_LOCALLY:
    STORAGES["default"] = {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    }

    CLOUDINARY_CLOUD_NAME = env("CLOUDINARY_CLOUD_NAME", None)
    if CLOUDINARY_CLOUD_NAME is None:
        raise ImproperlyConfigured("CLOUDINARY_CLOUD_NAME is missing!")

    CLOUDINARY_API_KEY = env("CLOUDINARY_API_KEY", None)
    if CLOUDINARY_API_KEY is None:
        raise ImproperlyConfigured("CLOUDINARY_API_KEY is missing!")

    CLOUDINARY_API_SECRET = env("CLOUDINARY_API_SECRET", None)
    if CLOUDINARY_API_SECRET is None:
        raise ImproperlyConfigured("CLOUDINARY_API_SECRET is missing!")

    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
        "API_KEY": CLOUDINARY_API_KEY,
        "API_SECRET": CLOUDINARY_API_SECRET,
    }
else:
    MEDIA_ROOT = BASE_DIR / "media"


# DEFAULT PRIMARY KEY FIELD TYPE.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# EMAIL CONFIGURATION.

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if not DEBUG:
    EMAIL_HOST_USER = env("MAIL_USERNAME", default=None)
    if EMAIL_HOST_USER is None:
        raise ImproperlyConfigured("MAIL_USERNAME is missing!")

    EMAIL_HOST_PASSWORD = env("MAIL_PASSWORD", default=None)
    if EMAIL_HOST_PASSWORD is None:
        raise ImproperlyConfigured("MAIL_PASSWORD is missing!")

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    EMAIL_HOST = "smtp.gmail.com"

    EMAIL_PORT = 587

    EMAIL_USE_TLS = True

    DEFAULT_FROM_EMAIL = f"Awesome {EMAIL_HOST_USER}"

    ACCOUNT_EMAIL_SUBJECT_PREFIX = ""


# ADDITIONAL CONFIGURATION.

AUTH_USER_MODEL = "a_users.User"

LOGIN_REDIRECT_URL = "home"

ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_LOGIN_METHODS = ["username", "email"]

ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]

ACCOUNT_SIGNUP_REDIRECT_URL = "profile-onboarding"

ACCOUNT_LOGOUT_REDIRECT_URL = "home"

ACCOUNT_USERNAME_BLACKLIST = [
    "admin",
    "accounts",
    "inbox",
    "chat",
    "category",
    "post",
    "profile",
    "comment_sent",
    "comment",
    "reply_sent",
    "reply",
]
