from Labs.Lab4.io.my_iostream import MyInputOutputStream
from Labs.Lab4.runtime.CommandManager import CommandManager

def lab4():
    iostream = MyInputOutputStream()
    app_manager = CommandManager(iostream)
    app_manager.run()


lab4()

'''
A = Matrix(3, 3)
A.set_row(0, [7, 31.3, 172.09])
A.set_row(1, [31.3, 172.09, 1049.05])
A.set_row(2, [172.09, 1049.05, 6779.43])

B = Matrix(3, 1)
B.set_col(0, [64, 368.03, 2355.72])

print(gauss_linear_solve(A, B))
'''
