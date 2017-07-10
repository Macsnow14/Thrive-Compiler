# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-04-15 12:38:20
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-04-15 12:45:52
expString = {'fineCases': ['1(0|1)*101',
                           '1(1010*|1(010)*1)*0',
                           '0*10*10*10*',
                           '(00|11)*((01|10)(00|11)*(01|10)(00|11)*)*'
                           ],
             'badCases': ['1(((1001*|10)*']
             }
grammar_str = ('E -> TR',
               'R -> +TR',
               'R -> -TR',
               'R -> ε',
               'T -> (E)',
               'T -> i',
               'T -> n')

non_terminators = ('E', 'T', 'R')
terminators = ('i', 'n', '(', ')', '+', '-')

source_str = """# recursive factorial calculation
int b;

int fact(int a){
    if(a == 0){
        return 1;
    }
    return a * fact(a - 1);
}

b = fact(10);"""
