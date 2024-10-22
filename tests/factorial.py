def factorial(n):
    """Возвращает факториал числа n."""
    if n < 0:
        raise ValueError("Факториал не определен для отрицательных чисел.")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result