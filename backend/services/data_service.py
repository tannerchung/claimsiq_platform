import pandas as pd
from sqlalchemy import create_engine, text
from backend.config import DATABASE_URL
from typing import Optional, Dict, Any

class DataService:
    _claims_cache: Optional[pd.DataFrame] = None
    _providers_cache: Optional[pd.DataFrame] = None
    
    @staticmethod
    def load_claims_from_csv(filepath: str) -> pd.DataFrame:
        df = pd.read_csv(filepath)
        DataService._claims_cache = df
        return df
    
    @staticmethod
    def load_claims_from_db() -> pd.DataFrame:
        engine = create_engine(DATABASE_URL)
        try:
            df = pd.read_sql_table('claims', engine)
            df = DataService._ensure_claim_columns(df)
            DataService._claims_cache = df
            return df
        except Exception as e:
            print(f"Error loading claims from database: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def get_claims() -> pd.DataFrame:
        if DataService._claims_cache is None:
            DataService.load_claims_from_db()
        return DataService._claims_cache if DataService._claims_cache is not None else pd.DataFrame()
    
    @staticmethod
    def load_providers_from_db() -> pd.DataFrame:
        engine = create_engine(DATABASE_URL)
        try:
            df = pd.read_sql_table('providers', engine)
            DataService._providers_cache = df
            return df
        except Exception as e:
            print(f"Error loading providers from database: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def get_providers() -> pd.DataFrame:
        if DataService._providers_cache is None:
            DataService.load_providers_from_db()
        return DataService._providers_cache if DataService._providers_cache is not None else pd.DataFrame()
    
    @staticmethod
    def refresh_cache():
        DataService.load_claims_from_db()
        DataService.load_providers_from_db()

    @staticmethod
    def _ensure_claim_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Guarantee optional columns exist so downstream code can rely on them."""
        required_defaults: Dict[str, Any] = {
            "denial_reason": None,
            "days_to_process": 0,
            "processed_date": None,
            "processor_notes": None,
        }
        for column, default in required_defaults.items():
            if column not in df.columns:
                df[column] = default
        return df

    @staticmethod
    def update_claim_record(claim_id: str, updates: Dict[str, Any]) -> int:
        """Persist claim updates to the database."""
        if not updates:
            return 0

        set_clause = ", ".join(f"{column} = :{column}" for column in updates)
        params = {**updates, "claim_id": claim_id}

        engine = create_engine(DATABASE_URL)
        with engine.begin() as conn:
            result = conn.execute(
                text(f"UPDATE claims SET {set_clause} WHERE id = :claim_id"),
                params,
            )
        return result.rowcount or 0

    @staticmethod
    def update_claim_cache(claim_id: str, updates: Dict[str, Any]) -> None:
        """Update the in-memory claims cache with new values."""
        df = DataService._claims_cache
        if df is None or df.empty:
            return

        mask = df["id"] == claim_id
        if mask.any():
            for column, value in updates.items():
                if column not in df.columns:
                    df[column] = None
                df.loc[mask, column] = value
