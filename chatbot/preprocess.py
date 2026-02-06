import re  # importing regular expression
# from typing import List

def clean_text(text: str) -> str:
    # change input user to lowercase
    text = text.lower()

    # remove punctuation mark
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # remove spacing(too much spacing)
    text = re.sub(r"\s+", " ", text).strip()

    return text