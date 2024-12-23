from reserved_words import reserved_words, special_symbols
import re
class LexicalAnalyzer:
    def __init__(self, expression):
        self.tokens = expression.split()
        self.variables = {}
        self.variable_id = 1
        self.expression = expression

    def is_float(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def is_int(self, token):
        try:
            int(token)
            return True
        except ValueError:
            return False

    def is_valid_token(self, token):
        # Check if the token is a valid identifier, reserved word, special symbol, or numeric literal
        
        return (
            re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", token) or
            token in reserved_words or
            token in special_symbols or
            self.is_int(token) or
            self.is_float(token) 
        )

    def lexical_analyzer(self):
        for key, value in self.variables.items():
            if key in self.expression:
                self.expression = self.expression.replace(key, value)

    def analyze(self):
        for token in self.tokens:
            if not self.is_valid_token(token):
                print("Invalid token detected Lexical error raised")
                return False, False
                #raise ValueError(f"Invalid token detected Lexical error raised")

            if (
                token not in reserved_words
                and token not in special_symbols
                and not self.is_float(token)
                and not self.is_int(token)
            ):
                if token not in self.variables:
                    self.variables[token] = "id" + str(self.variable_id)
                    self.variable_id += 1

        print(self.variables)
        self.lexical_analyzer()
        print("Lexical analyzer result:")
        print(self.expression)
        return self.variables, self.expression
        
