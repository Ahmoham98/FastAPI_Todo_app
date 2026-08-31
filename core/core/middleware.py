import time
from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
# از HTTPSRedirectMiddleware هم اگر خواستید می‌توانید استفاده کنید
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

def setup_middlewares(app: FastAPI) -> None:
    """setting all application middlewares 

    Args:
        app (FastAPI): Your application object
    """

    # 1. Trusted hosts settings
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1", "*.example.com"] # set your allowed hosts here
    )

    # 2. Responses conmpression
    app.add_middleware(
        GZipMiddleware, 
        minimum_size=1000, 
        compresslevel=5
    )

    # 3.CORS settings
    origins = [
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 4.Custom middleware for process-time calculation
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # 5.Redirect middleware (you can Activate it if required)
    # app.add_middleware(HTTPSRedirectMiddleware)
