from code_synth import synthesize_and_verify, synthesize_python, verify_source, TEMPLATES


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


def test_sort_palindrome_even():
    assert "return sorted(items)" in synthesize_python(
        "write a python function that sorts a list"
    )
    assert "def is_palindrome" in synthesize_python(
        "implement a python function that checks if a string is a palindrome"
    )
    assert "n % 2 == 0" in synthesize_python(
        "write a python function that checks if a number is even"
    )


def test_gcd_fib_vowels_unique():
    assert "while b:" in synthesize_python("write a python function that computes the gcd of two numbers")
    assert "def fibonacci" in synthesize_python("implement a python function for the nth fibonacci number")
    assert "aeiou" in synthesize_python("write a python function that counts vowels in a string")
    assert "seen" in synthesize_python("write a python function that returns unique items from a list")


def test_all_templates_verify():
    assert TEMPLATES
    for tmpl in TEMPLATES:
        check = verify_source(tmpl.source, tmpl.examples)
        assert check["ok"], (tmpl.name, check)


def test_synthesize_and_verify_add():
    bundle = synthesize_and_verify("write a python function that adds two numbers")
    assert bundle["verified"] is True
    assert bundle["checked"] >= 2
    assert "return a + b" in bundle["source"]


def test_odd_and_sum_list():
    assert "n % 2 != 0" in synthesize_python(
        "write a python function that checks if a number is odd"
    )
    assert "def sum_list" in synthesize_python(
        "write a python function that sums a list of numbers"
    )
    odd = synthesize_and_verify("write a python function that checks if a number is odd")
    assert odd["verified"] is True
    sl = synthesize_and_verify("write a python function that sums a list")
    assert sl["verified"] is True


def test_lcm_flatten_words_clamp_prime():
    assert "def lcm" in synthesize_python(
        "write a python function that computes the lcm of two numbers"
    )
    assert "out.extend" in synthesize_python(
        "write a python function that flattens a nested list"
    )
    assert "split()" in synthesize_python(
        "write a python function that counts words in a string"
    )
    assert "def clamp" in synthesize_python(
        "write a python function that clamps a number to a range"
    )
    assert "def is_prime" in synthesize_python(
        "write a python function that checks if a number is prime"
    )
    for q in (
        "write a python function that computes the lcm of two numbers",
        "write a python function that flattens a nested list",
        "write a python function that counts words in a string",
        "write a python function that clamps a number to a range",
        "write a python function that checks if a number is prime",
    ):
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
