"""
Data management routes for ClaimsIQ.

Endpoints for loading Kaggle data and generating synthetic data.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os

# Add scripts directory to path so we can import load_sample_data
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../scripts'))

try:
    from load_sample_data import download_kaggle_data, generate_sample_data, load_data_to_db
except ImportError as e:
    print(f"Warning: Could not import data loading functions: {e}")
    download_kaggle_data = None
    generate_sample_data = None
    load_data_to_db = None

router = APIRouter()


class DataLoadResponse(BaseModel):
    success: bool
    message: str
    claims_count: int = 0
    providers_count: int = 0


@router.post("/load-kaggle", response_model=DataLoadResponse)
async def load_kaggle_dataset():
    """
    Download and load real insurance data from Kaggle.

    Requires kaggle.json to be configured.
    Returns the number of claims and providers loaded.
    """
    if not download_kaggle_data or not load_data_to_db:
        raise HTTPException(
            status_code=500,
            detail="Data loading functions not available"
        )

    try:
        # Download from Kaggle
        claims_df, providers_df = download_kaggle_data()

        if claims_df is None or providers_df is None:
            return DataLoadResponse(
                success=False,
                message="Failed to download Kaggle dataset. Check kaggle.json configuration.",
                claims_count=0,
                providers_count=0
            )

        # Load to database
        load_data_to_db(claims_df, providers_df)

        return DataLoadResponse(
            success=True,
            message=f"Successfully loaded Kaggle dataset!",
            claims_count=len(claims_df),
            providers_count=len(providers_df)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading Kaggle data: {str(e)}"
        )


@router.post("/generate-sample", response_model=DataLoadResponse)
async def generate_sample_dataset(num_claims: int = 1000):
    """
    Generate realistic synthetic insurance claims data.

    Args:
        num_claims: Number of claims to generate (default: 1000)

    Returns the number of claims and providers generated.
    """
    if not generate_sample_data or not load_data_to_db:
        raise HTTPException(
            status_code=500,
            detail="Data loading functions not available"
        )

    # Validate num_claims
    if num_claims < 1 or num_claims > 100000:
        raise HTTPException(
            status_code=400,
            detail="num_claims must be between 1 and 100,000"
        )

    try:
        # Generate synthetic data
        claims_df, providers_df = generate_sample_data(num_claims)

        # Load to database
        load_data_to_db(claims_df, providers_df)

        return DataLoadResponse(
            success=True,
            message=f"Successfully generated {num_claims} synthetic claims!",
            claims_count=len(claims_df),
            providers_count=len(providers_df)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating sample data: {str(e)}"
        )


@router.post("/clear-data", response_model=DataLoadResponse)
async def clear_database():
    """
    Clear all claims and providers from the database.

    WARNING: This will delete all data!
    """
    from sqlalchemy import create_engine, text

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///claimsiq.db")

    try:
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            # Delete all claims
            result_claims = conn.execute(text("DELETE FROM claims"))
            claims_deleted = result_claims.rowcount

            # Delete all providers
            result_providers = conn.execute(text("DELETE FROM providers"))
            providers_deleted = result_providers.rowcount

            conn.commit()

        return DataLoadResponse(
            success=True,
            message=f"Cleared {claims_deleted} claims and {providers_deleted} providers",
            claims_count=0,
            providers_count=0
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing database: {str(e)}"
        )
