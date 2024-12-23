import re
from reserved_words import reserved_words # import reserved words from reserved_words.py
from lexical_analyzer import LexicalAnalyzer # import LexicalAnalyzer class from lexical_analyzer.py 
from syntax_analyzer import SyntaxAnalyzer , TreeVisualizer # import ParseTreeVisualizer class from ParseTreeVisualizer.py
from semantic_analyzer import SemanticAnalyzer # import SemanticAnalyzer class from semantic_analyzer.py
from code_generator import AssemblyCodeGenerator # import AssemblyCodeGenerator class from code_generator.py
from ICG import ICGGenerator
from Optimizer import CodeOptimizer
import tkinter as tk
from tkinter import ttk


def is_valid_identifier(identifier):
    return re.match(r'^[^\d\W]\w*\Z', identifier) is not None

def is_valid_expression(expression):
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z_0-9]*$', expression)) is not None


# def contains_float_or_pi(lst): # check if the list contains float or pi

#     for item in lst:
#         if '.' in item or item == 'pi':
#             return True
#     return False


def int_source(tokens):
  
    for i, token in enumerate(tokens):
        try:
            tokens[i] = int(token)
        except ValueError:
            pass  # Leave token as a string if it can't be converted

    new_expression = str(tokens[0])
    last_token = tokens[0]

    for token in tokens[1:]: 
        # Multiply numbers followed by variables except reserved words
        if isinstance(last_token, int) and isinstance(token, str) and token.isalpha() and token not in reserved_words: 
            new_expression += " * " + str(token)
        # Multiply variables followed by numbers except reserved words
        elif isinstance(last_token, str) and last_token.isalpha() and isinstance(token, int) and last_token not in reserved_words:
            new_expression += " * " + str(token)

        # Multiply consecutive variables except reserved words
        elif isinstance(last_token, str) and last_token.isalpha() and isinstance(token, str) and token.isalpha() and last_token not in reserved_words and token not in reserved_words:
            new_expression += " * " + str(token)
            
        # Multiply numbers or variables followed by an opening parenthesis
        elif( isinstance(last_token, int) or last_token.isalpha() ) and token == '(' and last_token not in reserved_words:
            new_expression += " * " + str(token)

        else:
            new_expression += " " + str(token) # concatenate other tokens

        last_token = token
    
    new_expression = new_expression.replace('^', '**')
    for i, token in enumerate(tokens):
        if token == '^':
            tokens[i] = '**'

    return new_expression , tokens


def float_source(tokens):
                                            
    for i, token in enumerate(tokens): # Convert numeric tokens to floats if possible
        try:
            tokens[i] = float(token)
        except ValueError:
            pass  # Leave token as a string if it can't be converted

    new_expression = str(tokens[0])
    last_token = tokens[0]

    for token in tokens[1:]: 
        # Multiply numbers followed by variables except reserved words
        if isinstance(last_token, float) and isinstance(token, str) and token.isalpha() and token not in reserved_words: 
            new_expression += " * " + str(token)
        # Multiply variables followed by numbers except reserved words
        elif isinstance(last_token, str) and last_token.isalpha() and isinstance(token, float) and last_token not in reserved_words:
            new_expression += " * " + str(token)

        # Multiply consecutive variables except reserved words
        elif isinstance(last_token, str) and last_token.isalpha() and isinstance(token, str) and token.isalpha() and last_token not in reserved_words and token not in reserved_words:
            new_expression += " * " + str(token)
            
        # Multiply numbers or variables followed by an opening parenthesis
        elif( isinstance(last_token, float) or last_token.isalpha() ) and token == '(' and last_token not in reserved_words:
            new_expression += " * " + str(token)

        else:
            new_expression += " " + str(token) # concatenate other tokens

        last_token = token

    # Replace symbols for Python syntax
    new_expression = new_expression.replace('^', '**')
    new_expression = new_expression.replace('pi', '3.14')
    for i, token in enumerate(tokens):
        if token == '^':
            tokens[i] = '**'
        elif token == 'pi':
            tokens[i] = '3.14'

    return new_expression , tokens

def convert_math_to_source(math_expression):  # main method to convert math expression to source code

    tokens = math_expression.split()

    is_float = radio_var.get()  # check if tokens contains float or pi
    if is_float == 'float':
        is_float = True
    else:
        is_float = False

    if is_float:                             # perform method for float
        print("is float")
        new_expression , tokens= float_source(tokens)
    else:                                    # perform method for int
        print("is int")                      
        new_expression , tokens = int_source(tokens)
    
    return new_expression , tokens , is_float
   
