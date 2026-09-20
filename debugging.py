"""AI Debugging Agent helpers — rule-based traceback diagnosis."""
import re

_KNOWN_ERRORS = {
    "ModuleNotFoundError": (
        "Python could not find a module you tried to import.",
        ["The package isn't installed in the current environment."],
        ["Install the package: pip install <package>"],
    ),
    "ImportError": (
        "A specific name could not be imported from a module that was found.",
        ["The module exists but doesn't have the attribute you are importing."],
        ["Check the module's actual exported names."],
    ),
    "SyntaxError": (
        "The code isn't valid Python.",
        ["A missing colon, parenthesis, or bracket."],
        ["Check the line number given in the traceback."],
    ),
    "NameError": (
        "The code refers to a name that doesn't exist in the current scope.",
        ["A typo in a variable or function name."],
        ["Check spelling against where the name was defined."],
    ),
    "TypeError": (
        "An operation was applied to a value of the wrong type.",
        ["Calling a function with the wrong number/type of arguments."],
        ["Check the function signature."],
    ),
    "ValueError": (
        "A function received an argument of the right type but an inappropriate value.",
        ["Parsing a string that isn't in the expected format."],
        ["Validate input before passing it in."],
    ),
    "KeyError": (
        "You tried to access a dictionary key that doesn't exist.",
        ["Typo in the key name."],
        ["Use dict.get(key, default) when the key might be missing."],
    ),
    "IndexError": (
        "You tried to access a list index that's out of range.",
        ["Off-by-one error in a loop bound."],
        ["Check len(sequence) before indexing."],
    ),
    "AttributeError": (
        "You tried to access an attribute that doesn't exist on that object.",
        ["Typo in the attribute name."],
        ["Print type(obj) and dir(obj)."],
    ),
    "ZeroDivisionError": (
        "The code attempted to divide by zero.",
        ["A denominator computed from data that wasn't validated."],
        ["Guard the division with an explicit zero check."],
    ),
    "FileNotFoundError": (
        "The code tried to open a file that doesn't exist.",
        ["Wrong relative path."],
        ["Print os.getcwd() to check the working directory."],
    ),
}


def diagnose_traceback(text: str) -> dict:
    for name, (explanation, causes, suggestions) in _KNOWN_ERRORS.items():
        if re.search(rf"\b{name}\b", text):
            return {"error_type": name, "explanation": explanation,
                    "likely_causes": causes, "suggestions": suggestions, "category": "python"}
    return {"error_type": None, "explanation": None, "likely_causes": [], "suggestions": [], "category": None}
