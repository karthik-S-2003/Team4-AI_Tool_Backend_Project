from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import Base, engine, SessionLocal
from app.admin.routes import router as admin_router
from app.user.routes import router as user_router
from app.models import Admin
from app.auth import get_password_hash
from fastapi.middleware.cors import CORSMiddleware




@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == "admin").first()
        if not admin:
            admin = Admin(
                username="admin",
                hashed_password=get_password_hash("password123")
            )
            db.add(admin)
            db.commit()
            print("Admin auto-created")
        else:
            print("Admin already exists")
    finally:
        db.close()

    yield


app = FastAPI(
    title="AI Tool Finder",
    lifespan=lifespan
)

app.include_router(admin_router)
app.include_router(user_router)

# Create tables once
Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "Welcome to Backend AiTools Project !!!"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
