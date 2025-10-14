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
│  ├─ 00_sanity_check.ipynb
│  └─ 10_embed_examples.ipynb
├─ scripts/
│  ├─ 00_download_eurosat.py          # download only (no unzip)
│  └─ 01_prepare_eurosat.py           # unzip, verify, organize
└─ src/
    ├─ __init__.py
    ├─ data_prep.py              # callable helpers used by the scripts
    ├─ paths.py                  # centralizes dirs (raw/interim/processed)
    ├─ hf_models.py              # load LLaVA/TerraMind embeddings
    └─ utils.py                  # logging, hashing, small helpers

```

Data is stored separately on the server. We store it at: ../waves/generalist_vs_specialized_geoAI. 

```
├─ DATA_PATH/                      # for us, ../waves/generalist_vs_specialized_geoAI
│  ├─ raw/                         # downloaded zips, untouched
│  ├─ interim/                     # unzipped but not yet curated
│  └─ processed/                   # final layout TorchGeo expects (source of truth)
```
