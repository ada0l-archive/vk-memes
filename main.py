import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.settings import settings
from backend.mem.api import router as mem
from backend.user.api import router as user
from backend.stat.api import router as stat

settings.configure_logging()

app = FastAPI(**settings.fastapi_kwargs)

if settings.allowed_hosts:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@app.on_event("startup")
async def startup_event():
    print("Starting up...")

app.include_router(mem)
app.include_router(user)
app.include_router(stat)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa
