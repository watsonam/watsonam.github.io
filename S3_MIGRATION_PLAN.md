# S3 Migration Plan for Power Market Data

## 🎯 Problem
- Current repo storing CSV data files (20MB/day) causing Git bloat
- Projected 7GB/year growth unsustainable for Git repository
- Need proper data storage architecture

## 💰 Cost Estimate
**Annual S3 Costs:**
- Year 1 (7.3GB): ~$3/year
- Year 3 (20GB): ~$7/year
- Storage: $0.023/GB/month
- Requests: $0.0005 per 1,000 PUT operations
- **Total: Very affordable ($5-10/year)**

## 🏗️ Implementation Plan

### Step 1: AWS Setup
**Create S3 Bucket:**
- Name: `power-market-data-[your-initials]-2025`
- Region: `us-east-1` (cheapest)
- Settings: Private, versioning enabled

**Create IAM User with Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::power-market-data-[your-initials]-2025",
        "arn:aws:s3:::power-market-data-[your-initials]-2025/*"
      ]
    }
  ]
}
```

### Step 2: GitHub Secrets
Add to Repository Settings → Secrets and Variables → Actions:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_BUCKET`

### Step 3: Data Organization Structure
```
s3://your-bucket/
├── raw/
│   ├── nordpool/
│   │   └── YYYY/MM/DD/
│   │       ├── prices.csv
│   │       └── volumes.csv
│   ├── epexspot/
│   │   └── YYYY/MM/DD/
│   │       ├── continuous.csv
│   │       └── auction.csv
│   └── elexon/
│       └── YYYY/MM/DD/
│           ├── demand_outturn.csv
│           ├── balancing_costs.csv
│           └── acceptances.csv
├── processed/
│   └── monthly_summaries/
└── cache/
    └── [pickle files for performance]
```

### Step 4: Update GitHub Actions
Modify `.github/workflows/scrape-data.yml`:
```yaml
- name: Configure AWS
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1

- name: Upload to S3
  run: |
    DATE=$(date +%Y/%m/%d)

    # Upload Nord Pool data
    aws s3 cp power_research/data/nordpool/ \
      s3://${{ secrets.AWS_S3_BUCKET }}/raw/nordpool/${DATE}/ \
      --recursive --exclude "*" --include "*.csv"

    # Upload EPEX SPOT data
    aws s3 cp power_research/data/epexspot/ \
      s3://${{ secrets.AWS_S3_BUCKET }}/raw/epexspot/${DATE}/ \
      --recursive --exclude "*" --include "*.csv"

    # Upload Elexon data
    aws s3 cp power_research/data/elexon/ \
      s3://${{ secrets.AWS_S3_BUCKET }}/raw/elexon/${DATE}/ \
      --recursive --exclude "*" --include "*.csv"
```

### Step 5: Update .gitignore
Add to `.gitignore`:
```
# Data files (stored in S3)
power_research/data/
cache/
*.csv
```

### Step 6: Data Access Script
Create `scripts/download_data.py`:
```python
import boto3
import pandas as pd
from datetime import datetime, timedelta
import os

def download_data(source, date, data_type=None):
    """
    Download data from S3

    Args:
        source: 'nordpool', 'epexspot', 'elexon'
        date: 'YYYY-MM-DD' or datetime object
        data_type: specific file type (optional)
    """
    s3 = boto3.client('s3')
    bucket = os.environ['AWS_S3_BUCKET']

    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')

    s3_path = f"raw/{source}/{date.strftime('%Y/%m/%d')}/"

    # List and download files
    response = s3.list_objects_v2(Bucket=bucket, Prefix=s3_path)

    for obj in response.get('Contents', []):
        filename = obj['Key'].split('/')[-1]
        local_path = f"data/{source}/{filename}"
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        s3.download_file(bucket, obj['Key'], local_path)
        print(f"Downloaded: {filename}")

def get_latest_data(source, days_back=7):
    """Get recent data for development"""
    for i in range(days_back):
        date = datetime.now() - timedelta(days=i)
        try:
            download_data(source, date)
        except:
            print(f"No data for {date.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    # Example usage
    get_latest_data('nordpool', days_back=7)
```

## 📋 Migration Steps

### Phase 1: Setup (30 minutes)
1. ✅ Create AWS account and S3 bucket
2. ✅ Create IAM user with appropriate permissions
3. ✅ Add GitHub secrets
4. ✅ Test AWS CLI access

### Phase 2: Code Changes (1 hour)
1. ✅ Update GitHub Actions workflow
2. ✅ Add data upload logic
3. ✅ Update .gitignore
4. ✅ Create data access scripts

### Phase 3: Migration (15 minutes)
1. ✅ Archive existing data to S3
2. ✅ Remove data files from Git history
3. ✅ Test automated workflow

### Phase 4: Cleanup (30 minutes)
1. ✅ Update documentation
2. ✅ Test data access scripts
3. ✅ Verify automated uploads working

## 🔄 Workflow After Migration

**Daily Process:**
1. GitHub Actions runs scrapers
2. Data collected to local `power_research/data/`
3. Data uploaded to S3 with date-based paths
4. Local data cleaned up
5. Summary report generated

**For Researchers:**
```python
# Get specific date's data
from scripts.download_data import download_data
download_data('nordpool', '2025-12-19')

# Get recent data for analysis
from scripts.download_data import get_latest_data
get_latest_data('elexon', days_back=30)
```

## ✅ Benefits After Migration
- ✅ **Fast Git operations** - no large files in repo
- ✅ **Proper data architecture** - organized by date/source
- ✅ **Scalable storage** - handles growth to TB+ easily
- ✅ **Cost effective** - $5-10/year for years of data
- ✅ **Professional setup** - industry standard approach
- ✅ **Better collaboration** - researchers get clean repo

## 🚨 Important Notes
- Keep cache files local for performance (scrapers rely on them)
- Test S3 permissions before deploying
- Consider S3 lifecycle policies for long-term cost optimization
- Monitor costs in AWS billing dashboard