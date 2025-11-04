import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import random
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///claimsiq.db")

def generate_sample_data(num_claims=1000):
    print(f"Generating {num_claims} sample claims...")
    
    statuses = ['pending', 'approved', 'denied', 'flagged']
    status_weights = [0.3, 0.5, 0.15, 0.05]
    
    providers = [f'PROV-{i:03d}' for i in range(1, 51)]
    provider_names = [f'Provider {i}' for i in range(1, 51)]
    
    claims_data = []
    
    for i in range(num_claims):
        claim_date = datetime.now() - timedelta(days=random.randint(0, 365))
        claim_amount = round(random.uniform(100, 15000), 2)
        status = random.choices(statuses, weights=status_weights)[0]
        provider_id = random.choice(providers)
        
        approved_amount = None
        if status == 'approved':
            approved_amount = round(claim_amount * random.uniform(0.7, 1.0), 2)
        
        claims_data.append({
            'id': f'CLM-{i+1:06d}',
            'policy_id': f'POL-{random.randint(1, 500):05d}',
            'claim_date': claim_date.strftime('%Y-%m-%d'),
            'claim_amount': claim_amount,
            'approved_amount': approved_amount,
            'status': status,
            'provider_id': provider_id,
            'procedure_codes': f'CPT-{random.randint(10000, 99999)}',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    claims_df = pd.DataFrame(claims_data)
    
    providers_data = []
    for i, provider_id in enumerate(providers):
        providers_data.append({
            'id': provider_id,
            'npi': f'{random.randint(1000000000, 9999999999)}',
            'name': provider_names[i],
            'type': random.choice(['Hospital', 'Clinic', 'Lab', 'Pharmacy']),
            'specialty': random.choice(['General', 'Cardiology', 'Orthopedics', 'Radiology'])
        })
    
    providers_df = pd.DataFrame(providers_data)
    
    return claims_df, providers_df

def load_data_to_db(claims_df, providers_df):
    print(f"Loading data to database at {DATABASE_URL}...")
    engine = create_engine(DATABASE_URL)
    
    claims_df.to_sql('claims', engine, if_exists='replace', index=False)
    print(f"Loaded {len(claims_df)} claims")
    
    providers_df.to_sql('providers', engine, if_exists='replace', index=False)
    print(f"Loaded {len(providers_df)} providers")
    
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_status ON claims(status)
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_date ON claims(claim_date)
        """))
        conn.commit()
        print("Created indexes")
    
    print("Data loading complete!")

if __name__ == "__main__":
    claims_df, providers_df = generate_sample_data(1000)
    load_data_to_db(claims_df, providers_df)
