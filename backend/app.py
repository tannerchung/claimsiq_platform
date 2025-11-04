from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import claims, analytics
from backend.services.data_service import DataService

app = FastAPI(title="ClaimsIQ API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(claims.router, prefix="/api", tags=["claims"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])

@app.on_event("startup")
async def startup_event():
    print("Starting ClaimsIQ API...")
    DataService.refresh_cache()
    print("Data cache loaded successfully")

@app.get("/")
async def root():
    return {"message": "ClaimsIQ API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
