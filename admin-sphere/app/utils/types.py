from typing import TypedDict

# Define the structure of the ChoiceType TypedDict
ChoiceType = TypedDict(
    "ChoiceType",  # Name of the TypedDict
    {
        "choice": str,  # Key "choice" with value of type str
        "status": bool   # Key "status" with value of type bool
    }
)

