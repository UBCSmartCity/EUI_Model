# Parse and sort the dataset.

# Edge cases:
# different order
# different symbol
# how much decimal places?

# Considerations:
# Building name at the front
# How to only get numbers from the file
import pandas as pd

list_of_col = ['Year', 'Month', 'Day', 'UBC_Temp', 'UBC_HDD', 'UBC_CDD', 'UBC_Humid', 
                                 'Elec_Energy', 'Elec_Power', 'Thrm_Energy', 'Thrm_Power', 'Wtr_Cns',
                                 'Elec_EUI', 'Thrm_EUI', 'Total_EUI',
                                 'Gross_Floor_Area', 'Building_Height', 'No_of_Floor', 'Inner_V', 'Glazing_A', 
                                 'WWR', 'WFA', 'FA_SA', 'Operable Window', 'Orientation', 'Adjacency', 'Built_Year'
                                 'NW_Facade_A', 'SW_Facade_A', 'NE_Facade_A', 'SE_Facade_A']

class skyspark:
        
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
    def merge_energy(self, folder_path):
        """
        A function for merging all 5 csv files ia given folder. 
        Also remove units, and re-arrange columns
        """
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

        m_df = pd.merge(Elec_Thrm_df, WC_df, on=['Timestamp'], how='left')
        
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
        ce_df = edited_file

        print(ce_df)
        # if not empty do computation
        # if not (ce_df['Gross_Floor_Area']): return False
        # else:
        #     ce_df['Elec_EUI'] = ce_df['Elec_Energy'] / ce_df['Gross_Floor_Area']
        #     ce_df['Thrm_EUI'] = ce_df['Thrm_Energy'] / ce_df['Gross_Floor_Area']
        #     ce_df['Total_EUI'] = ce_df['Thrm_EUI'] + ce_df['Elec_EUI']
        # return ce_df

    class operator:
        def __init__(self, dataframe):
            self.dataframe = dataframe
            
        # For building attributes
        def fill_data(self):
            add_df = self.dataframe

            # Check
            if list(add_df) == list_of_col: pass 
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
                if user_confirm == True or 'yes': break
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

folder_path = r'C:\Users\Peter\Desktop\EUI_Model\dataset\Hennings'
# f = skyspark('Hennings')
# a = f.merge_energy(folder_path)
# b = f.remove_unit(a)
# c = b.fillna(0)
# print(c)

building_name = 'Hennings'
f = skyspark(building_name)

# merge all files in the folder
a = f.merge_energy(folder_path)

# fill in any other column values
#c = skyspark.operator(b).fill_data()

# compute eui
#d = f.compute_eui(building_name + '_edited.csv')

a.to_csv(folder_path + '/' + '_' +building_name + '_merged.csv', index=False)
#c.to_csv(building_name + '_edited.csv', index=False)

