from pathlib import Path
from fastapi_babel import Babel, BabelConfigs

# TODO: This two variables need to be moved to application settings
I18N_DIR = Path(__file__).resolve().parent
LOCALES_DIR = I18N_DIR / "locales"
DEFAULT_LOCALE = "en"
SUPPORTED_LOCALES: tuple[str, ...] = ("en", "fa", "fr")

babel_configs = BabelConfigs(
    ROOT_DIR=str(I18N_DIR),
    BABEL_DEFAULT_LOCALE=DEFAULT_LOCALE,
    BABEL_TRANSLATION_DIRECTORY=str(LOCALES_DIR),
)

babel = Babel(configs=babel_configs)
