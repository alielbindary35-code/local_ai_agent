def fibonacci(n):
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed)
    
    Returns:
        int: The nth Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Example usage
if __name__ == "__main__":
    # Calculate first 10 Fibonacci numbers
    for i in range(10):
        print(f"fibonacci({i}) = {fibonacci(i)}")

