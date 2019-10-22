import HW_Assignments.HW2F19_Template.src.data_service.data_table_adaptor as dtadaptor
import json
import pandas as pd

def t_get_rdb_table():

    pass

def t_get_databases():

    dbList = dtadaptor.get_databases();
    # print("The list of databases is:\n\n {}".format(json.dumps(dbList, indent=2))) # Print as pretty json
    print("The list of databases is:\n\n {}".format(pd.DataFrame(dbList))) # Print as DataFrame (i.e. table)

t_get_databases()