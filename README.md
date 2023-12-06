# EUI_Model
This is a research project that aims to demonstrate a pipeline for optimizing energy storage in a distribution system with intermittent power sources. The optimization process references a dynamic model introduced [here](https://insightmaker.com/insight/2uM6Gc38YkMwcJ1Enwoufs/Smart-Grid-Electricity-storage-and-variable-energy-pricing). For more information on the research, visit [UBC Smart City](https://ubcsmartcity.com/).

## Table of Contents
+ [Getting Started](#getting_started)
+ [References](#references)
+ [Tools](#tools)

## Getting Started <a name = "getting_started"></a>
### Directory
```
README.md
LICENSE.md
.gitignore
requirements.txt
data_aquisition/
    main.py
    preperation.py
    test.py
ann/
    ANN Model - Building Facade Features.ipynb
    Exploratory Data Analysis - Building Facade Features.ipynb
mts/
    R-MURC-1.R
dataset/
    ubcv_buildings/
        ubcv_buildings.geojson
        BuildingName1/
            _BuildingName1_edited.csv
            BuildingName1_Elec_Energy.csv
            BuildingName1_Elec_Power.csv
            BuildingName1_Thrm_Energy.csv
            BuildingName1_Thrm_Power.csv
            BuildingName1_Wtr_Cns.csv
```

### Short Introduction
[data_aquisition.py](https://github.com/UBCSmartCity/EUI_Model/blob/main/data_aquisition/preperation.py) simplifies the data aquition process for UBC Skyspark. 

[ANN Model - Building Facade Features.ipynb & Exploratory Data Analysis - Building Facade Features.ipynb](https://github.com/UBCSmartCity/EUI_Model/tree/main/ann) is the code for artificial neural network model.

[R-MURC-1.R](https://github.com/UBCSmartCity/EUI_Model/blob/main/mts/R-MURC-1.R) is the code for multivariate time series model. 

## References <a name = "references"></a>
- [UBC Geospatial Opendata](https://github.com/UBCGeodata/ubc-geospatial-opendata)
- [UBC Skyspark](https://skyspark.energy.ubc.ca/)

## Tools <a name = "tools"></a>
- https://geojson.tools/
