import re
from reserved_words import reserved_words # import reserved words from reserved_words.py
from lexical_analyzer import LexicalAnalyzer # import LexicalAnalyzer class from lexical_analyzer.py 
from syntax_analyzer import SyntaxAnalyzer , TreeVisualizer # import ParseTreeVisualizer class from ParseTreeVisualizer.py
from semantic_analyzer import SemanticAnalyzer # import SemanticAnalyzer class from semantic_analyzer.py


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
    # Convert numeric tokens to ints 
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
     # Convert numeric tokens to floats if possible
    for i, token in enumerate(tokens):
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

    is_float = input("Enter '1' for integer or '2' for float: ")  # check if tokens contains float or pi
    if is_float == '2':
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
    while True:
        user_input = input("Enter a math expression or source code: ")
        

        if '=' in user_input:
            left_side, right_side = user_input.split('=', 1)
            left_side = left_side.strip()
            right_side = right_side.strip()
            
            if not is_valid_identifier(left_side):
                print(f"Invalid identifier: {left_side}, please enter again !")
                continue
            
            right_side , tokens , is_float = convert_math_to_source(right_side)
            
            if not is_valid_expression(right_side):
                print(f"Invalid expression: {right_side}")
                continue
            
            print(f"Valid input: {left_side} = {right_side}")
        else:
            print("Input must contain an '=' sign.")
        expression =  left_side+" = "+right_side
        # Create a lexical analyzer object
        lexical_analyzer = LexicalAnalyzer(tokens, expression)
        lexical_analyzer.analyze()



        visualizer = SyntaxAnalyzer(expression)
        postfix = visualizer.infix_to_postfix()
        print (postfix)



        
        tree_root = visualizer.postfix_to_tree()
        value = TreeVisualizer(tree_root) #a = 3 * 2 / ( 1 - 5 ) ** 2 
        value.show()



        analyzer = SemanticAnalyzer(user_input,is_float)
        analyzer.semantic_analysis()
        
        
        

        

if __name__ == "__main__":
    main()