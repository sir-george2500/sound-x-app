from fastapi import FastAPI
from routes.routes import router as user_router

app = FastAPI(title="User Authentication Services", docs_url="/")

app.include_router(user_router, prefix="/api")


