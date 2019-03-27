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

from _ast import If
try:
    from sets import Set
except ImportError:
    Set = set
import asterqueryutility as queryutility
from pseudoconstantgetters import *


def getInputTableFromDatasets(datasetname, inputDatasets):
    return next(iter(x for x in inputDatasets if x.datasetname == datasetname), None)

def getUnaliasedInputOnClause(requiredinput, inputTables):
    table = getInputTableFromDatasets(requiredinput, inputTables)
    return UNALIASED_ON_CLAUSE.format(input_table=table.tablename,
               partitionKeys=table.partitionKey, orderKeys=table.orderKey and
               " ".join(["ORDER BY", table.orderKey])).rstrip() +\
               "\n" if table else ''
               
def getInputQueryOnClause(inputquery):
    return UNALIASED_QUERY_ON_CLAUSE.format(input_query=inputquery) +\
               "\n" if inputquery else ''

def getOrderByClause(inputdef):
    orderByColumn = inputdef.get('orderByColumn', '') if\
    inputdef.get('isOrdered', False) else ''
    return orderByColumn and ("ORDER BY " + orderByColumn)
#Added useCoprocessor
def getAliasedInputONClause(input_, jsonfile, inputTables, useCoprocessor):
    table = getInputTableFromDatasets(input_.get('value', ''), inputTables)
    table.setPropertiesFromDef(input_, useCoprocessor)
    print('Input tables check')
    print(inputTables)
    if table.orderKey == [] or table.orderKey == [""] or table.orderKey == '':           
        return ALIASED_ON_CLAUSE.format(input_table=table.tablename,
           input_name=table.alias and ('AS "' + table.alias + '"'),
           partitionKeys=table.partitionKey,
           orderKeys = '').rstrip() + "\n" if table else ''
    else:
        return ALIASED_ON_CLAUSE.format(input_table=table.tablename,
            input_name=table.alias and ('AS "' + table.alias + '"'),
            partitionKeys=table.partitionKey,
            orderKeys = table.orderKey and
                " ".join(["ORDER BY", table.orderKey])).rstrip() + "\n" if table else ''
           
# added useCoprocessor
def getMultipleAliasedInputsClause(dss_function, jsonfile, inputTables):
    aliasedinputs = [x for x in dss_function.get('required_input', []) if
                     x.get('name', '') and x.get('value', '')]
    return ''.join(map(lambda x: getAliasedInputONClause(x, jsonfile, inputTables, dss_function['useCoprocessor']), aliasedinputs))

def getMultipleUnaliasedInputsClause(dss_function, inputTables):
    isQueryMode = dss_function.get('isQueryMode', False)
    if isQueryMode:
        return ''.join(map(lambda x: getInputQueryOnClause(x),
             """{}""".format(dss_function.get('queries', '')).split(DELIMITER)))
    unaliasedinputsdict = dss_function.get('unaliased_inputs', {})
    unaliasedinputs = unaliasedinputsdict.get('values', [])
    return ''.join(map(lambda x: getUnaliasedInputOnClause(x, inputTables),
                       unaliasedinputs[:int(min(unaliasedinputsdict.get('count', 1),
                                                len(unaliasedinputs)))]))
    
def getArgumentClauses(dss_function, jsonfile, inputTables):
    if dss_function.get('arguments', []) != []:
        print('Has arguments')
        return '\n' + queryutility.getJoinedArgumentsString(dss_function.get('arguments', []),
                                                 queryutility.getArgumentClausesFromJson(jsonfile),
                                                 inputTables)
    else:
        print('No arguments')
        return ''
    

def getOutClause(dss_function, jsonfile, inputTables):
    if dss_function.get('output_tables', []) != []:
        print(dss_function.get('output_tables', []))
        print('This happens in getoutclause')
        return '\n' + queryutility.getJoinedOutputTableString(dss_function.get('output_tables', []),
                                                 queryutility.getOutputTableClausesFromJson(jsonfile),
                                                 inputTables)   
    else:
        print('NOthing happens in getoutclause')
        return ''

    # return '\n' + queryutility.getJoinedArgumentsString(dss_function.get('output_tables', []),
    #                                              queryutility.getArgumentClausesFromJson(jsonfile),
    #                                              inputTables)                                                 

def getOnClause(dss_function, jsonfile, inputTables):
    return (getMultipleUnaliasedInputsClause(dss_function, inputTables) +
            getMultipleAliasedInputsClause(dss_function, jsonfile, inputTables)).strip() or\
            ON_SELECT_ONE_PARTITION_BY_ONE

def getFunctionName(config, dss_function, useCoprocessor):
    aafschema = config.get('aafschema', '')
    functionname = dss_function.get('name', '')
    if useCoprocessor:
        coprocessorString = "@coprocessor"
    else:
        coprocessorString = ""
    return (aafschema and (aafschema + '.')) + functionname + coprocessorString

def getAdditionClauses(dss_function):
    if isinstance(dss_function.get('additionalSQLClause'), list):
        return '\n'.join(dss_function.get('additionalSQLClause'))
    else:
        return ''

