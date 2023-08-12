"""
Author: Peter Kim
Contributor: -
Purpose: Handle skyspark data with pandas
"""
# Package
import pandas as pd
import geopandas as gpd

# Global Variable
# Note:
#   Thrm = Thermal (Hot Water)
#   Wtr = Water
#   Conf = confidence factor
#   FSP = Floor Space Percentage
#   excwtr = Exclude Water Usage Intensity
list_of_col = [ 'BLDG_UID', 'Timestamp', 'Year', 'Month', 'Day', 'UBC_Temp', 'UBC_HDD', 'UBC_CDD', 'UBC_Humid', 
                'Elec_Energy', 'Elec_Power', 'Elec_ConF','Thrm_Energy', 'Thrm_Power', 'Thrm_ConF','Wtr_Cns', 'Wtr_Conf'
                'Elec_EUI', 'Thrm_EUI', 'Wtr_WUI', 'Total_EUI_excwtr',
                'Occu_Date', 'Constr_Type', 'Condition', 'Green_Status', 'MAX_Floors', 'BLDG_Height', 
                'GFA', 'GBA', 'FSP_Classroom', 'FSP_Lab', 'FSP_Library', 'FSP_Office',
                'WWR', 'WFA', 'FA_SA', 'Inner_V', 'Glazing_A', 
                'Operable_Window', 'Orientation', 'Adjacency',
                'NW_Facade_A', 'SW_Facade_A', 'NE_Facade_A', 'SE_Facade_A'
                ]

# Columns from GeoJSON
# Building Unique ID
# Built Year(OCCU_DATE), Green_Status (GREEN_STATUS), Constr_Type (CONSTR_TYPE), Max_Floors (MAX_FLOORS)
# BLDG_Height (BLDG_HEIGHT), GBA,

