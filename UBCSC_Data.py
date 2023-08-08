"""
Author: Peter Kim
Contributor: -
Purpose: Handle skyspark data with pandas
"""
# Package
import pandas as pd

# Global Variable
#   Thrm = Thermal (Hot Water)
#   Wtr = Water
#   Conf = confidence factor
#   FSP = Floor Space Percentage
#   excwtr = Exclude Water Usage Intensity
   
list_of_col = [ 'Timestamp', 'Year', 'Month', 'Day', 'UBC_Temp', 'UBC_HDD', 'UBC_CDD', 'UBC_Humid', 
                'Elec_Energy', 'Elec_Power', 'Elec_ConF','Thrm_Energy', 'Thrm_Power', 'Thrm_ConF','Wtr_Cns', 'Wtr_Conf'
                'Elec_EUI', 'Thrm_EUI', 'Wtr_EUI', 'Total_EUI_excwtr',
                'Built_Year', 'Gross_Floor_Area', 'FSP_Classroom', 'FSP_Lab', 'FSP_Library', 'FSP_Office',
                'MAX_Floor', 'BLDG_Height' , 'Inner_V', 'Glazing_A', 
                'WWR', 'WFA', 'FA_SA', 'Operable_Window', 'Orientation', 'Adjacency',
                'NW_Facade_A', 'SW_Facade_A', 'NE_Facade_A', 'SE_Facade_A'
                'Constr_Type' ,'Green_Status']

class skyspark:
    """ 
    Process energy data available from UBC Skyspark, as well as provide tools such as:
    - compute_eui
    - fill_data
    - ...
    """
    def __init__(self, building_name):
        self.building_name = building_name

    def merge_energy(self, folder_path):
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
        EE_df = pd.read_csv(folder_path + '/' + self.building_name + '_Elec_Energy.csv').set_axis(['Timestamp', 'Elec_Energy'], axis = 'columns')
        EP_df = pd.read_csv(folder_path + '/' + self.building_name + '_Elec_Power.csv').set_axis(['Timestamp', 'Elec_Power'], axis = 'columns')
        TE_df = pd.read_csv(folder_path + '/' + self.building_name + '_Thrm_Energy.csv').set_axis(['Timestamp', 'Thrm_Energy'], axis = 'columns')
        TP_df = pd.read_csv(folder_path + '/' + self.building_name + '_Thrm_Power.csv').set_axis(['Timestamp', 'Thrm_Power'], axis = 'columns')
        WC_df = pd.read_csv(folder_path + '/' + self.building_name + '_Wtr_Cns.csv').set_axis(['Timestamp', 'Wtr_Cns'], axis = 'columns')
        
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

    def csv_output(self, dataframe, folder_path, function):
        dataframe.to_csv(folder_path + function + '.csv', index=False)

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
                ce_df['Wtr_EUI'] = ce_df['Wtr_Cns'] / ce_df['Gross_Floor_Area']
                ce_df['Total_EUI_excwtr'] = ce_df['Thrm_EUI'] + ce_df['Elec_EUI']

            return ce_df

building_name = 'Hennings'; merge = '_merged'; edit = '_edited'
in_path = r'C:\Users\Peter\Desktop\EUI_Model\dataset\Hennings'
out_path = in_path + '/' + '_' + building_name
a = skyspark(building_name)

# Merging files
b = a.merge_energy(in_path)
a.csv_output(b, out_path, merge)

# Adding values to the merged dataframe
#c = a.operator(in_path + '/' + '_' + building_name + '' + merge + '.csv').fill_col()
#a.csv_output(c, out_path, edit)

# Computing EUI
#d = a.operator(in_path + '/' + '_' + building_name + '' + edit + '.csv').compute_eui()
#a.csv_output(d, out_path, edit)

