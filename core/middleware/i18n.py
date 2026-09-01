import gettext
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Custom Translation Middleware class
class I18NMiddleware(BaseHTTPMiddleware):
    """Translate responses base on accep-language header
    """
    def __init__(self, app, locales_path: str, default_locale: str = "en"):
        super().__init__(app)
        self.locales_path = locales_path
        self.default_locale = default_locale

    async def dispatch(self, request: Request, call_next):
        # 1.Gets language from eccept-language header
        accept_language = request.headers.get("accept-language", self.default_locale)
        # 2.Expected output from header is: "en-US,en;q=0.9" -> which we only need the first part
        lang = accept_language.split(",")[0].split("-")[0]

        # 3.Giving value to gettext for accepted language 
        try:
            translation = gettext.translation(
                "messages", 
                localedir=self.locales_path, 
                languages=[lang],
                fallback=True
            )
        except FileNotFoundError:
            # 4.If language translation file doesn't exists, rollback to default language translation file
            translation = gettext.translation(
                "messages", 
                localedir=self.locales_path, 
                languages=[self.default_locale],
                fallback=True
            ) 

        # 5.Injecting translation to request.state for access to them in endponits
        request.state._ = translation.gettext

        response = await call_next(request)
        return response