class data:
    """ 
    Process energy data available from UBC Skyspark, as well as provide tools such as:
    - compute_eui
    - fill_data
    - ...
    
    Instead of having a completely automated process, the functions to spot mis-match or the error in the dataset easier.
    """
    def __init__(self, building_name, folder_path):
        self.building_name = building_name
        self.folder_path = folder_path

    def merge_5(self):
        """
        Merge & parse 5 data files available from UBC Skyspark and re-format the csv files to our needs. 5 data includes: 
        - electrical energy/power
        - thermal(hot water) energy/power
        - water consumption

        argument - folder_path
            Path to the folder that contains all the csv files
        return variable - m_df
            Merged dataframe
        """

        # Read csv files and the column name according to the data if represents
        EE_df = pd.read_csv(self.folder_path + '/' + self.building_name + '_Elec_Energy.csv').set_axis(['Timestamp', 'Elec_Energy'], axis = 'columns')
        EP_df = pd.read_csv(self.folder_path + '/' + self.building_name + '_Elec_Power.csv').set_axis(['Timestamp', 'Elec_Power'], axis = 'columns')
        TE_df = pd.read_csv(self.folder_path + '/' + self.building_name + '_Thrm_Energy.csv').set_axis(['Timestamp', 'Thrm_Energy'], axis = 'columns')
        TP_df = pd.read_csv(self.folder_path + '/' + self.building_name + '_Thrm_Power.csv').set_axis(['Timestamp', 'Thrm_Power'], axis = 'columns')
        WC_df = pd.read_csv(self.folder_path + '/' + self.building_name + '_Wtr_Cns.csv').set_axis(['Timestamp', 'Wtr_Cns'], axis = 'columns')
        
        # Merge of energy and power (for eletrical and thermal). Also validate the data by comparing the timestamps on each file
        Elec_df = pd.merge(EE_df, EP_df, on=['Timestamp'], how='left')  # Merge electrical energy/power
        Thrm_df = pd.merge(TE_df, TP_df, on=['Timestamp'], how='left')  # Merge themeral energy/power
        flag = Elec_df['Timestamp'].equals(Thrm_df['Timestamp'])        # Compare timestamp column
        if (flag) == False: return False 
        
        # Merge of eletrical and thermal
        Elec_Thrm_df = pd.merge(Elec_df, Thrm_df, on=['Timestamp'], how='left')
        flag = Elec_Thrm_df['Timestamp'].equals(WC_df['Timestamp'])
        if (flag) == False: return False 

        # Merge of electrical+thermal and water consumption
        m_df = pd.merge(Elec_Thrm_df, WC_df, on=['Timestamp'], how='left')
        
        # Iterate through the columns and remove units or parse them
        for column in m_df:

            # Parse the timestamp column into Year, Month, and Day
            if ('Timestamp' in column):
                    
                    # Use temporary column to split Y, M, and D
                    m_df['temp'] = m_df[column] 
                    m_df['temp'] = m_df['temp'].replace('T00:00:00-08:00 Los_Angeles', '', regex = True)    # Get only yyyy-mm-dd
                    m_df['temp'] = m_df['temp'].replace('T00:00:00-07:00 Los_Angeles', '', regex = True)    # Cover two timestamps
                    m_df[['Year', 'Month', 'Day']] = m_df['temp'].str.split('-', expand=True)               # Insert new column
                    
                    # Parse the original timestamp
                    m_df[column] = m_df[column].replace(' Los_Angeles', 'PST', regex = True)
                    m_df[column] = m_df[column].replace(' Los_Angeles', 'PST', regex = True)

                    # Delete the temporary column
                    m_df = m_df.drop('temp', axis = 1)
            
            # Remove units
            if ('Energy' in column):
                m_df[column] = m_df[column].replace('kWh', '', regex = True)
            if ('Power' in column):
                m_df[column] = m_df[column].replace('kW', '', regex = True) 
            if ('Cns' in column):
                m_df[column] = m_df[column].replace('m³', '', regex = True)

        # Re-arrange the dataframe
        m_df = m_df.reindex(columns=list_of_col)    
        
        return m_df

    def geojson(self, dataframe, json_path):
        bldg_info = gpd.read_file(json_path)
        geo_df = pd.read_csv(dataframe)
        
        
        def geo_row():
            row = 0
            flag = 0
            for name in bldg_info['NAME']:
                row = row + 1
                if self.building_name in name:
                    flag = 1
                    i = row - 1
            
            return flag, i
         
        index = geo_row()
        
        if index[0] != 0:
            geo_df['BLDG_UID'] = bldg_info['BLDG_UID'][index[1]]
            geo_df['Occu_Date'] = bldg_info['OCCU_DATE'][index[1]]
            geo_df['Condition'] = bldg_info['BLDG_CONDITION'][index[1]]
            geo_df['Green_Status'] = bldg_info['GREEN_STATUS'][index[1]]        
            geo_df['Constr_Type'] = bldg_info['CONSTR_TYPE'][index[1]]
            geo_df['Max_Floors'] = bldg_info['MAX_FLOORS'][index[1]]
            geo_df['BLDG_Height'] = bldg_info['BLDG_HEIGHT'][index[1]]
            geo_df['GBA'] = bldg_info['GBA'][index[1]]
        else:
            print("Building name not in GeoJSON")
             
        return geo_df

    def csv_output(self, dataframe, function):
        dataframe.to_csv(self.folder_path + '/' + '_' + self.building_name + '_' +function + '.csv', index=False)

    class operator:
        """
        Perform data manipulation or simple computation on dataframe
        """
        def __init__(self, dataframe):
            self.dataframe = dataframe
            
        def fill_col(self):
            """
            Fill a given column in the list_of_col with a desired integer value. 
            """
            # Read dataframe
            fill_df = pd.read_csv(self.dataframe)

            # Check if the columns matches list_of_col
            if list(fill_df) == list_of_col: print(list_of_col) 
            else: return False
            
            # User interface
            user_col = input("Enter column: ")

                # Get user input untill the input matches to one of the items in the list_of_col
            while user_col not in list(fill_df): 
                print("Please enter a column name that is in the list_of_col\n")
                user_col = input("Enter column: ")
            
                # Get the desired integer value from the user and confirm the value before proceeding
            while True:
                user_val = None
                while user_val is None:
                    try: user_val = int(input("Enter value: "))
                    except ValueError: print("Invalid input")

                # User confirmation
                user_confirm = input('Confirm Value: ' + str(user_val) + ' (yes or no)\n')
                if user_confirm == 'yes': break
                else: user_val = None

            # Fill the value to column
            fill_df[user_col] = user_val

            return fill_df
        
        def compute_eui(self):
            """
            Compute EUI if Gross_Floor_Area is not empty
            """

            # Read dataframe
            ce_df = pd.read_csv(self.dataframe)

            # If Gross_Floor_Area is not empty, compute EUI
            if ce_df['Gross_Floor_Area'].empty: return False
            else:
                ce_df['Elec_EUI'] = ce_df['Elec_Energy'] / ce_df['Gross_Floor_Area']
                ce_df['Thrm_EUI'] = ce_df['Thrm_Energy'] / ce_df['Gross_Floor_Area']
                ce_df['Wtr_WUI'] = ce_df['Wtr_Cns'] / ce_df['Gross_Floor_Area']
                ce_df['Total_EUI_excwtr'] = ce_df['Thrm_EUI'] + ce_df['Elec_EUI']

            return ce_df


merge = 'merged'; edit = 'edited'

# Setting up the calls
building_name = 'Hennings' 
in_path = r'C:\Users\Peter\Desktop\Project\EUI_Model\dataset\Hennings'  # Folder that contains all 5 files
                                                                # Make sure that the naming covention of all files matches that of
                                                                # Building_Name_TypeofMeter_TypeofMeasurement
out_path = in_path + '/' + '_' + building_name                  # Store the new file in the name folder with edited names
# Note that once naming conventions are set, the only thing the user has to change is building name and input folder path.

json_path = r'C:\Users\Peter\Desktop\Project\EUI_Model\ubcv_buildings.geojson'

# Execution
a = data(building_name, in_path)

# Merging files
b = a.merge_5()
a.csv_output(b, merge)

# Get data from GeoJSON
c = a.geojson(r'C:\Users\Peter\Desktop\Project\EUI_Model\dataset\Hennings\_Hennings_merged.csv', json_path)
a.csv_output(c, edit)

# Adding values to the merged dataframe
#c = a.operator(in_path + '/' + '_' + building_name + '' + merge + '.csv').fill_col()
#a.csv_output(c, out_path, edit)

# Computing EUI
#d = a.operator(in_path + '/' + '_' + building_name + '' + edit + '.csv').compute_eui()
#a.csv_output(d, out_path, edit)
