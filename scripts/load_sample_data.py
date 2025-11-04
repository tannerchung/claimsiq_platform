import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import random
import os
import sys

# Add kagglehub import
try:
    import kagglehub
    KAGGLEHUB_AVAILABLE = True
except ImportError:
    KAGGLEHUB_AVAILABLE = False
    print("Warning: kagglehub not installed. Install with: pip install kagglehub")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///claimsiq.db")

def download_kaggle_data():
    """
    Download insurance claims dataset from Kaggle using kagglehub.
    Dataset: ravalsmit/insurance-claims-and-policy-data

    Requires kaggle.json to be set up at:
    - Linux/Mac: ~/.kaggle/kaggle.json
    - Windows: C:\\Users\\<username>\\.kaggle\\kaggle.json

    Returns:
        tuple: (claims_df, providers_df) or (None, None) if download fails
    """
    if not KAGGLEHUB_AVAILABLE:
        print("ERROR: kagglehub is not installed.")
        print("Install with: pip install kagglehub")
        return None, None

    try:
        print("Downloading Kaggle dataset: ravalsmit/insurance-claims-and-policy-data")
        print("This may take a few minutes on first run...")

        # Download the dataset - kagglehub caches it locally
        path = kagglehub.dataset_download("ravalsmit/insurance-claims-and-policy-data")
        print(f"Dataset downloaded to: {path}")

        # List files in the downloaded directory
        import glob
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        print(f"Found CSV files: {csv_files}")

        # Load the CSV files
        claims_df = None
        providers_df = None

        for csv_file in csv_files:
            filename = os.path.basename(csv_file).lower()
            print(f"Processing {filename}...")

            if 'claim' in filename:
                claims_df = pd.read_csv(csv_file)
                print(f"Loaded claims data: {len(claims_df)} rows, {len(claims_df.columns)} columns")
                print(f"Columns: {list(claims_df.columns)}")
            elif 'provider' in filename or 'hospital' in filename:
                providers_df = pd.read_csv(csv_file)
                print(f"Loaded providers data: {len(providers_df)} rows, {len(providers_df.columns)} columns")
                print(f"Columns: {list(providers_df.columns)}")

        # If we found claims data, process it
        if claims_df is not None:
            claims_df = process_kaggle_claims(claims_df)

        # If we found provider data, process it
        if providers_df is not None:
            providers_df = process_kaggle_providers(providers_df)

        # If we didn't find provider data, create a basic one from claims
        if providers_df is None and claims_df is not None:
            print("No provider data found, creating basic provider table from claims...")
            providers_df = create_providers_from_claims(claims_df)

        return claims_df, providers_df

    except Exception as e:
        print(f"ERROR downloading Kaggle data: {e}")
        print(f"Make sure you have kaggle.json configured correctly.")
        print(f"See: https://github.com/Kaggle/kaggle-api#api-credentials")
        return None, None

