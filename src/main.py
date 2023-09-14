import preperation as prep

# Configure dir
data_dir = str(prep.pl.Path(__file__).parent.parent.resolve()) + '/dataset'
dir = fr'{data_dir}'

# Configure name & columns
build_name = 'AERL' # Make sure that the folder name & file name starts with the same building name.s
list_of_col = [ 'BLDG_UID', 'Timestamp', 'Year', 'Month', 'Day', 'UBC_Temp', 'UBC_HDD', 'UBC_CDD', 'UBC_Humid', 
                'Elec_Energy', 'Elec_Power', 'Elec_ConF','Thrm_Energy', 'Thrm_Power', 'Thrm_ConF','Wtr_Cns', 'Wtr_Conf',
                'Elec_EUI', 'Thrm_EUI', 'Wtr_WUI', 'Total_EUI_excwtr',
                'Occu_Date', 'Constr_Type', 'Condition', 'Green_Status', 'MAX_Floors', 
                'FSP_Classroom', 'FSP_Lab', 'FSP_Library', 'FSP_Office', 
                'BLDG_Height', 'GFA', 'GBA','WWR', 'WFA', 'FA_SA', 'Inner_V', 'Glazing_A', 
                'Operable_Window', 'Orientation', 'Adjacency',
                'NW_Facade_A', 'SW_Facade_A', 'NE_Facade_A', 'SE_Facade_A'
                ]


# Execution
def one():
    # 1
    a = prep.Collection(build_name, data_dir)
    b = a.skyspark()

    # 2
    a2 = prep.Transformation(b)
    c = a2.parse_arrange(list_of_col)

    # 3
    d = a.geojson(c)

    # 4
    e = a.eui(d) 

    # 5
    prep.csv_output(dir, build_name, e, 'edit')

# Fill columns with values from Skyspark manually
def two():
    df = prep.pd.read_csv(data_dir + '/' + build_name + '/' + '_' + build_name + '_edit.csv')
    df['Elec_ConF'] = 0.9999
    df['Thrm_ConF'] = 0.9999
    df['Wtr_ConF'] = 0.9999
    df['FSP_Classroom'] = 0.06
    df['FSP_Lab'] = 0.05
    df['FSP_Library'] = 0
    df['FSP_Office'] = 0.46

    prep.csv_output(dir, build_name, df, 'edit')

two()