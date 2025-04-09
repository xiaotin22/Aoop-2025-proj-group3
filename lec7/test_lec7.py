import lec7
import pytest

# please write a test for fib function
def test_rev_list():
    assert lec7.rev_list([1,2,3,4]) == [4,3,2,1]
    assert lec7.rev_list([1,2,3]) == [3,2,1]
    assert lec7.rev_list([1,2]) == [2,1]
    assert lec7.rev_list([1]) == [1]
    assert lec7.rev_list([]) == []
    assert lec7.rev_list([-1,-2,-3]) == [-3,-2,-1]
    assert lec7.rev_list([-1,-2,0]) == [-2,-1,0]

def test_primes_list():
    assert lec7.primes_list(2) == [2]
    assert lec7.primes_list(3) == [2,3]
    assert lec7.primes_list(4) == [2,3]
    assert lec7.primes_list(5) == [2,3,5]
    assert lec7.primes_list(6) == [2,3,5]



    