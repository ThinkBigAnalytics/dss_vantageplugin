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

import asterqueryutility as queryutility
import cascadequerybuilder as cascadequery
import singlequerybuilder as singlequery
from inputtableinfo import *
from outputtableinfo import *


def getSelectClause(dss_function, inputTables, config={}):
    return cascadequery.getSelectQuery(dss_function, inputTables, config)\
        if 'cascaded_functions' in \
        dss_function else singlequery.getSelectQuery(dss_function, inputTables, config)

def getCreateQuery(dss_function, inputTables, outputTable, config={}):
    return CREATE_QUERY.format(
                    # outputTable.tableType,
                       outputTable.tablename,
                    #    outputTable.hashKey and DISTRIBUTE_BY_HASH.format(outputTable.hashKey),
                       getSelectClause(dss_function, inputTables, config))

def getDropOutputTableArgumentsStatementFromMultipleArguments(arg):
    outputs = arg.get('value', '').split(',')
    return '\n'.join(DROP_QUERY.format(outputTableName=x)\
            for x in outputs)

def getDropOutputTableArgumentsStatements(args):
    # beginTXNStatement = ''
    # return [''] + [DROP_QUERY.format(outputTablename=x.get('value', ''))\
    return [DROP_QUERY.format(outputTablename=x.get('value', ''))\
            for x in args if x.get('isOutputTable', False) and not x.get('allowsLists', False)\
            and x.get('value','')] + [getDropOutputTableArgumentsStatementFromMultipleArguments(x)\
                                      for x in args if x.get('isOutputTable', False)\
                                      and x.get('allowsLists', False) and x.get('value', '')]\
                                      
                                    #    + ['COMMIT;']

def getBeginDropCreateQueries(dss_function, inputTables, outputTable, config):
    #  return [BEGIN_TRANSACTION_QUERY,
    return [
                    # DROP_QUERY.format(outputTablename=outputTable.tablename) + "\n" +
                    getCreateQuery(dss_function, inputTables, outputTable, config)
                    # getCreateQuery(dss_function, inputTables, outputTable, config),
                    # COMMIT_QUERY]
            ]

def getFunctionsQuery(dss_function, inputTables, outputTable, config):
    return getBeginDropCreateQueries(dss_function, inputTables, outputTable, config)

def dropTableStatement(outputTable):
    return DROP_QUERY.format(outputTablename=outputTable.tablename)

