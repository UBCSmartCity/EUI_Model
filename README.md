# EUI_Model

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Usage](#usage)

## About
The goal of this research project is to advance the accuracy of energy demand forecasting for a group of buildings, thereby minimizing the variability in estimating base load and storage requirements for a given area. And doing so, one can significantly reduce the costs associated with incorporating renewable energy into existing energy systems or developing a new sustainable infrastructure.

This script automates and simplifies the process of acquiring data from both Skyspark and GeoJSON.

## Getting Started <a name = "getting_started"></a>
#### Operational Directiory
```
EUI_MODEL
README.md
LICENSE.md
.gitignore
requirements.txt
data_prep/
    main/
    test/
dataset/
    ubcv_buildings/
        ubcv_buildings.geojson
        BuildingName1/
            _BuildingName1_merged.csv
            _BuildingName1_edited.csv
            BuildingName1_Elec_Energy.csv
            BuildingName1_Elec_Power.csv
            BuildingName1_Thrm_Energy.csv
            BuildingName1_Thrm_Power.csv
            BuildingName1_Wtr_Cns.csv
```

### Prerequisites
Pandas & GeoPandas

Folder directory example:
```
dataset/
    ubcv_buildings/
        ubcv_buildings.geojson
        Hennings/
            _Hennings_edit.csv -> (output)
            Hennings_Elec_Energy.csv
            Hennings_Elec_Power.csv
            Hennings_Thrm_Energy.csv
            Hennings_Thrm_Power.csv
            Hennings_Wtr_Cns.csv
```


## Usage <a name = "usage"></a>
```python
Merge the 5 files under the folder 
a = prep.Collection(build_name, data_dir)
b = a.skyspark()
```

```python
Parse units and re-arrange columns
a2 = prep.Transformation(b)
c = a2.parse_arrange(list_of_col)
```

```python
Get data from geojson
d = a.geojson(c)
```

```python
Compute EUI after entering the GFA data
e = a.eui(d)
```

```python
Output dataframe as .csv file
prep.csv_output(dir, build_name, e, 'edit')
```

#### List_of_Col Description


| Column  | Name | Unit | Description | 
|:-------------:|:-------------:|:-----:|----|
'Timestamp' | Unparsed date, time, and timezone | yyyy-mm-ddThh:mm-hh:mm*TZ*
'UBC_Temp' | UBC temperature | °C | Local temperature from: 
'UBC_HDD' | ^ Heating degree days | Degree Days | Demand for energy to heat a building
'UBC_CDD' |^ Cooling degree days | Degree Days | Demand for energy to cool a building
'UBC_Humid' | ^ Humidity |  Relative Humidity |
'Elec_Energy' | Electrical energy | kWh
'Elec_Power' | Electrical power | kW
'Elec_ConF' | Electrical confidence factor | %  
'Thrm_Energy' | Hot water (thermal) energy| kWh
'Thrm_Power' | Hot water (thermal) power | kW
'Thrm_ConF' | Hot water (thermal) confidence factor | %
'Wtr_Cns' | Water consumption | m^3
'Wtr_Conf' | Water confidence factor | % 
'Elec_EUI' | Electrical energy usage intensity | kWh/m^2/day
'Thrm_EUI' | Hot water (thermal) energy usage intensity | kWh/m^2/day
'Wtr_WUI' | Water usage/consumption intensity |m^3/m^3/day
'Total_EUI_excwtr' | Elec_EUI + Thrm_EUI | kWh/m^2/day 
'Built_Year' | | Year | Year of complete construction
'Gross_Floor_Area' | | m^2 | Total Floor are inside the building envelope
'FSP_Classroom' | Floor Space Percentage | % | Percent of floor space a type of room occupies
'FSP_Lab' | ^ | %
'FSP_Library' | ^ | %
'FSP_Office' | ^ | %
'MAX_Floor' | Floors | % | Total occupied floor
'BLDG_Height' | Height | m | Height from open entrance to top of the building
'Inner_V' | Inner volume | m^3 | Total enclosed volume of a building 
'Glazing_A' | Glazing Area | m^2 | 
'WWR' | Window-to-Wall | | total window area / total exterior wall area
'WFA' | Window-to-Floor Area | | total window area / total floor area 
'FA_SA' | FA/SA | | Fascade area / site area
'Operable_Window' | 
'Orientation' | | Position of the building with respect to N
'Adjacency' | | Adjacent building casting shadows
'NW_Facade_A' | | 
'SW_Facade_A' | | 
'NE_Facade_A' | | 
'SE_Facade_A' | |
'Constr_Type'  | | Construction Material
'Green_Status' | | Leed status

### Tasks
- [ ] Use flags to help detect error (flags.txt)
- [ ] Simplify the merge, fill_col(), and compute EUI process
- [x] Add GeoJson capability
    - Reasech through building code -> and grab info -> fill col
