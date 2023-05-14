import os
import time


def clear():
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')



def measure_time(func) :
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # Capture the function's result
        stop_time = time.time()
        dt = stop_time - start_time
        print(f"Time required for {func.__name__} = {dt} seconds\n")
        return result  # Return the function's result
    return inner


def main():
    pass


if __name__ == '__main__':
    main()
