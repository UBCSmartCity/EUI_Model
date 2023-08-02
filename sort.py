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
    
    def __init__(self, file_name, building_name, address):
        self.file_name = file_name
        self.building_name = building_name
        self.address = address


    def merge(self, fn1, fn2):
        df1 = pd.read_csv(fn1)
        df2 = pd.read_csv(fn2)
        df_col_merged = pd.merge(df1, df2, on=['Timestamp'], how='left')
        return df_col_merged

    def remove_unit(self):
        df = pd.read_csv(self.file_name) # Read csv
          
        # Detect col and remove appropriate units.
        for column in df:
            
            if ('Timestamp' in column):
                df[column] = df[column].replace('T00:00:00-08:00 Los_Angeles', '', regex = True)
                df[column] = df[column].replace('T00:00:00-07:00 Los_Angeles', '', regex = True)
                df[['Year', 'Month','Day']] = df[column].str.split('-', expand=True)
            
            if ('Energy' in column):
                df[column] = df[column].replace('kWh', '', regex = True)
                
            if ('Power' in column):
                df[column] = df[column].replace('kW', '', regex = True) 

            if ('Consumption' in column):
                df[column] = df[column].replace('m³', '', regex = True)
        
        # Store the df into a separate df
        return df
        
        # Output the new dataframe as CSV file
        #global new_name
        #new_name = self.building_name +'_New.csv'
        #df.to_csv(new_name, index=False)
        
     # Re-arrage DF - But before that we have to change the names of the col.
    def arrange(self, new_file_name):
        
        """
        -parese date and put the parsed in-front
        -change the col names - such that it dosen't have the building name
        
        - Use this after integration

        """
        
        df = pd.read_csv(new_file_name)
        
        for column in df:
            if ('Energy' in column):
                if ('Elec' in column):
                    df.rename({column: 'Elec_Energy'}, axis=1, inplace=True)
                if ('HW' in column):
                    df.rename({column: 'HW_Energy'}, axis=1, inplace=True)
 
            if ('Power' in column):
                if ('Elec' in column):
                    df.rename({column: 'Elec_Power'}, axis=1, inplace=True)
                if ('HW' in column):
                    df.rename({column: 'HW_Power'}, axis=1, inplace=True) 
                    
            if ('Consumption' in column):
                df.rename({column: 'DW_Volume'}, axis=1, inplace=True) 
                
        
        df = df.drop('Timestamp', axis = 1)
        
        # We have more columns such as area, temp, humidity and stuff like that.
        df = df.reindex(columns=['Year', 'Month', 'Day', 'Elec_Energy', 'Elec_Power', 'HW_Energy', 'HW_Power', 'DW_Volume'])
        
        print(df)
        df.to_csv(self.address + self.building_name +'-Arranged.csv', index=False)

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



path = r'C:\Users\peter.kim\Desktop\EUI\AERL_Elec_Power.csv'

#def __init__(self, file_name, building_name, address)
f2 = process_skyspark('AERL_Elec_Power.csv', 'AERL', path)
print(f2.merge('AERL_Elec_Power.csv', 'AERL_Elec_Energy.csv'))
#f2.remove_unit()

    
