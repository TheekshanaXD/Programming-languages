import re
from enum import Enum, auto


class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING = auto()
    OPERATOR = auto()
    PUNCTUATION = auto()
    END = auto()


KEYWORDS = {
    "let", "in", "fn", "where", "aug", "or", "not", "gr", "ge", "ls", "le",
    "eq", "ne", "true", "false", "nil", "dummy", "within", "and", "rec"
}

PUNCTUATION = {'(', ')', ';', ','}

OPERATOR_SYMBOLS = r'\+\-\*<>&\.@/:=~\|$!#%\^_\[\]\{\}"\'\?'

TOKEN_REGEX = [
    ("COMMENT", r"//[^\n]*"),
    ("SPACE", r"[ \t\n]+"),
    ("STRING", r"\'(\\[nt\\'\"]|[^\\'])*\'"),
    ("INTEGER", r"\d+"),
    ("KEYWORD", r"\b(" + '|'.join(KEYWORDS) + r")\b"),
    ("IDENTIFIER", r"[A-Za-z][A-Za-z0-9_]*"),
    ("OPERATOR", f"[{OPERATOR_SYMBOLS}]+"),
    ("PUNCTUATION", r"[();,]")
]

COMPILED_PATTERNS = [(name, re.compile(pattern)) for name, pattern in TOKEN_REGEX] #Precompiles regex patterns for performance


class Token:
    def __init__(self, type_: TokenType, value: str):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"<{self.type.name}:{self.value}>"

    def __repr__(self):
        return self.__str__()


def tokenize(input_text):
    """
    Tokenizes input text into a list of tokens for lexical analysis.
    This function processes the input text character by character, matching against
    predefined compiled patterns to identify different types of tokens such as
    keywords, identifiers, integers, strings, operators, and punctuation.
    Args:
        input_text (str): The source code text to be tokenized.
    Returns:
        list[Token]: A list of Token objects representing the lexical elements
                    found in the input text. The list always ends with an EOF token.
    Raises:
        SyntaxError: If an unexpected character is encountered that doesn't match
                    any of the defined token patterns.
    Note:
        - Whitespace and comments are skipped during tokenization
        - The function relies on COMPILED_PATTERNS being defined in the module scope
        - Each token contains a type (from TokenType enum) and the matched text
    """
    tokens = []
    position = 0
    length = len(input_text)

    while position < length:
        matched = False
        for name, pattern in COMPILED_PATTERNS:
            match = pattern.match(input_text, position)
            if match:
                text = match.group(0)
                if name == "SPACE" or name == "COMMENT":
                    pass  # Skip whitespace/comments
                elif name == "KEYWORD":
                    tokens.append(Token(TokenType.KEYWORD, text))
                elif name == "IDENTIFIER":
                    tokens.append(Token(TokenType.IDENTIFIER, text))
                elif name == "INTEGER":
                    tokens.append(Token(TokenType.INTEGER, text))
                elif name == "STRING":
                    tokens.append(Token(TokenType.STRING, text))
                elif name == "OPERATOR":
                    tokens.append(Token(TokenType.OPERATOR, text))
                elif name == "PUNCTUATION":
                    tokens.append(Token(TokenType.PUNCTUATION, text))
                matched = True
                position = match.end()
                break
        if not matched:
            raise SyntaxError(f"Unexpected character at position {position}: '{input_text[position]}'")

    tokens.append(Token(TokenType.END, "EOF"))
    return tokens



# if __name__ == "__main__":
#     import os
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     project_root = os.path.dirname(script_dir)
#     input_path = os.path.join(project_root, "inputs", "input.txt")
#
#     with open(input_path, "r") as f:
#         input_code = f.read()
#
#     token_list = tokenize(input_code)
#     for token in token_list:
#         print(token)


