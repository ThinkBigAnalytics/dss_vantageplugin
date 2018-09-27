# -*- coding: utf-8 -*-
'''
Copyright © 2018 by Teradata.
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

def asterDo():
    # Recipe inputs
    main_input_name = get_input_names_for_role('main')[0]
    input_dataset = dataiku.Dataset(main_input_name)

    # Recipe outputs
    main_output_name = get_output_names_for_role('main')[0]
    output_dataset =  dataiku.Dataset(main_output_name)
    
    # Recipe function param
    dss_function = get_recipe_config().get('function', None)
    
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
                           """ Make sure connection setting is set to 'Read a database table'."""
                           """ This plugin only supports Aster tables.""")

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
                           """ Make sure connection setting is set to 'Read a database table'."""
                           """ This plugin only supports Aster tables.""")
        
    # actual query
    query = getFunctionsQuery(dss_function, inputTables, outputTable, get_recipe_config() or {})
    
    # raise RuntimeError("""I Just wanted to make this execution stop: """)
    
    # Uncomment below
    executor = SQLExecutor2(dataset=input_dataset)   
    if dss_function.get('dropIfExists', False):
        # dropAllQuery = getDropOutputTableArgumentsStatements(dss_function.get('arguments', []))
        dropAllQuery = getDropOutputTableArgumentsStatements(dss_function.get('output_tables', []))
        print(dropAllQuery)
        executor.query_to_df('SELECT \'DROPPING output_tables\';', dropAllQuery)
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
    recipe_output_table = dss_function.get('recipeOutputTable', "")
    print('recipe_output_table before IF')
    print(recipe_output_table)
    if recipe_output_table == "" or recipe_output_table == None:                   
        print('Default')
        selectResult = executor.query_to_df(query)
    else: #Perform Recipe output table select query
        print('Recipe output Table')
        print(recipe_output_table)
        print(recipe_output_table[u'name'])
        arg = dss_function.get('output_tables', [])
        print('arg')
        print(arg)        
        recipeOutputTableName = list(filter(lambda d: d[u'name'] == recipe_output_table.get('name'), arg))[0].get('value')
        # outputs = arg[0].get('value', '').split(',') #Check this
        print('outputs')
        print(recipeOutputTableName)        
        # print(outputs['recipe_output_table'])
        # recipeOutputTableName = outputs[recipe_output_table.name]
        customOutputTableSQL = 'SELECT * from '+ recipeOutputTableName
        print('Performing SELECT on Selected Table')
        print(customOutputTableSQL)
        selectResult = executor.query_to_df(customOutputTableSQL,query) 
    
    #if driver_function
        #if usethistable_checked
            #then use that as select query
    print('Moving results to output...')
    pythonrecipe_out = output_dataset
    pythonrecipe_out.write_with_schema(selectResult)
    print('Complete!')  

# Uncomment end