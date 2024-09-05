from pathlib import Path
from environ import Env


BASE_DIR = Path(__file__).resolve().parent.parent

# ENVIRONMENT VARIABLE.

env = Env()
Env.read_env()

ENVIRONMENT = env("ENVIRONMENT", default="production")


# SECURITY KEY.

SECRET_KEY = env("SECRET_KEY")

ENCRYPT_KEY = env("ENCRYPT_KEY")


# SECURITY MODE.

DEBUG = ENVIRONMENT == "development"

ALLOWED_HOSTS = []


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
    "django.contrib.sites",
    "admin_honeypot",
    "allauth",
    "django_htmx",
    "allauth.account",
    "allauth.socialaccount",
    "django_cleanup.apps.CleanupConfig",
    "a_posts",
    "a_users",
    "a_inbox",
    "a_rtchat",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media"


# DEFAULT PRIMARY KEY FIELD TYPE.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# EMAIL CONFIGURATION.

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = env("EMAIL_ADDRESS")

EMAIL_HOST_PASSWORD = env("EMAIL_PASSWORD")

EMAIL_PORT = 587

EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = f'Awesome {env("EMAIL_ADDRESS")}'

ACCOUNT_EMAIL_SUBJECT_PREFIX = ""


# ADDITIONAL CONFIGURATION.

LOGIN_REDIRECT_URL = "home"

ACCOUNT_AUTHENTICATION_METHOD = "email"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_SIGNUP_REDIRECT_URL = "profile-onboarding"

ACCOUNT_USERNAME_BLACKLIST = [
    "admin",
    "administrator",
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
