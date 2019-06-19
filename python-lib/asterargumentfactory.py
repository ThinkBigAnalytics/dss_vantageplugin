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

'''
Created on Jun 6, 2017

@author: DT186022
'''

from integerargument import *
from booleanargument import *
from ListArgument import *
from sqlexprargument import *
from columnnamesargument import *
from tableargument import *

class AsterArgumentFactory(object):
    '''
    Creates specific aster argument object based on data type
    '''


    def createArg(argument, argumentDef, inputTables):
        # print(argument.get('name'))
        # print('This is a list/tuple')
        if 'BOOLEAN' == argumentDef.get('datatype',''):
            # print('is Boolean')
            return BooleanArgument(argument, argumentDef)
        elif 'SQLEXPR' == argumentDef.get('datatype', '').upper():
            return SqlExprArgument(argument, argumentDef)
            # print('is SQLEXPR')
        elif ('INTEGER' == argumentDef.get('datatype', '').upper() or\
              'LONG' == argumentDef.get('datatype', '')) and\
        not argumentDef.get('allowsLists', False):
            # print('INTEGER')
            return IntegerArgument(argument, argumentDef)
        # elif 'TABLE_NAME' == argumentDef['datatype'] and not \
        elif 'TABLE_NAME' == argumentDef.get('datatype', '') and not \
        argumentDef.get('allowsLists', False) \
        and not argumentDef.get('isOutputTable', False):
            # print('TABLE_NAME')
            return TableArgument(argument, argumentDef, inputTables)        
        elif isinstance(argument.get('value',''), (list, tuple)):     
            # print('is List/tuple')      
            #This works to fix an issue with the empty inputs for the list. I have no idea why. As long as this code filters the input to ListArgument, no errors should occur for empty inputs.            
            argument['value'] = filter(None, argument.get('value'))
            # print(argument.get('value'))
            return ListArgument(argument, argumentDef)
        else:
            # print('is Others')
            return AsterArgument(argument, argumentDef)
    createArg = staticmethod(createArg)
    # elif 'COLUMN_NAMES' == argumentDef.get('datatype', '').upper() and\
        #     argumentDef.get('allowsLists', False):
        #     return ColumnNamesArgument(argument, argumentDef)
