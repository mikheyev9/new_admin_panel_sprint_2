from pathlib import Path

from split_settings.tools import include
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

include(
    'settings_components/base.py',
    'settings_components/database.py',
    'settings_components/auth.py',
    'settings_components/static.py',
    'settings_components/install_apps.py',
    'settings_components/middleware.py',
    'settings_components/templates.py',
    'settings_components/logging.py',
    'settings_components/corsheaders.py',
)