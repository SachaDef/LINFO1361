"""
Class used to represent a clause in CNF for the color grid problem.
Variable X_i_j is true iff cell at position (i,j) has a queen on it.

For example, to create a clause:

X_0_1 or ~X_1_2 or X_3_3

you can do:

clause = Clause(4)
clause.add_positive(0, 1)
clause.add_negative(1, 2)
clause.add_positive(3, 3)

"""


class Clause:

    def __init__(self, size, varname='C'):
        self.varname = varname
        self.n_rows = self.n_columns = size
        self.value = []

    def index(self, row_ind, column_ind):
        if row_ind >= 0 and row_ind < self.n_rows and column_ind >= 0 and column_ind < self.n_columns :
            return row_ind * self.n_columns + column_ind
        else:
            raise ValueError("Indices : row_ind =", row_ind, "column_ind =", column_ind, "is incorrect")

    def str_from_index(self, index):
        if index >= 0:
            index -= 1
        else:
            index += 1
        row_ind = abs(index) // self.n_columns
        column_ind = abs(index) % self.n_columns
        if index < 0:
            return '~{0}_{1}_{2}'.format(self.varname, row_ind, column_ind)
        return '{0}_{1}_{2}'.format(self.varname, row_ind, column_ind)

    def add_positive(self, row_ind, column_ind):
        self.value.append(self.index(row_ind, column_ind)+1)

    def add_negative(self, row_ind, column_ind):
        self.value.append(-self.index(row_ind, column_ind)-1)

    def minisat_str(self):
        return ' '.join([str(x) for x in self.value])

    def __str__(self):
        return ' or '.join([self.str_from_index(x) for x in self.value])


if __name__ == '__main__':
    clause = Clause(3)
    clause.add_positive(1, 1)
    clause.add_negative(1, 2)
    clause.add_positive(2, 2)
    print(clause)
    print(clause.minisat_str())
