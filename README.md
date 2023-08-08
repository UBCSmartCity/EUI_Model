# EUI_Model

## Research Overview
The goal of this research project is to advance the accuracy of energy demand forecasting for a group of buildings, thereby minimizing the variability in estimating base load and storage requirements for a given area. And doing so, one can significantly reduce the costs associated with incorporating renewable energy into existing energy systems or developing a new sustainable infrastructure.

To achieve this, we begin by training carefully selected models using datasets obtained from the University of British Columbia (UBC). This dataset encompasses various parameters, including Energy Usage Intensity (EUI), building parameters, weather conditions, and geological factors. By leveraging this information, our model should be able to accurately predict the energy demand on a daily, monthly, and yearly basis. In validating the accuracy of our models, we compare our predictions with actual energy consumption records obtained from UBC Skyspark and UBC's sustainability reports. This process confirms the soundness of our approach and provides the confidence factor which can be used in the analysis process. 

After evaluating the model's performance in predicting energy demand, our research focuses on connecting the demand side with the supply side. This integration allows us to determine the optimal base load and storage requirements for the area under consideration, which plays a vital role in estimating the cost and shaping the energy infrastructure. 

In summary, our research aims to predict energy demand through comprehensive energy data analysis and subsequently determine the optimal base load and storage requirements, leading to cost reduction in energy production. By analyzing and comparing various model development methods, we gain valuable insights into the most effective approaches across different contexts. Through these efforts, we contribute to the broader goal of advancing renewable energy integration and sustainability in the energy sector.

## Script 
This script automates and simplifies the process of acquiring data from both Skyspark and GeoJSON sources.

### Tasks
- [ ] Simplify the merge, fill_col(), and compute EUI process
- [ ] Add GeoJson capability
    - Reasech through building code -> and grab info -> fill col


### User Guide
```
a = 'Hello world';
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