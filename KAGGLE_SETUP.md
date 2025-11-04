# Kaggle Data Setup Guide

## Overview

ClaimsIQ can load real insurance claims data from Kaggle using the `kagglehub` library. This guide shows you how to set up Kaggle authentication and download the dataset.

**Dataset:** [ravalsmit/insurance-claims-and-policy-data](https://www.kaggle.com/datasets/ravalsmit/insurance-claims-and-policy-data)

---

## Quick Start: UI Method (Easiest!)

**Don't want to use the command line?** You can load Kaggle data directly from the dashboard:

1. **Set up `kaggle.json`** (one-time setup, see below)
2. **Start the application:**
   ```bash
   reflex run --env prod --frontend-port 5000 --backend-port 8001
   ```
3. **Open dashboard:** `http://localhost:5000`
4. **Click "Load Kaggle Data"** button in the Data Management panel
5. **Wait 1-2 minutes** for download (first time only, cached after)
6. **Done!** Data appears automatically in dashboard

**OR** skip Kaggle setup entirely and click **"Generate Sample Data"** for instant realistic synthetic data!

---

## Prerequisites

1. **Kaggle Account**: Create a free account at [kaggle.com](https://www.kaggle.com)
2. **Python 3.10+**: Ensure Python is installed
3. **kagglehub**: Installed via `pip install kagglehub` (already in requirements.txt)

---

## Step 1: Get Your Kaggle API Credentials

### 1.1 Sign in to Kaggle
Go to [kaggle.com](https://www.kaggle.com) and sign in to your account.

### 1.2 Create API Token
1. Click on your profile picture (top right)
2. Select **"Settings"**
3. Scroll down to the **"API"** section
4. Click **"Create New Token"**

This will download a file called `kaggle.json` to your computer.

### 1.3 Locate kaggle.json
The file will be in your Downloads folder. It looks like this:

```json
{
  "username": "your_kaggle_username",
  "key": "abc123def456..."
}
```

**IMPORTANT:** Keep this file secure! It contains your API credentials.

---

## Step 2: Install kaggle.json

### On Linux / Mac

1. Create the `.kaggle` directory in your home folder:
```bash
mkdir -p ~/.kaggle
```

2. Move `kaggle.json` to the `.kaggle` directory:
```bash
mv ~/Downloads/kaggle.json ~/.kaggle/
```

3. Set proper permissions (required for security):
```bash
chmod 600 ~/.kaggle/kaggle.json
```

### On Windows

1. Create the `.kaggle` directory:
```cmd
mkdir %USERPROFILE%\.kaggle
```

2. Move `kaggle.json` to the `.kaggle` directory:
```cmd
move %USERPROFILE%\Downloads\kaggle.json %USERPROFILE%\.kaggle\
```

### Verify Installation

Check that the file is in the correct location:

**Linux/Mac:**
```bash
ls -la ~/.kaggle/kaggle.json
```

**Windows:**
```cmd
dir %USERPROFILE%\.kaggle\kaggle.json
```

You should see the `kaggle.json` file listed.

---

## Step 3: Install Dependencies

Make sure `kagglehub` is installed:

```bash
pip install kagglehub
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 4: Download the Dataset

**Choose your preferred method:**

### Method A: UI (Recommended)

1. Start the application:
   ```bash
   reflex run --env prod --frontend-port 5000 --backend-port 8001
   ```

2. Open `http://localhost:5000` in your browser

3. Click **"Load Kaggle Data"** in the Data Management panel

4. Wait for the success notification (1-2 minutes first time)

**Benefits:** No command line needed, visual feedback, automatic dashboard refresh

### Method B: Command Line

Run the data loading script:

```bash
python scripts/load_sample_data.py
```

### What Happens:

1. **First Run**: Downloads the Kaggle dataset (may take a few minutes)
   - Dataset is cached locally for future use
   - Progress is shown in the terminal

2. **Subsequent Runs**: Uses cached data (instant)
   - kagglehub automatically caches downloaded datasets
   - No re-download unless you clear the cache

### Expected Output:

```
============================================================
ClaimsIQ Data Loading Script
============================================================

[1/2] Attempting to download data from Kaggle...
Downloading Kaggle dataset: ravalsmit/insurance-claims-and-policy-data
This may take a few minutes on first run...
Dataset downloaded to: /home/user/.cache/kagglehub/datasets/...
Found CSV files: ['/path/to/claims.csv', '/path/to/policies.csv']
Processing claims.csv...
Loaded claims data: 5000 rows, 12 columns
Columns: ['claim_id', 'policy_id', 'amount', 'status', ...]
Processing Kaggle claims data...
Processed 5000 claims

[2/2] Loading data to database...
Loading data to database at sqlite:///claimsiq.db...
Loaded 5000 claims
Loaded 50 providers
Created indexes
Data loading complete!

============================================================
✅ Data loading complete!
============================================================
```

---

## Troubleshooting

### Error: "kagglehub not installed"

**Solution:** Install kagglehub:
```bash
pip install kagglehub
```

### Error: "Unauthorized"

**Problem:** kaggle.json not found or incorrect permissions

**Solution:**
1. Verify kaggle.json location:
   - Linux/Mac: `~/.kaggle/kaggle.json`
   - Windows: `C:\Users\<username>\.kaggle\kaggle.json`

2. Check file permissions (Linux/Mac):
   ```bash
   chmod 600 ~/.kaggle/kaggle.json
   ```

3. Verify file contents (should have "username" and "key")

### Error: "Dataset not found"

**Problem:** You may not have accepted the dataset's terms

**Solution:**
1. Go to the [dataset page](https://www.kaggle.com/datasets/ravalsmit/insurance-claims-and-policy-data)
2. Click **"Download"** (you may need to accept terms)
3. Try running the script again

### Fallback to Synthetic Data

If Kaggle download fails, the script automatically falls back to generating synthetic data:

```
[1/2] Kaggle download failed or unavailable.
Falling back to synthetic data generation...
Generating 1000 sample claims...
```

This ensures the application works even without Kaggle credentials.

---

## Alternative: Manual Download

If you prefer to manually download the dataset:

1. Go to [the dataset page](https://www.kaggle.com/datasets/ravalsmit/insurance-claims-and-policy-data)
2. Click **"Download"**
3. Extract the ZIP file
4. Place CSV files in `data/sample/` directory
5. Modify `scripts/load_sample_data.py` to read from that directory

---

## Data Processing

The script automatically:
- **Maps columns** from Kaggle format to ClaimsIQ schema
- **Generates missing fields** (status, dates, provider IDs if needed)
- **Creates provider table** from claims data if not available
- **Validates data** to ensure compatibility

### ClaimsIQ Enhanced Schema:

**Claims Table (18 fields):**
- `id`: Claim ID (CLM-XXXXXX)
- `policy_id`: Policy ID (POL-XXXXX)
- `claim_date`: Date of claim (YYYY-MM-DD)
- `claim_amount`: Dollar amount claimed
- `approved_amount`: Dollar amount approved (if approved)
- `status`: pending/approved/denied/flagged
- `provider_id`: Provider ID (PROV-XXX)
- `procedure_codes`: Medical procedure codes (CPT-XXXXX)
- `procedure_description`: Human-readable procedure name
- `diagnosis_code`: ICD-10 diagnosis code (e.g., E11.9)
- `diagnosis_description`: Human-readable diagnosis
- `patient_age`: Patient age (0-100)
- `patient_gender`: M/F
- `patient_state`: Two-letter state code (CA, TX, NY, etc.)
- `denial_reason`: Reason for denial (if denied)
- `days_to_process`: Number of days to process claim (if processed)
- `processed_date`: Date claim was processed (YYYY-MM-DD)
- `created_at`: Timestamp

**Providers Table (6 fields):**
- `id`: Provider ID (PROV-XXX)
- `npi`: National Provider Identifier (10 digits)
- `name`: Provider name (e.g., "Dr. A. Smith Clinic", "Regional Hospital")
- `type`: Hospital/Clinic/Urgent Care/Lab/Pharmacy/Imaging Center/Surgery Center
- `specialty`: General Practice/Family Medicine/Cardiology/Orthopedics/etc.
- `state`: Two-letter state code where provider is located

**New Fields Added:**
- **Patient Demographics**: Age, gender, state for better analytics
- **Clinical Details**: Diagnosis codes (ICD-10) and procedure descriptions
- **Processing Metrics**: Days to process, processed date, denial reasons
- **Geographic Data**: Patient and provider states for regional analysis

---

## Dataset Information

**Source:** [Kaggle - Insurance Claims and Policy Data](https://www.kaggle.com/datasets/ravalsmit/insurance-claims-and-policy-data)

**Dataset Details:**
- Real insurance claims and policy data
- Multiple CSV files with claims, policies, and provider information
- Suitable for analytics, fraud detection, and claims processing demos

**License:** Check the Kaggle dataset page for license information

**Size:** Varies by dataset version (typically 5K-50K rows)

---

## Synthetic Data (Fallback Mode)

If Kaggle is not configured, the script generates **realistic synthetic data** that matches the Kaggle dataset structure:

### Data Characteristics:

**Claims (1000 rows by default):**
- **Status Distribution**: 60% approved, 25% pending, 12% denied, 3% flagged
- **Claim Amounts**: $100 - $50,000 (realistic distribution)
  - Office visits: $100 - $500
  - Emergency visits: $500 - $3,000
  - Hospital/Surgery: $5,000 - $50,000
- **Claim Dates**: Exponential distribution (more recent claims)
- **Patient Age**: Normal distribution (mean 45, std 20)
- **Geographic**: 20 US states represented

**Medical Codes:**
- **12 Common Diagnoses** (ICD-10): Diabetes, Hypertension, COPD, etc.
- **12 Common Procedures** (CPT): Office visits, blood work, X-rays, etc.

**Providers (50 providers):**
- **7 Provider Types**: Hospital, Clinic, Urgent Care, Lab, Pharmacy, Imaging Center, Surgery Center
- **12 Specialties**: Cardiology, Orthopedics, Radiology, etc.
- **Realistic Names**: "Regional Hospital", "Dr. A. Smith Clinic"

### Example Output:

```
Generating 1000 synthetic claims (matching Kaggle dataset structure)...
Generated 1000 claims and 50 providers
Status distribution: {'approved': 603, 'pending': 247, 'denied': 123, 'flagged': 27}
Average claim amount: $3,247.82
```

**Note:** The synthetic data is statistically realistic and suitable for demos, testing, and development.

---

## Security Best Practices

1. **Never commit kaggle.json to git**
   - Already added to `.gitignore`
   - Contains your API credentials

2. **Keep kaggle.json secure**
   - Set permissions to 600 (read/write for owner only)
   - Don't share your API key

3. **Regenerate if compromised**
   - Delete old token in Kaggle settings
   - Create new token
   - Replace `~/.kaggle/kaggle.json`

---

## Using Kagglehub in Code

To use kagglehub directly in your Python code:

```python
import kagglehub

# Download the dataset
path = kagglehub.dataset_download("ravalsmit/insurance-claims-and-policy-data")
print(f"Dataset downloaded to: {path}")

# Load CSV files
import pandas as pd
import glob
import os

csv_files = glob.glob(os.path.join(path, "*.csv"))
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    print(f"Loaded {csv_file}: {len(df)} rows")
```

---

## FAQ

**Q: Do I need a paid Kaggle account?**
A: No, a free Kaggle account is sufficient.

**Q: How often should I re-download the dataset?**
A: kagglehub caches the dataset locally. Only re-download if you want the latest version.

**Q: Can I use this in production?**
A: For demo/testing, yes. For production, verify the dataset license and consider using your own data.

**Q: What if I don't want to use Kaggle?**
A: The script automatically falls back to generating synthetic data. No Kaggle required.

**Q: Where is the cached data stored?**
A:
- Linux/Mac: `~/.cache/kagglehub/`
- Windows: `%LOCALAPPDATA%\kagglehub\cache\`

**Q: How do I clear the cache?**
A: Delete the kagglehub cache directory (see above paths).

---

## Next Steps

After loading the data:

1. **Start the application:**
   ```bash
   reflex run --env prod --frontend-port 5000 --backend-port 8001
   ```

2. **Access the dashboard:**
   - Frontend: http://localhost:5000
   - Backend API: http://localhost:8001
   - API Docs: http://localhost:8001/docs

3. **Explore the data:**
   - View claims in the interactive table
   - Use filters to find specific claims
   - Export data to CSV for analysis

---

**Version:** 1.0
**Last Updated:** 2025-11-03
**Dataset:** ravalsmit/insurance-claims-and-policy-data
