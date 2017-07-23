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

source_str = ["""# recursive factorial calculation
int b;

int fact(int a) {
    if(a == 0){
        return 1;
    }
    return a * fact(a - 1);
}

int main() {
    b = fact(10);
}
""", """# Default Sample
# Feel free to explore the World of thrilang.
int main () {
  # Declare an matrix of matrix
  float b[2];
  float a[b[1]][2][2][2];
  int i = 0, j = 100;
  bool test = true;
  while (i < j || test) {
    i++;
    j--;
    if ( j - i > 2 * j && test) {
      j = j + i;
    }
  }
}
int c;
""", """int a1;
int main() {
    a1 = 10
}
"""]
