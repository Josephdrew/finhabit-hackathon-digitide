from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from firebase_admin import credentials, initialize_app, auth
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from .core.database import get_db, engine, Base
from . import crud
from .schemas.user import UserCreate
from .auth_utils import create_access_token, create_refresh_token, decode_token



# ✅ Initialize Firebase Admin SDK once
cred = credentials.Certificate("app/firebase_credentials.json")
initialize_app(cred)

# Pydantic models for requests
class TokenRequest(BaseModel):
    firebase_id_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# ✅ Define FastAPI app only once
app = FastAPI(
    title="FinHabit API",
    description="API for managing users, OTPs, and financial data",
    version="1.0.0",
    docs_url="/swagger-ui.html",
    redoc_url=None,
    openapi_url="/v3/api-docs",
    lifespan=lifespan
)

# ✅ Add BearerAuth security scheme to OpenAPI so Swagger UI shows "Authorize" button
def custom_api():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply BearerAuth globally (optional)
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_api


# ----------------------------- AUTH ROUTES ---------------------------------------
@app.post("/firebase-login")
async def firebase_login(token_request: TokenRequest, db: AsyncSession = Depends(get_db)):
    try:
        decoded_token = auth.verify_id_token(token_request.firebase_id_token)
        uid = decoded_token.get("uid")
        phone_number = decoded_token.get("phone_number")

        if not phone_number:
            raise HTTPException(status_code=400, detail="Phone number not found in token")

        user = await crud.get_user_by_phone(db, phone_number)
        if not user:
            await crud.create_user(
                db,
                UserCreate(
                    name="Firebase User",
                    email=f"{phone_number}@example.com",
                    phone=phone_number
                )
            )

        user_data = {"sub": uid, "phone": phone_number}
        access_token, access_expiry = create_access_token(user_data)
        refresh_token, refresh_expiry = create_refresh_token(user_data)

        return {
            "message": "Authenticated!",
            "access_token": access_token,
            "access_token_expires_at": access_expiry.isoformat(),
            "refresh_token": refresh_token,
            "refresh_token_expires_at": refresh_expiry.isoformat(),
            "user": user_data
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Firebase ID token: {e}")

@app.post("/refresh-token")
async def refresh_token(req: RefreshRequest):
    try:
        decoded = decode_token(req.refresh_token)
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_data = {
            "sub": decoded.get("sub"),
            "phone": decoded.get("phone"),
        }

        new_access_token, new_access_expiry = create_access_token(user_data)
        return {
            "access_token": new_access_token,
            "access_token_expires_at": new_access_expiry.isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token: {e}")

@app.get("/")
async def root():
    return {"message": "API is running"}
