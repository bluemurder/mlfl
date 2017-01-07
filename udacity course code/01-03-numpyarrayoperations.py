"""Operations on arrays."""

import numpy as np

def test_run():

    np.random.seed(693)
    a = np.random.randint(0, 10, size = (5, 4))
    print "Array:\n", a

    # Sum of the elements
    print "Sum of all elements:", a.sum()
    print "Sum of each column:\n", a.sum(axis = 0)
    print "Sum of each row:\n", a.sum(axis = 1)

    # Statistics
    print "Minimum of each column:\n", a.min(axis = 0)
    print "Max of each row:\n", a.max(axis = 1)
    print "Mean of all elements:", a.mean()
        

if __name__ == "__main__":
    test_run()
