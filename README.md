gojek_ds
==============================
### Getting Started

#### Prerequisites
```
make setup
```

### Run Project

#### Download and preprocess data
```
make data
```

load data from GCP using **pandas_gpq** package, may need to set up google account access on first connection according to pop-up instructions <br>

processed data will be saved in data/interim folder

#### Feature engineering
```
make features
```

process data from data/interim and save to data/processed folder

#### Train model
```
make train
```

read data from data/processed and save the trained model to models

#### Test model 
```
make test
```

load test data from data/processed and model from models, save predictions to models

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make setup` or `make run`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- 
    │
    ├── docs               <- 
    │
    ├── models             <- Trained models, model predictions
    │
    ├── notebooks          <- Jupyter notebooks. 
    │
    ├── references         <- 
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- 
    │       └── visualize.py
    │
    └── tox.ini            <- 

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
