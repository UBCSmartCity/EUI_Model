# Parse and sort the dataset.

# Edge cases:
# different order
# different symbol
# how much decimal places?

# Considerations:
# Building name at the front
# How to only get numbers from the file
import pandas as pd
class process_skyspark:
        
    """ 
    Take in the utilities file, and parase the data in the right column. 
    Consider the building names when iterating through the columns, also consider the
    unit character differences. 
    
    Use the date range to arrange the data nicely. Meaning recognize the date range and
    re-time stamp it. 
    
    Note for csv files from ENERGY tab, modify the header such that the column includes either energy or power
    For example, AERL file just says AERL in the column. So make it to AERL Elec Energ. 
    This way the algo can detect the energy tab
    
    - THis is case sensitive, can I make it so that it is not?
    """
    def __init__(self, building_name):
        self.building_name = building_name

    # Note we have to merge building-building too
    # Merge the energy data
    def merge_building(self, folder_path):
        EE_df = pd.read_csv(folder_path + '/' + self.building_name + '_Elec_Energy.csv').set_axis(['Timestamp', 'Elec_Energy'], axis = 'columns')
        EP_df = pd.read_csv(folder_path + '/' + self.building_name + '_Elec_Power.csv').set_axis(['Timestamp', 'Elec_Power'], axis = 'columns')
        TE_df = pd.read_csv(folder_path + '/' + self.building_name + '_Thrm_Energy.csv').set_axis(['Timestamp', 'Thrm_Energy'], axis = 'columns')
        TP_df = pd.read_csv(folder_path + '/' + self.building_name + '_Thrm_Power.csv').set_axis(['Timestamp', 'Thrm_Power'], axis = 'columns')
        WC_df = pd.read_csv(folder_path + '/' + self.building_name + '_Wtr_Cns.csv').set_axis(['Timestamp', 'Wtr_Cns'], axis = 'columns')
        
        Elec_df = pd.merge(EE_df, EP_df, on=['Timestamp'], how='left')
        Thrm_df = pd.merge(TE_df, TP_df, on=['Timestamp'], how='left')
        flag = Elec_df['Timestamp'].equals(Thrm_df['Timestamp'])
        if (flag) == False: return False 
        
        Elec_Thrm_df = pd.merge(Elec_df, Thrm_df, on=['Timestamp'], how='left')
        flag = Elec_Thrm_df['Timestamp'].equals(WC_df['Timestamp'])
        if (flag) == False: return False 

        df = pd.merge(Elec_Thrm_df, WC_df, on=['Timestamp'], how='left')
        
        for column in df:
            if ('Timestamp' in column):
                    df[column] = df[column].replace('T00:00:00-08:00 Los_Angeles', '', regex = True)
                    df[column] = df[column].replace('T00:00:00-07:00 Los_Angeles', '', regex = True)
                    df[['Year', 'Month','Day']] = df[column].str.split('-', expand=True)

        df = df.drop('Timestamp', axis = 1)
        
        # We have more columns such as area, temp, humidity and stuff like that. Get everyhting I can from the Skyspark
        df = df.reindex(columns=['Year', 'Month', 'Day', 'Elec_Energy', 'Elec_Power', 'Thrm_Energy', 'Thrm_Power', 'Wtr_Cns'])
        
        #print(df)
        df.to_csv(self.building_name + '_merged.csv', index=False)
        return df
    
    def remove_unit(self, merged_file):
        m_df = merged_file # Read csv
          
        # Detect col and remove appropriate units.
        for column in m_df:
            
            if ('Energy' in column):
                m_df[column] = m_df[column].replace('kWh', '', regex = True)
                
            if ('Power' in column):
                m_df[column] = m_df[column].replace('kW', '', regex = True) 

            if ('Cns' in column):
                m_df[column] = m_df[column].replace('m³', '', regex = True)
        
        # Store the df into a separate df
        m_df.to_csv(self.building_name + '_merged_nounit.csv', index=False)
        return m_df

    def validate(self):
    # Count number of nan
    # Replace nan with 0
        pass


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


folder_path = r''
f = process_skyspark('ChemBio')
a = f.merge(folder_path)
b = f.remove_unit(a)
c = b.fillna(0)

print(c)

