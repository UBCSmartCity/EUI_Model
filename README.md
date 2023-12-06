# EUI_Model
This is a research project that aims to enhance the energy demand prediction for a cluster of buildings, optimizing electrical load in a distribution system with intermittent power sources. 

## Table of Contents
+ [Getting Started](#getting_started)
+ [Usage](#usage)
+ [References](#references)

## Getting Started <a name = "getting_started"></a>
#### Directory Overview
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

## Usage <a name = "usage"></a>
```
[data_aquisition.py]() simplifies the data aquition process for UBC Skyspark. 
```

```
[ANN Model - Building Facade Features.ipynb & Exploratory Data Analysis - Building Facade Features.ipynb]() is the code for artificial neural network model.
```

```
[R-MURC-1.R]() is the code for multivariate time series model. 
```

## References <a name = "references"></a>
- [UBC Geospatial Opendata](https://github.com/UBCGeodata/ubc-geospatial-opendata)
- [UBC Skyspark](https://skyspark.energy.ubc.ca/)

## Tools
- https://geojson.tools/
