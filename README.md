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


## Set up environments

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

#### Multispectral (S2): 
```bash
wget -c "https://zenodo.org/records/7711810/files/EuroSAT_MS.zip?download=1" -O /home/waves/generalist_vs_specialized_geoAI/EuroSAT/EuroSAT_MS.zip
```

<!-- ```python
from datasets import load_dataset

S2 = load_dataset("blanchon/EuroSAT_MSI")
``` -->

#### Sentinel-1 (SAR): 
```bash
wget -c "https://huggingface.co/datasets/wangyi111/EuroSAT-SAR/resolve/main/EuroSAT-SAR.zip?download=1" -O /home/waves/generalist_vs_specialized_geoAI/EuroSAT/EuroSAT_SAR.zip
```

<!-- ```python
from datasets import load_dataset

S1 = load_dataset("wangyi111/EuroSAT-SAR")
``` -->

<!-- #### Landsat (L): 

Only on hugging face? 
```python
from datasets import load_dataset

# Login using e.g. `huggingface-cli login` to access this dataset
ds = load_dataset("isaaccorley/eurosat-l")
``` -->

Then notebookds/00_unzip_eurosat.ipynb to unzip them