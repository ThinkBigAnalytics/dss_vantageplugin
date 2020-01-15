# -*- coding: utf-8 -*-
'''
Copyright © 2019 by Teradata.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import dataiku
from dataiku.customrecipe import *
from dataiku import Dataset
from sets import Set
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
# Import the class that allows us to execute SQL on the Studio connections
from dataiku.core.sql import SQLExecutor2
# Import plugin libs
from querybuilderfacade import *
from inputtableinfo import *
from outputtableinfo import *
from outputtableinfo import *

# def getConnectionDetails(inputDataset):
#     return getConnectionParamsFromDataset(input_A_datasets[0]);

def asterDo():
    # Recipe inputs
    main_input_name = get_input_names_for_role('main')[0]
    input_dataset = dataiku.Dataset(main_input_name)    

    # print('Connection info:')
    # print(input_dataset.get_location_info(sensitive_info=True)['info'])
    properties = input_dataset.get_location_info(sensitive_info=True)['info'].get('connectionParams').get('properties')
    autocommit = input_dataset.get_location_info(sensitive_info=True)['info'].get('connectionParams').get('autocommitMode')
    
    requiresTransactions = True
     
    print('I am assuming in TERA MODE by default')
    if autocommit:
        print('I am assuming autocommmit TERA mode')
        requiresTransactions = False
        tmode = 'TERA'
        stTxn = ';'
        edTxn = ';'
    else:
        #Detected TERA
        print('I am assuming non-autocommit TERA MODE')
        tmode = 'TERA'
        stTxn = 'BEGIN TRANSACTION;'
        edTxn = 'END TRANSACTION;'

    for prop in properties:
        if prop['name'] == 'TMODE' and prop['value'] == 'TERA':
            if autocommit:
                print('I am in autocommmit TERA mode')
                requiresTransactions = False
                tmode = 'TERA'
                stTxn = ';'
                edTxn = ';'
            else:
                #Detected TERA
                print('I am in TERA MODE')
                tmode = 'TERA'
                stTxn = 'BEGIN TRANSACTION;'
                edTxn = 'END TRANSACTION;'
        elif prop['name'] == 'TMODE' and prop['value'] == 'ANSI':
            #Detected ANSI
            print('I am in ANSI MODE')
            tmode = 'ANSI'
            stTxn = ';'
            edTxn = 'COMMIT WORK;'
    print(properties)
    


    # Recipe outputs
    main_output_name = get_output_names_for_role('main')[0]
    output_dataset =  dataiku.Dataset(main_output_name)
    
    # Recipe function param
    dss_function = get_recipe_config().get('function', None)
    print('Showing DSS Function')
    print(dss_function)
    
    # Daitaiku DSS params
    client = dataiku.api_client()
    projectkey = main_input_name.split('.')[0]
    project = client.get_project(projectkey)

    try:
        # output dataset
        outputTable = outputtableinfo(output_dataset.get_location_info()['info'], main_output_name,
                                  get_recipe_config() or {})
    except Exception as error:
        raise RuntimeError("""Error obtaining connection settings for output table."""                           
                           """ This plugin only supports Teradata tables.""")
        # raise RuntimeError("""Error obtaining connection settings for output table."""
        #                    """ Make sure connection setting is set to 'Read a database table'."""
        #                    """ This plugin only supports Aster tables.""")

    # input datasets
    try:
        main_input_names = get_input_names_for_role('main')
        inputTables = []
        for inputname in main_input_names:
            inconnectioninfo = dataiku.Dataset(inputname).get_location_info()['info']
            inTable = inputtableinfo(inconnectioninfo, inputname, dss_function)
            inputTables.append(inTable)
    except Exception as error:
        raise RuntimeError("""Error obtaining connection settings from one of the input tables."""                           
                           """ This plugin only supports Teradata tables.""")
        
    # actual query
    query = getFunctionsQuery(dss_function, inputTables, outputTable, get_recipe_config() or {})
    
    # raise RuntimeError("""I Just wanted to make this execution stop: """)
    
    # Uncomment below
    executor = SQLExecutor2(dataset=input_dataset)   
    
   

    if dss_function.get('dropIfExists', False):
        #Start transaction
        #Move to drop query and make each DROP run separately
        dropAllQuery = getDropOutputTableArgumentsStatements(dss_function.get('output_tables', []))
        print('Drop ALL Query:')
        print(dropAllQuery)        
        
        # if requiresTransactions:
            # print('Start transaction for drop')
            # print(stTxn)
            # executor.query_to_df(stTxn)
        # dropAllQuery = getDropOutputTableArgumentsStatements(dss_function.get('arguments', []))
        
        #Change dropAllQuery to string/s? or execute one drop per item in list.            
        if requiresTransactions:
            for dropTblStmt in dropAllQuery:
                print('Start transaction for drop')
                print(stTxn)
                executor.query_to_df(stTxn)

                print('End transaction for drop')
                print(edTxn)
                executor.query_to_df(edTxn,[dropTblStmt])
            # executor.query_to_df(edTxn)
        else:
            for dropTblStmt in dropAllQuery:
                executor.query_to_df([dropTblStmt])
    # executor.query_to_df("END TRANSACTION;", pre_queries=query)
    
    # write table schema ACTUAL COMMENT
    # nQuery = '''SELECT * FROM {} LIMIT (1);'''.format(outputTable.tablename)
    # selectResult = executor.query_to_df(nQuery);
    # output_schema = []
    # for column in selectResult.columns:
    #     output_schema.append({"name":column, "type":"string"})
    # output_dataset.write_schema(output_schema)
    print('\n'.join(query))

    

    print(dss_function)
    # recipe_output_table = dss_function.get('recipeOutputTable', "")
    # print('recipe_output_table before IF')
    # print(recipe_output_table)
    if requiresTransactions:
        print('Start transaction for selectResult')
        print(stTxn)
        executor.query_to_df(stTxn)

    # Detect error
    try:
        selectResult = executor.query_to_df(query)
    except Exception as error:

        err_str = str(error)
        err_str_list = err_str.split(" ")
        
        if len(err_str_list) > 25:
            new_err_str = err_str_list[:24]
            new_err_str.append("\n\n")
            new_err_str.append("...")
            new_err_str = " ".join(new_err_str)
            raise RuntimeError(new_err_str)
        else:
            raise RuntimeError(err_str)
            
    
    print('Moving results to output...')
    pythonrecipe_out = output_dataset
    pythonrecipe_out.write_with_schema(selectResult)
    outtables = dss_function.get('output_tables', [])

    if(outtables != []):
        tableCounter = 1
        print('Working on output tables')
        print(get_output_names_for_role('main'))
        print(outtables)
        for table in outtables:
            if table.get('value') != '' and table.get('value') != None:
                # try:
                print('Table')
                print(table)
                #Need to change this to max of split in order for multiple database or no-database table inputs
                #Change below might fix issue 4 of Jan 4 2018 for Nico. For non-drop tables
                try:
                    main_output_name2 = list(filter(lambda out_dataset: out_dataset.split('.')[len(out_dataset.split('.'))-1] == table.get('value').split('.')[len(table.get('value').split('.'))-1].strip('\"'),get_output_names_for_role('main')))[0]
                except Exception as error:
                    # print(error.message)                    
                    raise RuntimeError('Unable to find an output dataset for '+table.get('value')+ 'It may not exist as an output Dataset: '+table.get('value')+"\n\Runtime Error:"+ error.message)
                print('Output name 2')
                print(main_output_name2)
                output_dataset2 =  dataiku.Dataset(main_output_name2)   
                # print("od2 printer")
                tableNamePrefix = output_dataset2.get_location_info(sensitive_info=True)['info'].get('connectionParams').get('namingRule').get('tableNameDatasetNamePrefix')
                if tableNamePrefix != None or tableNamePrefix != '':
                    print('Table prefix is not empty:' + tableNamePrefix)
                # except:
                #     #Need to change this error
                #     print('Error: Dataset for' + table.get('name') + ' not found')  
                #     raise Value              
                customOutputTableSQL = 'SELECT * from '+ table.get('value') + ' SAMPLE 0'
                print('Working on table number:')
                print(tableCounter)
                print(customOutputTableSQL)
                selRes = executor.query_to_df(customOutputTableSQL)
                tableCounter += 1
                pythonrecipe_out2 = output_dataset2
                pythonrecipe_out2.write_schema_from_dataframe(selRes)
    if requiresTransactions:
        print('End transaction')
        print(edTxn)
        executor.query_to_df(edTxn)
    print('Complete!')  


# Uncomment end