def getSelectQuery(dss_function, inputTables, config):
    jsonfile= queryutility.getJson(dss_function.get('name',''), dss_function.get('useCoprocessor',''))
    outTableClauses = getOutClause(dss_function, jsonfile, inputTables)     
    argumentClauses = getArgumentClauses(dss_function, jsonfile, inputTables)
    if(outTableClauses == '\n'):
        outTableClauses = ''
    if(argumentClauses == '\n'):
        argumentClauses = ''
    print('outTableClauses')
    print('START'+outTableClauses+'END')
    print('argumentClauses')
    print('START'+argumentClauses + 'END')
    completeClause = 'USING ' + outTableClauses + argumentClauses
    fullUsingClause = (outTableClauses or argumentClauses) and completeClause
    # if completeClause == 'USING ':
    #     fullUsingClause = ''
    #     print('Why isn\'t this  working')
    if outTableClauses or argumentClauses:
        print('This should work')
    print('fullUsingClause')
    print(fullUsingClause)
    print('The and statements')
    print('(outTableClauses or argumentClauses)')
    print((outTableClauses or argumentClauses))
    print('everything')
    print((outTableClauses or argumentClauses) and completeClause)
    print(fullUsingClause)
    #TODO ADD USING CLAUSE SOMEWHERE    
    # Update to:
    # Following code might have issues with Reduce functions with multiple INPUT TABLES
    useCoprocessor = dss_function.get('useCoprocessor','')
    if dss_function.get('hasPartnerFunction', False):
        jsonfilePartner= queryutility.getJson(dss_function.get('name',''), dss_function.get('useCoprocessor',''))
        # useCoprocessor = dss_function.get('useCoprocessor','')
        outTableClausesPartner = getOutClause(dss_function['partnerFunction'], jsonfilePartner, inputTables)     
        argumentClausesPartner = getArgumentClauses(dss_function['partnerFunction'], jsonfilePartner, inputTables)
        if(outTableClausesPartner == '\n'):
            outTableClausesPartner = ''
        if(argumentClausesPartner == '\n'):
            argumentClausesPartner = ''
        completeClausePartner = 'USING ' + outTableClausesPartner + argumentClausesPartner
        fullUsingClausePartner = (outTableClausesPartner or argumentClausesPartner) and completeClausePartner
        

        mapQuery = MAP_FUNCTION_QUERY.format(getFunctionName(config, dss_function, useCoprocessor),                       
                       getOnClause(dss_function, jsonfile, inputTables),
                       fullUsingClause)
        return MR_SELECT_QUERY.format(dss_function.get('select_clause', '*'),
                       getFunctionName(config, dss_function['partnerFunction'], useCoprocessor),                       
                       mapQuery, #    dss_function['partnerFunction']['required_input'][0]['name'],
                       "",
                       getPartitionByMap(dss_function['partnerFunction']['required_input'][0]), getOrderByMap(dss_function['partnerFunction']['required_input'][0]),
                       fullUsingClausePartner,
                       getAdditionClauses(dss_function['partnerFunction']))
    else:
        return SELECT_QUERY.format(dss_function.get('select_clause', '*'),
                       getFunctionName(config, dss_function, useCoprocessor),                       
                       getOnClause(dss_function, jsonfile, inputTables),
                       fullUsingClause,
                       getAdditionClauses(dss_function))
    return SELECT_QUERY.format(dss_function.get('select_clause', '*'),
                       getFunctionName(config, dss_function, useCoprocessor),                       
                       getOnClause(dss_function, jsonfile, inputTables),
                       fullUsingClause,
                       getAdditionClauses(dss_function))
    # return SELECT_QUERY.format(dss_function.get('select_clause', '*'),
    #                    getFunctionName(config, dss_function),                       
    #                    getOnClause(dss_function, jsonfile, inputTables),
    #                    fullUsingClause,
    #                    getAdditionClauses(dss_function)
    #                    )
    # return SELECT_QUERY.format(getFunctionName(config, dss_function),                       
    #                    getOnClause(dss_function, jsonfile, inputTables),
    #                    fullUsingClause
    #                    )
def getPartitionByMap(mapRequiredInputZero):
    # def getAliasedInputONClause(input_, jsonfile, inputTables, useCoprocessor):
    # table = getInputTableFromDatasets(input_.get('value', ''), inputTables)
    # table.setPropertiesFromDef(input_, useCoprocessor)
    print('Map Input tables check')
    # print(inputTables)
    print(mapRequiredInputZero)
    partitionByType = mapRequiredInputZero.get('kind','')
    if partitionByType == 'PartitionByKey':
        # return " ".join(["Partition BY", mapRequiredInputZero.partitionAttributes])).rstrip() +\
        partitionAttrbs = mapRequiredInputZero.get('partitionAttributes',[])
        if isinstance(partitionAttrbs, (list, tuple)) and mapRequiredInputZero.get('partitionAttributes', []) != ['']:
            partitionCols = ', '.join(mapRequiredInputZero.get('partitionAttributes',[]))
            print('Partition Column things')
            print(partitionCols)
            return "PARTITION BY " + partitionCols
    elif partitionByType == 'PartitionByAny':
        return "Partition By Any"
    elif partitionByType == 'PartitionByOne':
        return "Partition By 1"
    else:
        return "\n"

def getOrderByMap(mapRequiredInputZero):
    # def getAliasedInputONClause(input_, jsonfile, inputTables, useCoprocessor):
    # table = getInputTableFromDatasets(input_.get('value', ''), inputTables)
    # table.setPropertiesFromDef(input_, useCoprocessor)
    # print('Input tables check')
    # print(inputTables)
    print('Map Input tables check')
    # print(inputTables)
    print(mapRequiredInputZero)
    isOrdered = mapRequiredInputZero.get('isOrdered', False)
    if isOrdered:
        if isinstance(mapRequiredInputZero.get('orderByColumn',[]), (list, tuple)) and mapRequiredInputZero.get('orderByColumn',[]) != ['']:
            orderCols = ', '.join([a + " " +  b for a,b in zip(mapRequiredInputZero.get('orderByColumn',[]),mapRequiredInputZero.get('orderByColumnDirection',[]))])
            print('Order Column Things')
            print(orderCols)
            return "ORDER BY " + orderCols    
    else:
        return "\n"