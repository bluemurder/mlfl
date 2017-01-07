"""Generating random numbers."""

import numpy as np

def test_run():
        # Generate an array full of random numbers, uniformly distributed from [0.0, 1.0)
        print np.random.random((5, 4))

        # Sample from a Gaussian distribution
        print np.random.normal(size = (2, 3))# standard normal (mean = 0, s.d. = 1)
        print np.random.normal(50, 10, size = (2, 3)) # mean = 50, s.d. = 10

        # Random integers
        print np.random.randint(10)
        print np.random.randint(0, 10) # a single integer in [0, 10)
        print np.random.randint(0, 10, size = 5) # 5 random integers in [0, 10)
        print np.random.randint(0, 10, size = (2, 3)) # 2x3 array
        

if __name__ == "__main__":
    test_run()
