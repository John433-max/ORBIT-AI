from code_synth import synthesize_python


def test_add_multiply_subtract():
    assert "return a + b" in synthesize_python("write a python function that adds two numbers")
    assert "def multiply" in synthesize_python("implement a python function that multiplies two numbers")
    assert "return a - b" in synthesize_python("write a python function that subtracts two numbers")


def test_max_reverse_factorial():
    assert "def maximum" in synthesize_python("write a function that returns the maximum of two numbers")
    assert "[::-1]" in synthesize_python("implement a python function to reverse a string")
    assert "def factorial" in synthesize_python("write a python function for factorial")


def test_divide_average_abs_power():
    assert "def divide" in synthesize_python("write a python function that divides two numbers")
    assert "return a / b" in synthesize_python("implement a python function that divides two numbers")
    assert "def average" in synthesize_python("write a python function that averages two numbers")
    assert "def absolute" in synthesize_python("write a python function for the absolute value")
    assert "def power" in synthesize_python("write a python function that raises a number to a power")