def main():
    user_input = entry.get()  # Get the user input
    output_text.delete(1.0, tk.END)  # Clear the output text area

    if not user_input.strip():  # If input is empty
        output_text.after(0, lambda: output_text.insert(tk.END, "Please enter a valid expression.\n"))
        return

    if '=' in user_input:
        left_side, right_side = user_input.split('=', 1)
        left_side = left_side.strip()
        right_side = right_side.strip()

        if not is_valid_identifier(left_side):
            output_text.after(0, lambda: output_text.insert(tk.END, f"Invalid identifier: {left_side}. Please enter again!\n"))
            return

        right_side, tokens, is_float = convert_math_to_source(right_side)

        if not is_valid_expression(right_side):
            output_text.after(0, lambda: output_text.insert(tk.END, f"Invalid expression: {right_side}\n"))
            return

        output_text.after(0, lambda: output_text.insert(tk.END, f"Valid input: {left_side} = {right_side}\n"))
    else:
        output_text.after(0, lambda: output_text.insert(tk.END, "Input must contain an '=' sign.\n"))
        return

    expression = f"{left_side} = {right_side}"

    # Lexical Analyzer
    if left_side in right_side:
        output_text.after(0, lambda: output_text.insert(tk.END, "Lexical error detected.\n"))
        return

    try:
        lexical_analyzer = LexicalAnalyzer(expression)
        dictionary, new_expression = lexical_analyzer.analyze()
        if not dictionary:
            output_text.after(0, lambda: output_text.insert(tk.END, "Lexical analysis failed.\n"))

            
            return
    except Exception as e:
        output_text.after(0, lambda: output_text.insert(tk.END, f"Lexical analysis error: {e}\n"))
        return

    output_text.after(0, lambda: output_text.insert(tk.END, f"Lexical Analysis: {dictionary}\n"))
    output_text.after(0, lambda: output_text.insert(tk.END, f"Output:  {new_expression}\n"))

    # Syntax Analyzer
    try:
        visualizer = SyntaxAnalyzer(expression, dictionary)
        postfix = visualizer.infix_to_postfix()
        if not postfix:
            output_text.after(0, lambda: output_text.insert(tk.END, "Syntax error detected.\n"))
            return
        tree_root = visualizer.postfix_to_tree()
        if not tree_root:
            output_text.after(0, lambda: output_text.insert(tk.END, "Syntax error detected.\n"))
            return
        value = TreeVisualizer(tree_root, dictionary)
        value.show()
    except Exception as e:
        output_text.after(0, lambda: output_text.insert(tk.END, f"Syntax analysis error: {e}\n"))
        return

    # Semantic Analyzer
    try:
        analyzer = SemanticAnalyzer(user_input, is_float, dictionary)
        analyzer.semantic_analysis()
    except Exception as e:
        output_text.insert(tk.END, f"Semantic analysis error: {e}\n")
        return

    # ICG
    try:
        icg_generator = ICGGenerator(tree_root, dictionary, is_float)
        icg_generator.generate_icg()
        icg_generator.display_optimized_code()
    except Exception as e:
        output_text.insert(tk.END, f"ICG generation error: {e}\n")
        return

    # Optimizer
    try:
        optimizer = CodeOptimizer(new_expression)
        optimizer.run()
    except Exception as e:
        output_text.insert(tk.END, f"Code optimization error: {e}\n")
        return

    # Code Generator
    try:
        code = AssemblyCodeGenerator(new_expression)
        code.generate_assembly_code()
    except Exception as e:
        output_text.insert(tk.END, f"Assembly code generation error: {e}\n")
        return

    output_text.insert(tk.END, "Processing completed successfully.\n")
    entry.delete(0, tk.END)  # Clear the entry field after processing


# Function to handle the button click
def perform_action():
    main()

    output_text.after(0, lambda: output_text.insert(tk.END, "Processing completed successfully.\n"))
    entry.delete(0, tk.END)  # Clear the entry field after processing



import threading

def perform_action():
    # Start a separate thread for the main function
    processing_thread = threading.Thread(target=main)
    processing_thread.daemon = True  # Daemonize the thread to exit with the program
    processing_thread.start()



# Create the main window
root = tk.Tk()
root.title("GUI Example")

# Create an input field
entry_label = ttk.Label(root, text="Enter a value:")
entry_label.pack(pady=5)
entry = ttk.Entry(root, width=30)
entry.pack(pady=5)

# Create radio buttons for selecting data type
radio_var = tk.StringVar(value="int")
radio_frame = ttk.LabelFrame(root, text="Select Type")
radio_frame.pack(pady=10, padx=10)

int_radio = ttk.Radiobutton(radio_frame, text="Integer", variable=radio_var, value="int")
int_radio.pack(side=tk.LEFT, padx=10)
float_radio = ttk.Radiobutton(radio_frame, text="Float", variable=radio_var, value="float")
float_radio.pack(side=tk.LEFT, padx=10)

# Create a text area to display output
output_label = ttk.Label(root, text="Output:")
output_label.pack(pady=5)
output_text = tk.Text(root, height=10, width=50, state=tk.NORMAL)
output_text.pack(pady=5)

# Create a button to perform the action
action_button = ttk.Button(root, text="Process", command=perform_action)
action_button.pack(pady=10)

# Run the application
root.mainloop()