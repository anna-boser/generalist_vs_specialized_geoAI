# Generalist vs. Specialized GeoAI
Project comparing generalist multimodal models to specialized geospatial models for satellite data analysis. 

```
generalist_vs_specialized_geoAI/
├─ README.md                       # You are here :) 
├─ environment.yml
├─ .gitignore
├─ configs/
│  └─ data.yaml                    # URLs, expected checksums, paths
├─ notebooks/
│  ├─ 00_explore_eurosat.ipynb
├─ scripts/
│  ├─ 00_download_eurosat.py          # download only (no unzip)
└─ src/
    ├─ __init__.py
    └─ utils.py                  # logging, hashing, small helpers

```

Data is stored separately on the server. We store it at: ../waves/generalist_vs_specialized_geoAI. 

```
├─ DATA_PATH/                      # for us, ../waves/generalist_vs_specialized_geoAI
│  ├─ raw/                         # downloaded zips, untouched
│  ├─ interim/                     # unzipped but not yet curated
│  └─ processed/                   # final layout TorchGeo expects (source of truth)
```


## Setup environments

### Complete environment
```
# 1. Create environment
conda env create -f environments/complete.yml

# 2. Activate
conda activate gen_spec_geoAI

# 3. (Optional) Register kernel for Jupyter
python -m ipykernel install --user --name gen_spec_geoAI --display-name "Generalized vs. Specialized GeoAI"
```

To verify: 

```bash
python -c "import torch, rasterio, transformers; print(torch.__version__, rasterio.__version__)"
```

### Smaller environment for local development (no torch, torchgeo, etc.)

```
# 1. Create environment
conda env create -f environments/local.yml

# 2. Activate
conda activate geoai_local
```

## Download data

Replace the data paths with your local one. 

### EuroSAT

```bash
wget -c "https://zenodo.org/records/7711810/files/EuroSAT_MS.zip?download=1" -O /home/waves/generalist_vs_specialized_geoAI/EuroSAT/EuroSAT_MS.zip -d /home/waves/generalist_vs_specialized_geoAI/EuroSAT/raw
```

### [BigEarthNet](https://bigearth.net/)

```bash
# S1
tar --zstd -xf /home/waves/generalist_vs_specialized_geoAI/BigEarthNet-S1/raw/BigEarthNet-S1.tar.zst -C /home/waves/generalist_vs_specialized_geoAI/BigEarthNet-S1/raw

# S2
tar --zstd -xf /home/waves/generalist_vs_specialized_geoAI/BigEarthNet-S2/raw/BigEarthNet-S2.tar.zst -C /home/waves/generalist_vs_specialized_geoAI/BigEarthNet-S2/raw
```
