
try:
    print(1/0)
except ZeroDivisionError as ie:
    print("Error: An "+ str(ie) + " exception has occurred")

try:
    n=1/10
    if n < 1:
        raise ValueError("Error: value is too small")
except ZeroDivisionError as ie:
    print("Error: An "+ str(ie) + " exception has occurred")
except ValueError as ve:
    print('Caught Exception: ' + str(ve))
else:
    print("No exceptions, here is your result: " + str(n))
finally:
    print("Exception or not, this code was written by Abishek")