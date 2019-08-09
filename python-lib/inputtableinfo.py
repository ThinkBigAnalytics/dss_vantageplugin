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

import tableinfo
from pseudoconstantgetters import *

class inputtableinfo(tableinfo.tableinfo):
    def __init__(self, connectioninfo, datasetname, dss_function):
        super(inputtableinfo, self).__init__(connectioninfo, datasetname)
        self.__partitionKey = self.__getPartitionKeyFromFunctionDef(dss_function)
        self.__orderKey = self.__getOrderByKeyFromInputDef(dss_function)
        self.__dssfunction = dss_function
        self.__alias = ''
        
    @property
    def schemaname(self):
        return self._schemaname

    @property
    def tablenamewithoutschema(self):
        return self._tablename

    @property
    def partitionKey(self):
        return self.__partitionKey

    @property
    def orderKey(self):
        return self.__orderKey
    
    @property
    def alias(self):
        return self.__alias

    # Added useCoprocessor at end to get if coprocessor
    def setPropertiesFromDef(self, inputdef, useCoprocessor):
        tablealias = inputdef.get('name', '')
        tmpAlias = tablealias
        tmpAlias = '' if 'Dimension' == tablealias else tablealias
        # Test Add new alias if has alternateNames
        # print('Testing alternateNames')
        alternateNames = inputdef.get('alternateNames', [])
        # print(alternateNames)
        # print(alternateNames[0])
        # print(alternateNames[0].encode("utf-8"))
        # if alternate tables
        # if 
        tmpAlias = '' if 'input' == tablealias else tablealias
        tmpAlias = alternateNames[0].encode("utf-8") if alternateNames != [] else tmpAlias
        
        self.__alias = tmpAlias
        self.__partitionKey = self.__getPartitionClauseFromAliasedInputDef(
            inputdef.get('kind', 'DSSOTHERS'), inputdef)
        self.__orderKey = self.__getOrderByKeyFromInputDef(inputdef)

    def __getPartitionClauseFromAliasedInputDef(self, kind, inputdef):
        partitionbycolumn = inputdef.get('partitionAttributes', '')
        if isinstance(partitionbycolumn, (list, tuple)):
            return getPartitionKind(kind) +\
                (', '.join(partitionbycolumn) if 'PartitionByKey' == kind else '')
        return getPartitionKind(kind) +\
            (partitionbycolumn if 'PartitionByKey' == kind else '')

    def __getPartitionAttributes(self, inputdef):
        return ', '.join(inputdef.get('partitionAttributes', []))

    def __getPartitionClauseFromInputDef(self, kind, inputdef):
        return getPartitionKind(kind) +\
            (self.__getPartitionAttributes(inputdef) if 'PartitionByKey' == kind else '')

    def __getPartitionKeyFromFunctionDef(self, dss_function):
        # partition
        kind = next(iter(dss_function.get("partitionInputKind",[])),'DSSOTHERS')
        return self.__getPartitionClauseFromInputDef(kind, dss_function)

    def __getOrderByKeyFromInputDef(self, inputdef):
        #no empty string checking for orderByColumn since this is mandatory if isOrdered is true
        orderKeyFromInputDef = inputdef.get("orderByColumn", [])
        orderKeyDirectionFromInputDef = inputdef.get("orderByColumnDirection", [])
        
        # print('Order type')
        # print(orderKeyFromInputDef)
        # print(orderKeyDirectionFromInputDef)
        
        # print(orderKeyDirectionFromInputDef)
        # if orderKeyFromInputDef != [] or orderKeyFromInputDef == [''] or (len(orderKeyFromInputDef) == 0 and orderKeyFromInputDef[0].encode('ascii','ignore') != '' ):
        
        # return ', '.join([a + b for a,b in zip(orderKeyFromInputDef,orderKeyDirectionFromInputDef)]) if \
        #     isinstance(orderKeyFromInputDef, (list, tuple)) else orderKeyFromInputDef #Add DIRECTION
        # print('isinstance?')
        # print(isinstance(orderKeyFromInputDef, (list, tuple)))
        # print(isinstance(orderKeyDirectionFromInputDef, (list, tuple)))
        if isinstance(orderKeyFromInputDef, (list, tuple)) and orderKeyFromInputDef != ['']:
            returnValue = ', '.join([a + " " +  b for a,b in zip(orderKeyFromInputDef,orderKeyDirectionFromInputDef)])
            #print(returnValue)
            return ', '.join([a + " " +  b for a,b in zip(orderKeyFromInputDef,orderKeyDirectionFromInputDef)])
        else:
            return orderKeyFromInputDef



        # return ', '.join(orderKeyFromInputDef) if \
        #     isinstance(orderKeyFromInputDef, (list, tuple)) else orderKeyFromInputDef #Add DIRECTION
        # else:
        #     return ['']