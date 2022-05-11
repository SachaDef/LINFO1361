from clause import *

"""
For the queen problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the queen problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, queens=None):
    expression = []

    # 1.1 Clauses for rows (1QUEEN MIN)
    for i in range(size): #row index
        for j in range(size-1): #column index_1
            for k in range(j+1,size): #column_index_2
                clause = Clause(size)
                clause.add_negative(i,j)
                clause.add_negative(i,k)
                expression.append(clause)

    # 1.2 Clauses for rows (1QUEEN MAX)
    for i in range(size): #row index
        for j in range(size-1): #column index_1
            for k in range(j+1,size): #column_index_2
                clause = Clause(size)
                clause.add_negative(i,j)
                clause.add_negative(i,k)
                expression.append(clause)

    # 2.1 Clauses for columns (1QUEEN MIN)
    for i in range(size): #column index
        for j in range(size-1): #row index_1
            for k in range(j+1,size): #row index_2
                clause = Clause(size)
                clause.add_negative(j,i)
                clause.add_negative(k,i)
                expression.append(clause)

    # 2.2 Clauses for columns (1QUEEN MAX)
    for i in range(size): #column index
        for j in range(size-1): #row index_1
            for k in range(j+1,size): #row index_2
                clause = Clause(size)
                clause.add_negative(j,i)
                clause.add_negative(k,i)
                expression.append(clause)

    # 3 Clauses for descending diago
    # 3.1 middle and board above
    for i in range(size-1): #index of diago
        for j in range (size-i-1): # number of cases of the diago -1
            for k in range(1,size-i-j):
                clause = Clause(size)
                clause.add_negative(j,j+i)
                clause.add_negative(j+k,j+k+i)
                expression.append(clause)

    # 3.2 board below
    for i in range(1,size-1): #index of diago
        for j in range (size-i-1): # number of cases of the diago -1
            for k in range(1,size-i-j):
                clause = Clause(size)
                clause.add_negative(j+i,j)
                clause.add_negative(j+i+k,j+k)
                expression.append(clause)

    # 4 Clauses for ascending diago
    # 4.1 middle and board above
    for i in range(size-1): #index of diago
        for j in range (size-i-1): # number of cases of the diago -1
            for k in range(1,size-j-i):
                clause = Clause(size)
                clause.add_negative(size-(j+i)-1,j)
                clause.add_negative(size-(j+i+k)-1,j+k)
                expression.append(clause)

    # 4.2 board below
    for i in range(1,size-1): #index of diago
        for j in range (size-i-1): # number of cases of the diago -1
            for k in range(1,size-i-j):
                clause = Clause(size)
                clause.add_negative(size-j-1,j+i)
                clause.add_negative(size-(j+k)-1,j+k+i)
                expression.append(clause)

        
    # your code here

    return expression


if __name__ == '__main__':
    expression = get_expression(4)
    for clause in expression:
        print(clause)
