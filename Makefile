PYTHON = python

# Default target: runs the RPAL processor with the specified file
# file = ./Tests/Test_1.rpal
run:
	$(PYTHON) myrpal.py $(file)

# Target to print the AST
ast:
	$(PYTHON) myrpal.py $(file) -ast

# Target to print the standardized AST
st:
	$(PYTHON) myrpal.py $(file) -st

clean:
	rm -rf _pycache_ *.pyc

# Phony targets to avoid conflicts with files named 'run', 'ast', or 'st'
.PHONY: run ast st