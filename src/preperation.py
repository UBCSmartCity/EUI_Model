"""
Perform data collection and transformation

Author: Peter Kim (vento277)
Version: August 12, 2023
"""

import pandas as pd
import geopandas as gpd
import pathlib as pl

class Collection:
    """
    A class representing the data collection process

    Attribute building_name: Name of the building
    Invarient: building_name is a string

    Attribute folder_path: Relative path of the dataset/building_name
    Invarient: folder_path is a string with r''
    """
    def __init__(self, building_name, folder_path):
        self.building_name = building_name
        self.folder_path = folder_path

    def skyspark(self):
        """
        Returns merged dataframe

        Invarient: The value is a 2-dimensional data structure
        """
        # Read csv files and set the axes proper name other than the building name.
        EE_df = pd.read_csv(self.folder_path + '/' + self.building_name + '/' + self.building_name + '_Elec_Energy.csv').set_axis(['Timestamp', 'Elec_Energy'], axis = 'columns')
        EP_df = pd.read_csv(self.folder_path + '/' + self.building_name + '/' + self.building_name + '_Elec_Power.csv').set_axis(['Timestamp', 'Elec_Power'], axis = 'columns')
        TE_df = pd.read_csv(self.folder_path + '/' + self.building_name + '/' + self.building_name + '_Thrm_Energy.csv').set_axis(['Timestamp', 'Thrm_Energy'], axis = 'columns')
        TP_df = pd.read_csv(self.folder_path + '/' + self.building_name + '/' + self.building_name + '_Thrm_Power.csv').set_axis(['Timestamp', 'Thrm_Power'], axis = 'columns')
        WC_df = pd.read_csv(self.folder_path + '/' + self.building_name + '/' + self.building_name + '_Wtr_Cns.csv').set_axis(['Timestamp', 'Wtr_Cns'], axis = 'columns')

        # Compare timestamps to validate the time ranges.
        if  (   
            EE_df['Timestamp'].equals(EP_df['Timestamp']) &
            EP_df['Timestamp'].equals(TE_df['Timestamp']) &
            TE_df['Timestamp'].equals(TP_df['Timestamp']) &
            TP_df['Timestamp'].equals(WC_df['Timestamp'])
            ): error = False
        else: error = True
        
        # Merge dataframes if time range equals to one another.
        if (error != True):
            Elec_df = pd.merge(EE_df, EP_df, on=['Timestamp'], how='left')
            Thrm_df = pd.merge(TE_df, TP_df, on=['Timestamp'], how='left')
            Elec_Thrm_df = pd.merge(Elec_df, Thrm_df, on=['Timestamp'], how='left')
            m_df = pd.merge(Elec_Thrm_df, WC_df, on=['Timestamp'], how='left')
        else: return False

        return m_df
    
    def geojson(self, dataframe):
        """
        Returns dataframe with geojson data included

        Invarient: The value is a 2-dimensional data structure
        """
        geo_df = dataframe
        gjson = gpd.read_file(self.folder_path + '/ubcv_buildings.geojson')

        # Go through the GeoJSON dataframe to find the matching building name and its index.
        row = 0
        for name in gjson['NAME']:
            row = row + 1
            if self.building_name in name:
                index = row - 1

        # If the index is not 433 (max index), extract and fill the corrosponding values.
        if index != 433:
            geo_df['BLDG_UID'] = gjson['BLDG_UID'][index]
            geo_df['Occu_Date'] = gjson['OCCU_DATE'][index]
            geo_df['Condition'] = gjson['BLDG_CONDITION'][index]
            geo_df['Green_Status'] = gjson['GREEN_STATUS'][index]        
            geo_df['Constr_Type'] = gjson['CONSTR_TYPE'][index]
            geo_df['Max_Floors'] = gjson['MAX_FLOORS'][index]
            geo_df['BLDG_Height'] = gjson['BLDG_HEIGHT'][index]
            geo_df['GBA'] = gjson['GBA'][index]
        else:
            return 'Building could not be found in GeoJSON'

        return geo_df

    def eui(self, dataframe):
        """ 
        Returns dataframe with computed eui
        
        Invarient: The value is a 2-dimensional data structure
        """

        # Read dataframe
        eui_df = dataframe

        # If Gross_Floor_Area is not empty, compute EUI
        if (eui_df['GFA'].empty): return False
        else:
            eui_df['Elec_EUI'] = eui_df['Elec_Energy'] / eui_df['Gross_Floor_Area']
            eui_df['Thrm_EUI'] = eui_df['Thrm_Energy'] / eui_df['Gross_Floor_Area']
            eui_df['Wtr_WUI'] = eui_df['Wtr_Cns'] / eui_df['Gross_Floor_Area']
            eui_df['Total_EUI_excwtr'] = eui_df['Thrm_EUI'] + eui_df['Elec_EUI']

        return eui_df

