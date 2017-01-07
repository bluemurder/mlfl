"""Indexing."""

import numpy as np

def test_run():
    a = np.random.rand(5)
    print "Array:\n", a

    # Accessing using a list of indices
    indices = np.array([1, 1, 2, 3])
    print a[indices]

    # New array
    a = np.array([(20, 25, 10, 23, 26, 32, 10, 5, 0),
                  (0, 2, 50, 20, 0, 1, 28, 5, 0)])
    print "New array:\n", a

    # Mean
    mean = a.mean()
    print "Mean: ", mean

    # Masking
    a[a < mean] = mean
    print a
    
    

if __name__ == "__main__":
    test_run()
