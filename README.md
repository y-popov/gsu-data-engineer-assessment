# Senior Data Engineer Assessment

[![Terraform](https://github.com/y-popov/gsu-data-engineer-assessment/actions/workflows/terraform.yml/badge.svg)](https://github.com/y-popov/gsu-data-engineer-assessment/actions/workflows/terraform.yml)
[![Python Tests](https://github.com/y-popov/gsu-data-engineer-assessment/actions/workflows/python-tests.yml/badge.svg)](https://github.com/y-popov/gsu-data-engineer-assessment/actions/workflows/python-tests.yml)

This repository contains a data engineering pipeline for extracting, transforming, and loading the location of all hospitals for the UK from [OpenStreetMap](https://www.openstreetmap.org/). It demonstrates skills in:

- ETL pipeline development using Prefect
- Geospatial data processing
- Infrastructure as Code with Terraform
- AWS S3 integration
- CI/CD with GitHub Actions

## Project Overview

The pipeline extracts hospital data from OpenStreetMap for UK regions, stores the raw data in a "bronze" S3 bucket, transforms it into a more efficient format (Parquet), and then stores the processed data in a "silver" S3 bucket.

## Development

### Prerequisites

- Python 3.11+
- Terraform 1.12.2+
- AWS CLI or compatible S3 storage

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/y-popov/gsu-data-engineer-assessment.git
   cd gsu-data-engineer-assessment
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r tests/requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export TF_VAR_bronze_bucket="your-bronze-bucket-name"
   export TF_VAR_silver_bucket="your-silver-bucket-name"
   ```

### Infrastructure Deployment

The project uses Terraform to provision the necessary S3 buckets:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Running Tests

```bash
export PYTHONPATH=$(pwd)
pytest tests/
```

## Usage

### Running the Pipeline

To run the data pipeline locally:

```bash
python data-pipeline.py
```

This will:
1. Extract hospital data from all UK regions
2. Upload the raw GeoJSON files to the bronze S3 bucket
3. Filter the data and transform to GeoParquet format
4. Upload the GeoParquet file to the silver S3 bucket