class Transformation:
    """
    A class representing the data transformation process

    Attribute dataframe: Dataframe in which the transformation should occur
    Invarient: dataframe is a 2-dimensional data structure
    """
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def parse_arrange(self, col):
        """
        Returns parsed and arranged dataframe

        Invarient: The value is a 2-dimensional data structure
        """
        df = self.dataframe 

        # Parse timestamps and units
        for column in df:

            # Use temporary column to split year, month, and day - also replace timezone.
            if ('Timestamp' in column):
                df['temp'] = df[column] 
                df['temp'] = df['temp'].replace('T00:00:00-08:00 Los_Angeles', '', regex = True)    
                df['temp'] = df['temp'].replace('T00:00:00-07:00 Los_Angeles', '', regex = True)   
                df[['Year', 'Month', 'Day']] = df['temp'].str.split('-', expand=True)           
                df[column] = df[column].replace(' Los_Angeles', 'PST', regex = True)
                df[column] = df[column].replace(' Los_Angeles', 'PST', regex = True)
                df = df.drop('temp', axis = 1)

            # Remove meter units.
            if ('Energy' in column):
                df[column] = df[column].replace('kWh', '', regex = True)
            if ('Power' in column):
                df[column] = df[column].replace('kW', '', regex = True) 
            if ('Cns' in column):
                df[column] = df[column].replace('m³', '', regex = True)

        # Re-arrange the dataframe
        df = df.reindex(columns=col)    

        return df
        
# Configuration
build_name = 'Hennings'
data_dir = str(pl.Path(__file__).parent.parent.resolve()) + '/dataset'
dir = fr'{data_dir}'
list_of_col = [ 'BLDG_UID', 'Timestamp', 'Year', 'Month', 'Day', 'UBC_Temp', 'UBC_HDD', 'UBC_CDD', 'UBC_Humid', 
                'Elec_Energy', 'Elec_Power', 'Elec_ConF','Thrm_Energy', 'Thrm_Power', 'Thrm_ConF','Wtr_Cns', 'Wtr_Conf'
                'Elec_EUI', 'Thrm_EUI', 'Wtr_WUI', 'Total_EUI_excwtr',
                'Occu_Date', 'Constr_Type', 'Condition', 'Green_Status', 'MAX_Floors', 'BLDG_Height', 
                'GFA', 'GBA', 'FSP_Classroom', 'FSP_Lab', 'FSP_Library', 'FSP_Office',
                'WWR', 'WFA', 'FA_SA', 'Inner_V', 'Glazing_A', 
                'Operable_Window', 'Orientation', 'Adjacency',
                'NW_Facade_A', 'SW_Facade_A', 'NE_Facade_A', 'SE_Facade_A'
                ]

# Execution
a = Collection(build_name, data_dir)
b = a.skyspark()

a2 = Transformation(b)
c = a2.parse_arrange(list_of_col)

d = a.geojson(c)
print(d)










    
