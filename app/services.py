def calculate_pow(x: int, y: int) -> int:
    return x ** y

def calculate_factorial(n: int) -> int:
    if n == 0:
        return 1
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def calculate_fibonacci(n: int) -> int:
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
