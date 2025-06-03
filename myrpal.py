import sys
from LexicalAnalyzer.lexical_analyzer import tokenize
from Parser.parser import Parser
from Standardizer.standardizer import ASTFactory  # Import the standardizer

def main():
    if len(sys.argv) < 2:
        print("Usage: python myrpal.py <input_file> [-ast] [-st]")
        return

    file_path = sys.argv[1]
    show_ast = "-ast" in sys.argv
    show_st = "-st" in sys.argv

    try:
        with open(file_path, 'r') as file:
            source = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        # Tokenize and parse
        tokens = tokenize(source)
        parser = Parser(tokens)
        ast_nodes = parser.parse()

        if ast_nodes is None:
            print("Parsing failed.")
            return

        # Show original AST if requested
        if show_ast:
            print("Original AST:")
            for line in parser.convert_ast_to_string_ast():
                print(line)

        # Convert to standardizer format and standardize if requested
        if show_st:
            # Convert parser AST to string format
            string_ast = parser.convert_ast_to_string_ast()
            
            # Create standardizer AST from string representation
            ast_factory = ASTFactory()
            standardizer_ast = ast_factory.get_abstract_syntax_tree(string_ast)
            
            if standardizer_ast:
                # Standardize the AST
                standardizer_ast.standardize()
                
                print("Standardized AST:")
                standardizer_ast.print_ast()
            else:
                print("Failed to create standardizer AST.")

        if not show_ast and not show_st:
            print("Parsing successful. Use -ast to display AST, -st to display standardized AST.")

    except Exception as e:
        print("Error during parsing:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()