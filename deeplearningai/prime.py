#!/usr/bin/env python3
import timeit

def is_prime(n):
    if n <= 1:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True

def sum_of_primes(numbers):
    total = 0
    for number in numbers:
        if is_prime(number):
            print(f"Found prime: {number}")
            total += number
    return total

if __name__ == "__main__":

    numbers = list(range(1, 10000))
    print(f"Sum of primes: {sum_of_primes(numbers)}")
    execution_time = timeit.timeit('sum_of_primes(numbers)', globals=globals(), number=1)
    print(f"Execution time: {execution_time} seconds")
