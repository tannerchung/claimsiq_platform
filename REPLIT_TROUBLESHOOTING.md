# Replit Troubleshooting Guide

## Issue: Reflex Application Not Starting

### Root Cause
The application fails to start because dependencies (specifically Reflex) are not installed before the app tries to run.

### Symptoms
- "reflex: command not found" error
- Application fails to start on ports 5000/8001
- Replit console shows import errors

---

## Solutions

### Option 1: Quick Fix (Replit Shell)
Run these commands in the Replit shell:

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize Reflex (creates .web directory)
reflex init

# Start the application
reflex run --env prod --frontend-port 5000 --backend-port 8001 --loglevel warning
```

### Option 2: Use Setup Script
```bash
chmod +x setup_replit.sh
./setup_replit.sh
```

### Option 3: Automatic Setup (Updated .replit)
The `.replit` file has been updated to automatically:
1. Install dependencies via pip
2. Initialize Reflex
3. Start the application

Simply press the "Run" button in Replit.

---

## Common Issues & Fixes

### 1. Dependencies Not Installing
**Problem**: `pip install` fails or times out

**Solution**:
```bash
# Clear pip cache
pip cache purge

# Reinstall with verbose output
pip install -r requirements.txt --verbose

# Or install packages individually
pip install reflex fastapi uvicorn pandas sqlalchemy python-dotenv pydantic psycopg2-binary
```

### 2. Reflex Init Fails
**Problem**: `reflex init` command errors

**Solution**:
```bash
# Remove existing Reflex directories
rm -rf .web/ __pycache__/

# Reinitialize
reflex init --loglevel debug
```

### 3. Port Already in Use
**Problem**: Ports 5000 or 8001 already bound

**Solution**:
```bash
# Find and kill processes on port 5000
lsof -ti:5000 | xargs kill -9

# Find and kill processes on port 8001
lsof -ti:8001 | xargs kill -9
```

### 4. Module Import Errors
**Problem**: `ModuleNotFoundError` for claimsiq modules

**Solution**:
```bash
# Ensure you're in the project root
cd /home/runner/claimsiq-platform

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run with explicit path
python -m reflex run --env prod --frontend-port 5000 --backend-port 8001
```

### 5. Database Connection Issues
**Problem**: Cannot connect to PostgreSQL database

**Solution**:
```bash
# Check if DATABASE_URL is set in Replit Secrets
echo $DATABASE_URL

# If not set, add it in Replit Secrets tab:
# Key: DATABASE_URL
# Value: postgresql://user:password@host:port/database

# For local testing, can use SQLite:
export DATABASE_URL="sqlite:///claimsiq.db"
```

### 6. Frontend Not Accessible
**Problem**: Port 5000 running but webview shows error

**Checklist**:
- ✅ Ensure `frontend_host="0.0.0.0"` in rxconfig.py (already set)
- ✅ Verify port 5000 is mapped in .replit (already configured)
- ✅ Check Replit webview is pointing to port 5000
- ✅ Wait 30-60 seconds for Reflex to compile frontend

---

## Configuration Files

### rxconfig.py
```python
import reflex as rx

config = rx.Config(
    app_name="claimsiq",
    frontend_port=5000,
    backend_port=8001,
    backend_host="0.0.0.0",  # Required for Replit
    frontend_host="0.0.0.0", # Required for Replit
    tailwind={}
)
```

### .replit (Key Sections)
```toml
[[workflows.workflow.tasks]]
task = "shell.exec"
args = "pip install -r requirements.txt && reflex init && reflex run --env prod --frontend-port 5000 --backend-port 8001 --loglevel warning"
waitForPort = 5000

[[ports]]
localPort = 5000
externalPort = 80

[[ports]]
localPort = 8001
externalPort = 3001
```

---

## Debugging Steps

### 1. Check Logs
```bash
# Run with debug logging
reflex run --env prod --frontend-port 5000 --backend-port 8001 --loglevel debug

# Check for specific errors in output
```

### 2. Verify Installation
```bash
# Check if reflex is installed
which reflex
reflex --version

# Check Python version
python --version  # Should be 3.11+

# List installed packages
pip list | grep -E "(reflex|fastapi|uvicorn)"
```

### 3. Test Components Individually
```bash
# Test FastAPI backend only
cd backend
uvicorn app:app --host 0.0.0.0 --port 8001

# Test if Reflex can import modules
python -c "from claimsiq.pages.dashboard import dashboard; print('OK')"
```

### 4. Check File Permissions
```bash
# Ensure files are readable
chmod -R u+r .
chmod +x setup_replit.sh
```

---

## Development Workflow on Replit

1. **First Time Setup**:
   ```bash
   pip install -r requirements.txt
   reflex init
   ```

2. **Every Run**:
   ```bash
   reflex run --env prod --frontend-port 5000 --backend-port 8001
   ```

3. **After Code Changes**:
   - Reflex auto-reloads on file changes
   - For major changes, restart the process (Ctrl+C then rerun)

4. **Database Updates**:
   ```bash
   python scripts/load_sample_data.py
   ```

---

## Environment Variables Checklist

Create these in Replit Secrets tab:

| Variable | Example Value | Required |
|----------|--------------|----------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | Yes |
| `API_PORT` | `8001` | No (defaults in code) |
| `API_HOST` | `0.0.0.0` | No (defaults in code) |
| `DEBUG` | `False` | No |
| `REFLEX_ENV` | `prod` | No |

---

## Success Checklist

When the app is running correctly, you should see:

✅ No errors during `pip install -r requirements.txt`
✅ `reflex init` completes successfully
✅ Console shows: `App running at: http://0.0.0.0:5000`
✅ Backend API accessible at port 8001
✅ Replit webview displays the dashboard
✅ No module import errors in logs
✅ Claims data loads in the table

---

## Getting Help

If issues persist:

1. Check the Reflex documentation: https://reflex.dev/docs/getting-started/introduction/
2. Review Replit Python docs: https://docs.replit.com/programming-ide/configuring-repl
3. Share full error logs from console
4. Verify all config files match this guide

---

## Quick Reference Commands

```bash
# Full reset and restart
rm -rf .web/ __pycache__/
pip install -r requirements.txt --force-reinstall
reflex init
reflex run --env prod --frontend-port 5000 --backend-port 8001

# Check system status
ps aux | grep reflex
netstat -tuln | grep -E "(5000|8001)"
pip list | grep reflex

# Emergency stop
pkill -f reflex
lsof -ti:5000 | xargs kill -9
lsof -ti:8001 | xargs kill -9
```
