"""Arithmetic operations."""

import numpy as np

def test_run():
    a = np.array([(1, 2, 3, 4, 5), (10, 20, 30, 40, 50)])
    print "Array a:\n", a

    # Multiply
    print "Multiply a by 2:\n", 2 * a

    # Division
    print "Multiply a by 2:\n", a / 2.0

    b = np.array([(100, 200, 300, 400, 500),(1, 2, 3, 4, 5)])

    # Add the two arrays
    print "Add a+b:\n", a + b

    # Multiply the two arrays
    print "Mul a*b:\n", a * b

    # Divide the two arrays (remember: values are integers)
    print "Div a/b:\n", a / b
    

if __name__ == "__main__":
    test_run()
