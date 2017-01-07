"""Accessing array elements."""

import numpy as np

def test_run():
    a = np.random.rand(5, 4)
    print "Array:\n", a

    # Element in a specified position
    element = a[3, 2]
    print element

    # Elements in range
    print a[0, 1:3]

    # Slicing
    # Note: slice n:m:t specifies a range that starts at n, stops before m, in steps of size t
    print a[:, 0:3:2] #will select columns 0 and 2 for every row
    #print a[:, 0:3:1] #will select columns 0, 1 and 2 for every row
    #print a[:, 0:3:3] #will select columns 0 for every row

if __name__ == "__main__":
    test_run()
