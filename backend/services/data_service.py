import pandas as pd
from sqlalchemy import create_engine
from backend.config import DATABASE_URL
from typing import Optional

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
            DataService._claims_cache = df
            return df
        except Exception as e:
            print(f"Error loading claims from database: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def get_claims() -> pd.DataFrame:
        if DataService._claims_cache is None or DataService._claims_cache.empty:
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
        if DataService._providers_cache is None or DataService._providers_cache.empty:
            DataService.load_providers_from_db()
        return DataService._providers_cache if DataService._providers_cache is not None else pd.DataFrame()
    
    @staticmethod
    def refresh_cache():
        DataService.load_claims_from_db()
        DataService.load_providers_from_db()
