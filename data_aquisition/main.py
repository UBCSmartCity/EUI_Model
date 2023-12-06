import preperation as prep

# Configure dir
data_dir = str(prep.pl.Path(__file__).parent.parent.resolve()) + '/dataset'
dir = fr'{data_dir}'

# Configure name & columns
build_name = 'Woodward Library' # Make sure that the folder name & file name starts with the same building name.s
list_of_col = [ 'BLDG_UID', 'Timestamp', 'Year', 'Month', 'Day', 'UBC_Temp', 'UBC_HDD', 'UBC_CDD', 'UBC_Humid', 
                'Elec_Energy', 'Elec_Power', 'Elec_ConF','Thrm_Energy', 'Thrm_Power', 'Thrm_ConF','Wtr_Cns', 'Wtr_ConF',
                'Elec_EUI', 'Thrm_EUI', 'Wtr_WUI', 'Total_EUI_excwtr',
                'Occu_Date', 'Constr_Type', 'Condition', 'Green_Status', 'MAX_Floors', 
                'FSP_Classroom', 'FSP_Lab', 'FSP_Library', 'FSP_Office', 
                'BLDG_Height', 'GFA', 'GBA','WWR', 'WFA', 'FA_SA', 'Inner_V', 'Glazing_A', 
                'Operable_Window', 'Orientation', 'Adjacency',
                'NW_Facade_A', 'SW_Facade_A', 'NE_Facade_A', 'SE_Facade_A'
                ]

# Execution
def analyze():
    # 1. Merge the 5 files under the folder 
    m = prep.Collection(build_name, data_dir)
    b = m.skyspark()

    # 2. Parse units and re-arrange columns
    a2 = prep.Transformation(b)
    c = a2.parse_arrange(list_of_col)

    # 3. Get data from geojson
    d = m.geojson(c)
    
    # 4. Manually change the values by reading it off of UBC Skyspark
    d['GFA'] = 7777
    d['Elec_ConF'] = 0.9995
    d['Thrm_ConF'] = 0.9995
    d['Wtr_ConF'] = 0.9995
    d['FSP_Classroom'] = 0.08
    d['FSP_Lab'] = 0.01
    d['FSP_Library'] = 0
    d['FSP_Office'] = 0.15

    # 5. Compute EUI after entering the GFA data
    e = m.eui(d) 

    # 6. Output dataframe as .csv file
    prep.csv_output(dir, build_name, e, 'edit')

analyze()