def process_kaggle_claims(df):
    """
    Process the Kaggle claims DataFrame to match our schema.

    Expected ClaimsIQ schema:
    - id: Claim ID
    - policy_id: Policy ID
    - claim_date: Date of claim
    - claim_amount: Amount claimed
    - approved_amount: Amount approved (if approved)
    - status: pending/approved/denied/flagged
    - provider_id: Provider ID
    - procedure_codes: Medical procedure codes
    - created_at: Timestamp
    """
    print("Processing Kaggle claims data...")

    # Create a copy to avoid modifying original
    processed = df.copy()

    # Map Kaggle columns to our schema
    # Note: Adjust these mappings based on actual Kaggle dataset columns
    column_mapping = {}

    # Try to identify columns (case-insensitive)
    cols_lower = {col.lower(): col for col in df.columns}

    if 'claim_id' in cols_lower or 'claimid' in cols_lower:
        column_mapping[cols_lower.get('claim_id', cols_lower.get('claimid'))] = 'id'
    elif 'id' in cols_lower:
        column_mapping[cols_lower['id']] = 'id'

    if 'policy_id' in cols_lower or 'policyid' in cols_lower:
        column_mapping[cols_lower.get('policy_id', cols_lower.get('policyid'))] = 'policy_id'

    if 'claim_date' in cols_lower or 'claimdate' in cols_lower or 'date' in cols_lower:
        column_mapping[cols_lower.get('claim_date', cols_lower.get('claimdate', cols_lower.get('date')))] = 'claim_date'

    if 'claim_amount' in cols_lower or 'claimamount' in cols_lower or 'amount' in cols_lower:
        column_mapping[cols_lower.get('claim_amount', cols_lower.get('claimamount', cols_lower.get('amount')))] = 'claim_amount'

    if 'status' in cols_lower:
        column_mapping[cols_lower['status']] = 'status'

    if 'provider_id' in cols_lower or 'providerid' in cols_lower:
        column_mapping[cols_lower.get('provider_id', cols_lower.get('providerid'))] = 'provider_id'

    # Rename columns based on mapping
    if column_mapping:
        processed.rename(columns=column_mapping, inplace=True)

    # Ensure required columns exist
    if 'id' not in processed.columns:
        processed['id'] = [f'CLM-{i+1:06d}' for i in range(len(processed))]

    if 'claim_date' not in processed.columns:
        # Generate random dates in last year
        processed['claim_date'] = [(datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
                                   for _ in range(len(processed))]

    if 'status' not in processed.columns:
        # Assign random statuses
        statuses = ['pending', 'approved', 'denied', 'flagged']
        processed['status'] = [random.choices(statuses, weights=[0.3, 0.5, 0.15, 0.05])[0]
                               for _ in range(len(processed))]

    if 'approved_amount' not in processed.columns and 'claim_amount' in processed.columns:
        # Calculate approved amounts for approved claims
        def calc_approved(row):
            if row.get('status') == 'approved':
                return round(row['claim_amount'] * random.uniform(0.7, 1.0), 2)
            return None
        processed['approved_amount'] = processed.apply(calc_approved, axis=1)

    if 'created_at' not in processed.columns:
        processed['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if 'procedure_codes' not in processed.columns:
        processed['procedure_codes'] = [f'CPT-{random.randint(10000, 99999)}' for _ in range(len(processed))]

    if 'policy_id' not in processed.columns:
        processed['policy_id'] = [f'POL-{random.randint(1, 500):05d}' for _ in range(len(processed))]

    if 'provider_id' not in processed.columns:
        processed['provider_id'] = [f'PROV-{random.randint(1, 50):03d}' for _ in range(len(processed))]

    # Add additional fields to match enhanced schema
    if 'procedure_description' not in processed.columns:
        # Generate from common procedures
        procedure_descriptions = [
            'Office visit - established patient',
            'Office visit - detailed',
            'Emergency visit - high complexity',
            'Comprehensive metabolic panel',
            'Complete blood count',
            'Electrocardiogram',
            'Chest X-ray',
        ]
        processed['procedure_description'] = [random.choice(procedure_descriptions) for _ in range(len(processed))]

    if 'diagnosis_code' not in processed.columns:
        diagnosis_codes = ['E11.9', 'I10', 'M25.561', 'J44.9', 'E78.5', 'M54.5', 'J06.9']
        processed['diagnosis_code'] = [random.choice(diagnosis_codes) for _ in range(len(processed))]

    if 'diagnosis_description' not in processed.columns:
        diagnosis_descriptions = [
            'Type 2 Diabetes', 'Essential Hypertension', 'Pain in right knee',
            'COPD', 'Hyperlipidemia', 'Low back pain', 'Upper respiratory infection'
        ]
        processed['diagnosis_description'] = [random.choice(diagnosis_descriptions) for _ in range(len(processed))]

    if 'patient_age' not in processed.columns:
        processed['patient_age'] = [int(random.gauss(45, 20)) for _ in range(len(processed))]
        processed['patient_age'] = processed['patient_age'].clip(0, 100)

    if 'patient_gender' not in processed.columns:
        processed['patient_gender'] = [random.choice(['M', 'F']) for _ in range(len(processed))]

    if 'patient_state' not in processed.columns:
        states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']
        processed['patient_state'] = [random.choice(states) for _ in range(len(processed))]

    if 'denial_reason' not in processed.columns:
        def get_denial_reason(status):
            if status == 'denied':
                return random.choice([
                    'Service not covered',
                    'Pre-authorization required',
                    'Out of network',
                    'Duplicate claim',
                    'Missing documentation'
                ])
            return None
        processed['denial_reason'] = processed['status'].apply(get_denial_reason)

    if 'days_to_process' not in processed.columns:
        def calc_days_to_process(status):
            if status in ['approved', 'denied']:
                return random.randint(5, 45)
            return None
        processed['days_to_process'] = processed['status'].apply(calc_days_to_process)

    if 'processed_date' not in processed.columns:
        def calc_processed_date(row):
            if row.get('status') in ['approved', 'denied'] and 'claim_date' in row:
                try:
                    claim_dt = pd.to_datetime(row['claim_date'])
                    days = row.get('days_to_process', random.randint(5, 45))
                    processed_dt = claim_dt + timedelta(days=days)
                    return processed_dt.strftime('%Y-%m-%d')
                except:
                    return None
            return None
        processed['processed_date'] = processed.apply(calc_processed_date, axis=1)

    # Select all columns including new ones
    required_columns = [
        'id', 'policy_id', 'claim_date', 'claim_amount', 'approved_amount',
        'status', 'provider_id', 'procedure_codes', 'procedure_description',
        'diagnosis_code', 'diagnosis_description', 'patient_age', 'patient_gender',
        'patient_state', 'denial_reason', 'days_to_process', 'processed_date',
        'created_at'
    ]

    processed = processed[required_columns]

    print(f"Processed {len(processed)} claims")
    print(f"Columns: {list(processed.columns)}")
    return processed

def process_kaggle_providers(df):
    """Process the Kaggle providers DataFrame to match our schema."""
    print("Processing Kaggle providers data...")

    processed = df.copy()

    # Map columns (adjust based on actual Kaggle dataset)
    cols_lower = {col.lower(): col for col in df.columns}
    column_mapping = {}

    if 'provider_id' in cols_lower or 'providerid' in cols_lower or 'id' in cols_lower:
        column_mapping[cols_lower.get('provider_id', cols_lower.get('providerid', cols_lower.get('id')))] = 'id'

    if 'name' in cols_lower or 'provider_name' in cols_lower:
        column_mapping[cols_lower.get('name', cols_lower.get('provider_name'))] = 'name'

    if column_mapping:
        processed.rename(columns=column_mapping, inplace=True)

    # Ensure required columns
    if 'id' not in processed.columns:
        processed['id'] = [f'PROV-{i+1:03d}' for i in range(len(processed))]

    if 'npi' not in processed.columns:
        processed['npi'] = [f'{random.randint(1000000000, 9999999999)}' for _ in range(len(processed))]

    if 'name' not in processed.columns:
        processed['name'] = [f'Provider {i+1}' for i in range(len(processed))]

    if 'type' not in processed.columns:
        processed['type'] = [random.choice(['Hospital', 'Clinic', 'Lab', 'Pharmacy'])
                            for _ in range(len(processed))]

    if 'specialty' not in processed.columns:
        specialties = [
            'General Practice', 'Family Medicine', 'Internal Medicine',
            'Cardiology', 'Orthopedics', 'Radiology', 'Emergency Medicine',
            'Oncology', 'Pediatrics', 'Surgery', 'Dermatology', 'Psychiatry'
        ]
        processed['specialty'] = [random.choice(specialties) for _ in range(len(processed))]

    if 'state' not in processed.columns:
        states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
                  'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']
        processed['state'] = [random.choice(states) for _ in range(len(processed))]

    required_columns = ['id', 'npi', 'name', 'type', 'specialty', 'state']
    processed = processed[required_columns]

    print(f"Processed {len(processed)} providers")
    print(f"Columns: {list(processed.columns)}")
    return processed

def create_providers_from_claims(claims_df):
    """Create a basic providers table from unique provider IDs in claims."""
    print("Creating providers table from claims data...")

    if 'provider_id' not in claims_df.columns:
        print("No provider_id column in claims data")
        return None

    unique_providers = claims_df['provider_id'].unique()

    provider_types = ['Hospital', 'Clinic', 'Urgent Care', 'Lab', 'Pharmacy', 'Imaging Center', 'Surgery Center']
    specialties = [
        'General Practice', 'Family Medicine', 'Internal Medicine',
        'Cardiology', 'Orthopedics', 'Radiology', 'Emergency Medicine',
        'Oncology', 'Pediatrics', 'Surgery', 'Dermatology', 'Psychiatry'
    ]
    states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
              'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']

    providers_data = []
    for provider_id in unique_providers:
        provider_type = random.choice(provider_types)

        # Generate realistic provider names
        if provider_type in ['Hospital', 'Surgery Center', 'Imaging Center']:
            name = f'{random.choice(["Regional", "Community", "Memorial", "St. Mary\'s", "General", "County"])} {provider_type}'
        else:
            name = f'Dr. {chr(65 + random.randint(0, 25))}. {random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Martinez", "Davis"])} {provider_type}'

        providers_data.append({
            'id': provider_id,
            'npi': f'{random.randint(1000000000, 9999999999)}',
            'name': name,
            'type': provider_type,
            'specialty': random.choice(specialties),
            'state': random.choice(states)
        })

    providers_df = pd.DataFrame(providers_data)
    print(f"Created {len(providers_df)} providers from claims data")
    return providers_df

