import sys
from LexicalAnalyzer.lexical_analyzer import tokenize
from Parser.parser import Parser

def main():
    if len(sys.argv) < 2:
        print("Usage: python myrpal.py <input_file> [-ast]")
        return

    file_path = sys.argv[1]
    show_ast = "-ast" in sys.argv

    try:
        with open(file_path, 'r') as file:
            source = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()

        if ast is None:
            print("Parsing failed.")
        elif show_ast:
            for line in parser.convert_ast_to_string_ast():
                print(line)
        else:
            print("Parsing successful. Use -ast to display AST.")

    except Exception as e:
        print("Error during parsing:", e)

if __name__ == "__main__":
    main()
