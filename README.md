#TODO:

-Check if there are any references to category, need to change certain things such as Aster scoring and the addition of the new functions
-Remove all caps converter

Some inconsistencies with current documentation:
-XGBoost is a single function in the documentation
-Npath does not have the _____ Argument in the documentation


TRY TO GET TO WORK AND PRINT ONLY UNTIL HERE
query = getFunctionsQuery(dss_function, inputTables, outputTable, get_recipe_config() or {})
    print('\n'.join(query))
    executor = SQLExecutor2(dataset=input_dataset)   