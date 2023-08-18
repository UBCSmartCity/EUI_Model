# EUI_Model

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Usage](#usage)

## About
The goal of this research project is to advance the accuracy of energy demand forecasting for a group of buildings, thereby minimizing the variability in estimating base load and storage requirements for a given area. And doing so, one can significantly reduce the costs associated with incorporating renewable energy into existing energy systems or developing a new sustainable infrastructure.

This script automates and simplifies the process of acquiring data from both Skyspark and GeoJSON.

## Getting Started <a name = "getting_started"></a>
#### Directory Overview
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
            _BuildingName1_edited.csv
            BuildingName1_Elec_Energy.csv
            BuildingName1_Elec_Power.csv
            BuildingName1_Thrm_Energy.csv
            BuildingName1_Thrm_Power.csv
            BuildingName1_Wtr_Cns.csv
```

### Prerequisites

#### Packages
Pandas & GeoPandas

#### Data Folder Directory
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
# Configure dir
data_dir = str(prep.pl.Path(__file__).parent.parent.resolve()) + '/dataset'
dir = fr'{data_dir}'
```

```python
# Set building name and columns. View column description below for more information. 
build_name = 'Hennings'
list_of_col = [ 'BLDG_UID', 'Timestamp', 'Year', 'Month', 'Day', 'UBC_Temp', 'UBC_HDD', 'UBC_CDD', 'UBC_Humid', 
                'Elec_Energy', 'Elec_Power', 'Elec_ConF','Thrm_Energy', 'Thrm_Power', 'Thrm_ConF','Wtr_Cns', 'Wtr_Conf'
                'Elec_EUI', 'Thrm_EUI', 'Wtr_WUI', 'Total_EUI_excwtr',
                'Occu_Date', 'Constr_Type', 'Condition', 'Green_Status', 'MAX_Floors', 'BLDG_Height', 
                'GFA', 'GBA', 'FSP_Classroom', 'FSP_Lab', 'FSP_Library', 'FSP_Office',
                'WWR', 'WFA', 'FA_SA', 'Inner_V', 'Glazing_A', 
                'Operable_Window', 'Orientation', 'Adjacency',
                'NW_Facade_A', 'SW_Facade_A', 'NE_Facade_A', 'SE_Facade_A'
                ]
```

```python
# 1. Merge the 5 files under the folder 
a = prep.Collection(build_name, data_dir)
b = a.skyspark()
```

```python
# 2. Parse units and re-arrange columns
a2 = prep.Transformation(b)
c = a2.parse_arrange(list_of_col)
```

```python
# 3. Get data from geojson
d = a.geojson(c) 
```

```python
# 4. Compute EUI after entering the GFA data
e = a.eui(d) \
```

```python
# 5. Output dataframe as .csv file
prep.csv_output(dir, build_name, e, 'edit')
```
#### List_of_Col Description
*Italic descriptions are from [UBC](https://github.com/UBCGeodata/ubc-geospatial-opendata/blob/master/ubcv/locations/metadata/ubcv_buildings_fields.csv)*

##### Generic
| Column  |Description | Unit |  
|:----------:|:-----:|:----------:|
'BLDG_UID' | Building's Unique ID given by UBC | NA |  
'Timestamp' | Unparsed date, time, and timezone | yyyy-mm-ddThh:mm-hh:mm*TZ* |
'UBC_Temp' | UBC Vancouver temperature | °C |
'UBC_HDD' | How cold the temperature was on a given day or during a period of days | Degree Days | 
'UBC_CDD' | How hot the temperature was on a given day or during a period of days | Degree Days | 
'UBC_Humid' | UBC Vancouver relative humidity | % |

##### Building Utility
| Column  |Description | Unit |  
|:----------:|:-----:|:----------:|
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

##### Building Features
| Column  |Description | Unit |  
|:----------:|:-----:|:----------:|
'Occu_Date' | *The date on which Occupancy Permit was issued.*| As per 1970 natioanl building code - after 1970 = 1, before = 0
'Constr_Type' | *Classification of building based on construction material type.* | NA
'Condition' | *Facility Condition Index (FCI) score reflects the current condition of the building based on the total cost of needed building repairs and renewal divided by the current cost of replacing the building.* | Good, Fair, Poor, Critical
'Green_Status' | *Identify which program and at what level of certification a building has achieved. LEED for academic buildings and REAP for residential neighbourhood buildings* | Leed status
'MAX_Floor' | Total floors above and below grade. | NA | 
'FSP_Classroom' | Floor space percentage of classrooms | % |
'FSP_Lab' | Floor space percentage of labs | % |
'FSP_Library' | Floor space percentage of libraries | % |
'FSP_Office' | Floor space percentage of offices | % |
'BLDG_Height' | *Height in meters from grade to highest point of roof. See UBC Development Handbook Section 3.6.* | m | Height from open entrance to top of the building |
'GFA' |Total floor area inside the building envelope, including the external walls, and excluding the roof. | m^2 |
'GBA' | *The sum of all horizontal areas of each storey within the exterior stud face of all exterior and basement walls.* | m^2 
'WWR' | Window-to-Wall ratio, Max 40% for bldgs in Zone 4 (<3000 HDD), ASHRAE 90.1 (total window area / total exterior wall area) | NA | 
'WFA' | Window-to-Floor Area ratio (total window area / total floor area ) | NA | 
'FA_SA' | Fascade area / Site area | NA | 
'Inner_V' | Total enclosed volume of a building | m^3 | 
'Glazing_A' | Glazing Area (Number of Windows x Window Area (per type)) | m^2 | 
'Operable_Window' |  Presence of window | yes = 1 or no = 0
'Orientation' | Position of the building with respect to N | Long axis along with North-South is quantified as 1, NE-SW is 2, E-W is 3, SE-NW is 4.
'Adjacency' | Number of adjacent building casting shadows | NA |
'NW_Facade_A' | Northwest facing building area | m |
'SW_Facade_A' | Southwest facing building area | m |
'NE_Facade_A' | Northeast facing building area | m |
'SE_Facade_A' | Southeast facing building area | m |

### Tasks
- [x] Simplify the merge, fill_col(), and compute EUI process
- [x] Add GeoJson capability
    - Reasech through building code -> and grab info -> fill col
