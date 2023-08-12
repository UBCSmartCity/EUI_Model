import geopandas as gpd
building_info = gpd.read_file(r'/Users/peter/Desktop/EUI/EUI_Model/ubcv_buildings.geojson')

def test():
    x = 0   
    for name in building_info['NAME']:
        x = x + 1
        if "Henn" in name:
            return x - 1

row = test()
id = building_info['NAME'][row]
print(id)
    


# Columns
# BLDG_UID          y
# NAME              n    
# BLDG_CODE         n
# SHORTNAME         n
# POSTAL_CODE       n
# PRIMARY_ADDRESS   n
# CONSTR_STATUS     n
# OCCU_DATE         y
# BLDG_USAGE        n
# BLDG_SEC_USAGE    n
# JURISDICTION      n
# NEIGHBOURHOOD     n
# MANAGE_ORG        n
# BLDG_STATE        n   
# GREEN_STATUS      y
# CONSTR_TYPE       y
# MAX_FLOORS        y
# BLDG_HEIGHT       y
# GBA               y
# REC_IDS           n
# HAS_SUBBLDGS      n
# GEOM_SOURCE       n
# NOTES             n
# CREATED_USER      n
# CREATED_DATE      n
# LAST_EDITED_USER  n
# LAST_EDITED_DATE  n   
# BLDG_FORM         n
# BLDG_CONDITION    n
# ACCESSIBILITY_RATING  n
# BLDG_MAINTENANCE  n
# BLDG_CLASS        n
# PROPERTY_TYPE     n
# LABEL_NAME        n
# LABEL_CLASS       n
# geometry          n



