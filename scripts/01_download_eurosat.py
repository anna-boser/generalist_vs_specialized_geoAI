#!/usr/bin/env python3
"""
Simple script to download and prepare EuroSAT dataset.

Downloads to: ../waves/generalist_vs_specialized_geoAI/
"""

import shutil
import zipfile
from pathlib import Path
from urllib.request import urlretrieve
from src.utils import setup_logging, load_data_config


# Configuration - automatically loaded from YAML
config = load_data_config()
logger = setup_logging()
DATA_PATH = Path(config.get('DATA_PATH', 'data/'))
EUROSAT_URL = config.get('EUROSAT_URL', 'https://zenodo.org/records/7711810/files/EuroSAT_MS.zip')
ZIP_FILE = DATA_PATH / "raw" / "EuroSAT_MS.zip"
EXTRACTED_DIR = DATA_PATH / "interim" / "EuroSAT_MS"
PROCESSED_DIR = DATA_PATH / "processed"


def download_eurosat():
    """Download EuroSAT dataset."""
    logger.info(f"Downloading EuroSAT from {EUROSAT_URL}")
    logger.info(f"Destination: {ZIP_FILE}")
    
    # Create directories
    ZIP_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Download with progress
    def progress_hook(block_num, block_size, total_size):
        if total_size > 0:
            downloaded = block_num * block_size
            percent = min(100, (downloaded / total_size) * 100)
            size_mb = total_size / (1024 * 1024)
            logger.info(f"Downloaded {percent:.1f}% of {size_mb:.1f} MB")
    
    urlretrieve(EUROSAT_URL, ZIP_FILE, progress_hook)
    logger.info(f"Download complete: {ZIP_FILE}")


def extract_eurosat():
    """Extract the downloaded zip file."""
    logger.info(f"Extracting {ZIP_FILE} to {EXTRACTED_DIR}")
    
    EXTRACTED_DIR.parent.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(EXTRACTED_DIR.parent)
    
    logger.info(f"Extraction complete: {EXTRACTED_DIR}")


def organize_eurosat():
    """Organize data into final structure."""
    logger.info(f"Organizing data from {EXTRACTED_DIR} to {PROCESSED_DIR}")
    
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
        logger.error("Could not find EuroSAT data directory")
        return
    
    logger.info(f"Found data directory: {data_dir}")
    
    # Copy to processed directory
    shutil.copytree(data_dir, PROCESSED_DIR / "EuroSAT", dirs_exist_ok=True)
    
    # Count files
    total_files = len(list((PROCESSED_DIR / "EuroSAT").rglob("*.jpg")))
    logger.info(f"Organization complete. Total files: {total_files}")


def main():
    """Main function."""
    logger.info("EuroSAT Dataset Downloader")
    logger.info("=" * 40)
    
    # Check if already downloaded
    if ZIP_FILE.exists():
        logger.info(f"Zip file already exists: {ZIP_FILE}")
        response = input("Re-download? (y/N): ").lower()
        if response != 'y':
            logger.info("Skipping download")
        else:
            download_eurosat()
    else:
        download_eurosat()
    
    # Extract
    if EXTRACTED_DIR.exists():
        logger.info(f"Extracted directory already exists: {EXTRACTED_DIR}")
        response = input("Re-extract? (y/N): ").lower()
        if response != 'y':
            logger.info("Skipping extraction")
        else:
            extract_eurosat()
    else:
        extract_eurosat()
    
    # Organize
    if (PROCESSED_DIR / "EuroSAT").exists():
        logger.info(f"Processed directory already exists: {PROCESSED_DIR / 'EuroSAT'}")
        response = input("Re-organize? (y/N): ").lower()
        if response != 'y':
            logger.info("Skipping organization")
        else:
            organize_eurosat()
    else:
        organize_eurosat()
    
    logger.info("Done! EuroSAT data is ready at:")
    logger.info(f"  {PROCESSED_DIR / 'EuroSAT'}")


if __name__ == "__main__":
    main()
