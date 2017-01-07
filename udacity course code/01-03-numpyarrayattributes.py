"""Array attributes."""

import numpy as np

def test_run():
    # Generate an array full of random numbers, uniformly distributed from [0.0, 1.0)
    a = np.random.random((5, 4))
    print a
    print a.shape
    print len(a,shape)
    print a.size
    print a.dtype
        

if __name__ == "__main__":
    test_run()