def generate_sample_data(num_claims=1000):
    """
    Generate synthetic data that matches the Kaggle dataset structure.

    This replicates the structure and content distribution of:
    ravalsmit/insurance-claims-and-policy-data

    Includes realistic healthcare insurance claim patterns:
    - Patient demographics (age, gender, location)
    - Diagnosis codes (ICD-10)
    - Procedure codes (CPT)
    - Provider information
    - Policy details
    - Claim amounts and statuses
    """
    print(f"Generating {num_claims} synthetic claims (matching Kaggle dataset structure)...")

    # Statuses matching real insurance claim distributions
    statuses = ['pending', 'approved', 'denied', 'flagged']
    status_weights = [0.25, 0.60, 0.12, 0.03]  # More realistic: 60% approved

    # Realistic provider types and specialties
    provider_types = ['Hospital', 'Clinic', 'Urgent Care', 'Lab', 'Pharmacy', 'Imaging Center', 'Surgery Center']
    specialties = [
        'General Practice', 'Family Medicine', 'Internal Medicine',
        'Cardiology', 'Orthopedics', 'Radiology', 'Emergency Medicine',
        'Oncology', 'Pediatrics', 'Surgery', 'Dermatology', 'Psychiatry'
    ]

    # Common diagnosis codes (ICD-10) with descriptions
    diagnosis_codes = [
        ('E11.9', 'Type 2 Diabetes'),
        ('I10', 'Essential Hypertension'),
        ('M25.561', 'Pain in right knee'),
        ('J44.9', 'COPD'),
        ('E78.5', 'Hyperlipidemia'),
        ('M54.5', 'Low back pain'),
        ('J06.9', 'Upper respiratory infection'),
        ('N39.0', 'Urinary tract infection'),
        ('F41.9', 'Anxiety disorder'),
        ('K21.9', 'GERD'),
        ('R51', 'Headache'),
        ('Z00.00', 'General medical examination'),
    ]

    # Common procedure codes (CPT) with descriptions
    procedure_codes = [
        ('99213', 'Office visit - established patient'),
        ('99214', 'Office visit - detailed'),
        ('99285', 'Emergency visit - high complexity'),
        ('80053', 'Comprehensive metabolic panel'),
        ('85025', 'Complete blood count'),
        ('93000', 'Electrocardiogram'),
        ('71020', 'Chest X-ray'),
        ('73562', 'Knee X-ray'),
        ('99223', 'Hospital admission'),
        ('J3301', 'Injection - triamcinolone'),
        ('90834', 'Psychotherapy 45 min'),
        ('36415', 'Blood draw'),
    ]

    # State codes for geographic distribution
    states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
              'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']

    # Generate providers first (50 providers)
    num_providers = 50
    providers = []
    provider_names = []

    for i in range(num_providers):
        provider_id = f'PROV-{i+1:03d}'
        provider_type = random.choice(provider_types)
        specialty = random.choice(specialties)

        # Generate realistic provider names
        if provider_type in ['Hospital', 'Surgery Center', 'Imaging Center']:
            name = f'{random.choice(["Regional", "Community", "Memorial", "St. Mary\'s", "General", "County"])} {provider_type}'
        else:
            name = f'Dr. {chr(65 + random.randint(0, 25))}. {random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Martinez", "Davis"])} {provider_type}'

        providers.append({
            'id': provider_id,
            'npi': f'{random.randint(1000000000, 9999999999)}',
            'name': name,
            'type': provider_type,
            'specialty': specialty,
            'state': random.choice(states)
        })
        provider_names.append(provider_id)

    # Generate claims data
    claims_data = []

    for i in range(num_claims):
        # Basic claim info
        claim_id = f'CLM-{i+1:06d}'
        policy_id = f'POL-{random.randint(1, 500):05d}'

        # Claim date - weighted toward recent dates
        days_ago = int(random.expovariate(1/120))  # Exponential distribution, avg 120 days
        days_ago = min(days_ago, 730)  # Cap at 2 years
        claim_date = datetime.now() - timedelta(days=days_ago)

        # Patient demographics
        age = int(random.gauss(45, 20))  # Normal distribution, mean 45, std 20
        age = max(0, min(100, age))  # Clamp to 0-100
        gender = random.choice(['M', 'F'])
        patient_state = random.choice(states)

        # Provider
        provider_id = random.choice(provider_names)
        provider = next(p for p in providers if p['id'] == provider_id)

        # Diagnosis and procedure
        diagnosis = random.choice(diagnosis_codes)
        procedure = random.choice(procedure_codes)

        # Claim amount - realistic distribution based on procedure type
        base_amount = random.uniform(100, 5000)

        # Adjust amount based on procedure type
        if 'Hospital' in provider['type'] or 'Surgery' in provider['type']:
            base_amount *= random.uniform(2.5, 10)  # Higher for hospital/surgery
        elif 'Emergency' in procedure[1]:
            base_amount *= random.uniform(1.5, 3)  # Higher for ER visits

        claim_amount = round(base_amount, 2)

        # Status - weighted distribution
        status = random.choices(statuses, weights=status_weights)[0]

        # Approved amount (if approved)
        approved_amount = None
        if status == 'approved':
            # Typically pay 70-100% of claim
            approval_rate = random.uniform(0.7, 1.0)
            approved_amount = round(claim_amount * approval_rate, 2)
        elif status == 'denied':
            approved_amount = 0.0

        # Denial reason (if denied)
        denial_reason = None
        if status == 'denied':
            denial_reason = random.choice([
                'Service not covered',
                'Pre-authorization required',
                'Out of network',
                'Duplicate claim',
                'Missing documentation'
            ])

        # Days to process
        if status in ['approved', 'denied']:
            days_to_process = random.randint(5, 45)
            processed_date = claim_date + timedelta(days=days_to_process)
        else:
            days_to_process = None
            processed_date = None

        claims_data.append({
            'id': claim_id,
            'policy_id': policy_id,
            'claim_date': claim_date.strftime('%Y-%m-%d'),
            'claim_amount': claim_amount,
            'approved_amount': approved_amount,
            'status': status,
            'provider_id': provider_id,
            'procedure_codes': procedure[0],
            'procedure_description': procedure[1],
            'diagnosis_code': diagnosis[0],
            'diagnosis_description': diagnosis[1],
            'patient_age': age,
            'patient_gender': gender,
            'patient_state': patient_state,
            'denial_reason': denial_reason,
            'days_to_process': days_to_process,
            'processed_date': processed_date.strftime('%Y-%m-%d') if processed_date else None,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    claims_df = pd.DataFrame(claims_data)
    providers_df = pd.DataFrame(providers)

    print(f"Generated {len(claims_df)} claims and {len(providers_df)} providers")
    print(f"Status distribution: {claims_df['status'].value_counts().to_dict()}")
    print(f"Average claim amount: ${claims_df['claim_amount'].mean():.2f}")

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
    print("=" * 60)
    print("ClaimsIQ Data Loading Script")
    print("=" * 60)

    # Try to download from Kaggle first
    print("\n[1/2] Attempting to download data from Kaggle...")
    claims_df, providers_df = download_kaggle_data()

    # If Kaggle download failed, generate sample data
    if claims_df is None or providers_df is None:
        print("\n[1/2] Kaggle download failed or unavailable.")
        print("Falling back to synthetic data generation...")
        claims_df, providers_df = generate_sample_data(1000)

    # Load data to database
    print("\n[2/2] Loading data to database...")
    load_data_to_db(claims_df, providers_df)

    print("\n" + "=" * 60)
    print("✅ Data loading complete!")
    print("=" * 60)
