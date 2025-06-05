from fastapi import FastAPI
from app.api.routes.user import router as user_routers
from app.api.routes.auth import router as auth_routers
from app.core.exception_handlers import init_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Skynect",
        version="0.1.0",
        description="High-scale chat app with user connection and messaging features.",
    )

    # Import and include routers here later
    app.include_router(user_routers)
    app.include_router(auth_routers)
    
    # Exception Handlers
    init_exception_handlers(app)

    @app.get("/")
    def root():
        return {"message": "Welcome to Skynect 🔗"}

    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    print("🔥 Skynect API is running and DB is ready to connect...")
