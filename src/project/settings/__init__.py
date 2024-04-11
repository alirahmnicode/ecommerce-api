import os.path
from pathlib import Path

from split_settings.tools import optional, include


BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "project/templates")],
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

ENVVAR_SETTINGS_PREFIX = "CORESETTINGS_"


LOCAL_SETTINGS_PATH = os.getenv(f"{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH")


if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = "local/settings.dev.py"

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)


include("base.py", "custom.py", optional(LOCAL_SETTINGS_PATH), "envvars.py")
