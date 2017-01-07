"""Modifying array elements."""

import numpy as np

def test_run():
    a = np.random.rand(5, 4)
    print "Array:\n", a

    # Assign single value to entire row
    a[0, :] = 2
    print "Modified:\n", a

    # Assign single value to entire row
    a[:, 3] = [1, 2, 3, 4, 5]
    print "Modified:\n", a

    

if __name__ == "__main__":
    test_run()
