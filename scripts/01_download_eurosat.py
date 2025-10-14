#!/usr/bin/env python3
"""
Simple script to download and prepare EuroSAT dataset.

Downloads to: ../waves/generalist_vs_specialized_geoAI/
"""

import os
import shutil
import zipfile
from pathlib import Path
from urllib.request import urlretrieve
import yaml


# Load all configuration from data.yaml
def load_data_config():
    """Load all parameters from config file."""
    config_path = Path("configs/data.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


# Configuration - automatically loaded from YAML
config = load_data_config()
DATA_PATH = Path(config.get('DATA_PATH', 'data/'))
EUROSAT_URL = config.get('EUROSAT_URL', 'https://zenodo.org/records/7711810/files/EuroSAT_MS.zip')
ZIP_FILE = DATA_PATH / "raw" / "EuroSAT_MS.zip"
EXTRACTED_DIR = DATA_PATH / "interim" / "EuroSAT_MS"
PROCESSED_DIR = DATA_PATH / "processed"


def download_eurosat():
    """Download EuroSAT dataset."""
    print(f"Downloading EuroSAT from {EUROSAT_URL}")
    print(f"Destination: {ZIP_FILE}")
    
    # Create directories
    ZIP_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Download with progress
    def progress_hook(block_num, block_size, total_size):
        if total_size > 0:
            downloaded = block_num * block_size
            percent = min(100, (downloaded / total_size) * 100)
            size_mb = total_size / (1024 * 1024)
            print(f"Downloaded {percent:.1f}% of {size_mb:.1f} MB")
    
    urlretrieve(EUROSAT_URL, ZIP_FILE, progress_hook)
    print(f"Download complete: {ZIP_FILE}")


def extract_eurosat():
    """Extract the downloaded zip file."""
    print(f"Extracting {ZIP_FILE} to {EXTRACTED_DIR}")
    
    EXTRACTED_DIR.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(EXTRACTED_DIR.parent)
    
    print(f"Extraction complete: {EXTRACTED_DIR}")


def organize_eurosat():
    """Organize data into final structure."""
    print(f"Organizing data from {EXTRACTED_DIR} to {PROCESSED_DIR}")
    
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find the actual data directory (might be nested)
    data_dir = None
    for item in EXTRACTED_DIR.rglob("*"):
        if item.is_dir():
            # Look for directories with class names
            subdirs = [d.name for d in item.iterdir() if d.is_dir()]
            class_names = ["AnnualCrop", "Forest", "HerbaceousVegetation", "Highway", 
                          "Industrial", "Pasture", "PermanentCrop", "Residential", 
                          "River", "SeaLake"]
            if any(name in subdirs for name in class_names):
                data_dir = item
                break
    
    if data_dir is None:
        print("Error: Could not find EuroSAT data directory")
        return
    
    print(f"Found data directory: {data_dir}")
    
    # Copy to processed directory
    shutil.copytree(data_dir, PROCESSED_DIR / "EuroSAT", dirs_exist_ok=True)
    
    # Count files
    total_files = len(list((PROCESSED_DIR / "EuroSAT").rglob("*.jpg")))
    print(f"Organization complete. Total files: {total_files}")


def main():
    """Main function."""
    print("EuroSAT Dataset Downloader")
    print("=" * 40)
    
    # Check if already downloaded
    if ZIP_FILE.exists():
        print(f"Zip file already exists: {ZIP_FILE}")
        response = input("Re-download? (y/N): ").lower()
        if response != 'y':
            print("Skipping download")
        else:
            download_eurosat()
    else:
        download_eurosat()
    
    # Extract
    if EXTRACTED_DIR.exists():
        print(f"Extracted directory already exists: {EXTRACTED_DIR}")
        response = input("Re-extract? (y/N): ").lower()
        if response != 'y':
            print("Skipping extraction")
        else:
            extract_eurosat()
    else:
        extract_eurosat()
    
    # Organize
    if (PROCESSED_DIR / "EuroSAT").exists():
        print(f"Processed directory already exists: {PROCESSED_DIR / 'EuroSAT'}")
        response = input("Re-organize? (y/N): ").lower()
        if response != 'y':
            print("Skipping organization")
        else:
            organize_eurosat()
    else:
        organize_eurosat()
    
    print("\nDone! EuroSAT data is ready at:")
    print(f"  {PROCESSED_DIR / 'EuroSAT'}")


if __name__ == "__main__":
    main()
