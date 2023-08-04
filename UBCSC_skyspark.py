"""
Author: Peter Kim
Contributor: -
Purpose: Handle skyspark data with pandas
"""
# Package
import pandas as pd

# Global Variable
list_of_col = ['Year', 'Month', 'Day', 'UBC_Temp', 'UBC_HDD', 'UBC_CDD', 'UBC_Humid', 
                'Elec_Energy', 'Elec_Power', 'Thrm_Energy', 'Thrm_Power', 'Wtr_Cns',
                'Elec_EUI', 'Thrm_EUI', 'Total_EUI',
                'Gross_Floor_Area', 'Building_Height', 'No_of_Floor', 'Inner_V', 'Glazing_A', 
                'WWR', 'WFA', 'FA_SA', 'Operable Window', 'Orientation', 'Adjacency', 'Built_Year'
                'NW_Facade_A', 'SW_Facade_A', 'NE_Facade_A', 'SE_Facade_A']

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

        return value: m_df (merged dataframe)
        """

        # Read csv files and the column name according to the data if represents.
        EE_df = pd.read_csv(folder_path + '/' + self.building_name + '_Elec_Energy.csv').set_axis(['Timestamp', 'Elec_Energy'], axis = 'columns')
        EP_df = pd.read_csv(folder_path + '/' + self.building_name + '_Elec_Power.csv').set_axis(['Timestamp', 'Elec_Power'], axis = 'columns')
        TE_df = pd.read_csv(folder_path + '/' + self.building_name + '_Thrm_Energy.csv').set_axis(['Timestamp', 'Thrm_Energy'], axis = 'columns')
        TP_df = pd.read_csv(folder_path + '/' + self.building_name + '_Thrm_Power.csv').set_axis(['Timestamp', 'Thrm_Power'], axis = 'columns')
        WC_df = pd.read_csv(folder_path + '/' + self.building_name + '_Wtr_Cns.csv').set_axis(['Timestamp', 'Wtr_Cns'], axis = 'columns')
        
        # Merge of energy and power (for eletrical and thermal). Also validate the data by comparing the timestamps on each file.
        Elec_df = pd.merge(EE_df, EP_df, on=['Timestamp'], how='left')  # Merge electrical energy/power
        Thrm_df = pd.merge(TE_df, TP_df, on=['Timestamp'], how='left')  # Merge themeral energy/power
        flag = Elec_df['Timestamp'].equals(Thrm_df['Timestamp'])        # Compare timestamp column
        if (flag) == False: return False 
        
        # Merge of eletrical and thermal.
        Elec_Thrm_df = pd.merge(Elec_df, Thrm_df, on=['Timestamp'], how='left')
        flag = Elec_Thrm_df['Timestamp'].equals(WC_df['Timestamp'])
        if (flag) == False: return False 

        # Merge of electrical+thermal and water consumption
        m_df = pd.merge(Elec_Thrm_df, WC_df, on=['Timestamp'], how='left')
        
        # 
        for column in m_df:
            if ('Timestamp' in column):
                    m_df[column] = m_df[column].replace('T00:00:00-08:00 Los_Angeles', '', regex = True)
                    m_df[column] = m_df[column].replace('T00:00:00-07:00 Los_Angeles', '', regex = True)
                    m_df[['Year', 'Month','Day']] = m_df[column].str.split('-', expand=True)

            if ('Energy' in column):
                m_df[column] = m_df[column].replace('kWh', '', regex = True)
                
            if ('Power' in column):
                m_df[column] = m_df[column].replace('kW', '', regex = True) 

            if ('Cns' in column):
                m_df[column] = m_df[column].replace('m³', '', regex = True)

        m_df = m_df.drop('Timestamp', axis = 1)
        m_df = m_df.reindex(columns=list_of_col)
        
        return m_df

    def compute_eui(self, edited_file):
        ce_df = pd.read_csv(edited_file)

        # if not empty do computation
        if ce_df['Gross_Floor_Area'].empty: return False
        else:
            ce_df['Elec_EUI'] = ce_df['Elec_Energy'] / ce_df['Gross_Floor_Area']
            ce_df['Thrm_EUI'] = ce_df['Thrm_Energy'] / ce_df['Gross_Floor_Area']
            ce_df['Total_EUI'] = ce_df['Thrm_EUI'] + ce_df['Elec_EUI']
        return ce_df

    class operator:
        def __init__(self, dataframe):
            self.dataframe = dataframe
            
        # For building attributes
        def fill_data(self):
            add_df = pd.read_csv(self.dataframe)

            # Check
            if list(add_df) == list_of_col: print("list of col:\n" + list_of_col) 
            else: return False
            
            # Get User input
            user_col = input("Enter column: ")
            while user_col not in list(add_df): 
                print("Please enter a column name that is in the list_of_col\n")
                user_col = input("Enter column: ")

            while True:

                user_val = None
                while user_val is None:
                    try: user_val = int(input("Enter value: "))
                    except ValueError: print("Invalid input")

                user_confirm = input('Confirm Value: ' + str(user_val) + ' (yes or no)\n')
                if user_confirm == 'yes': break
                else: user_val = None

            # Fill the value to column
            add_df[user_col] = user_val

            return add_df

class error_detection:
    
    """
    Takes in a csv file and depending on what the user wants to detect as an error,
    it presents its analysis.
    
    For types of errors, there are:
    - Missing values
    - 
    """
    
    def __init__(self, file_name, type_of_error):
        self.file_name = file_name
        self.type_of_error = type_of_error

    # detect the missing value, and tell the date + col in which the value is missing.  
    def missing_value(self):
        pass
 
class df_integral:
    """
    Integrate separate dataset into one
    """

building_name = 'ChemBio'; merge = '_merged'; edit = '_edited'
in_path = r'C:\Users\peter.kim\Desktop\EUI\ChemBio'
out_path = in_path + '/' + '_' + building_name
f = skyspark(building_name)


# merge all files in the folder
#a = f.merge_energy(folder_path)

# fill in any other column values
#b = skyspark.operator( folder_path + '/' + '_' + building_name + '_merged.csv').fill_data()

# compute eui
#c = f.compute_eui(folder_path + '/' + '_' + building_name + '_edited.csv')

#a.to_csv(folder_path + '/' + '_' +building_name + '_merged.csv', index=False)
#c.to_csv(folder_path + '/' + '_' +building_name + '_edited.csv', index=False)

