from reserved_words import reserved_words, special_symbols

class LexicalAnalyzer:
    def __init__(self, tokens, expression):
        self.tokens = expression.split()
        self.variables = {} #{'y': 'id1', 'x': 'id2', 'z': 'id3'}
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
    def lexical_analyzer(self):
        for key, value in self.variables.items():
            if key in self.expression:
                self.expression = self.expression.replace(key, value)




    def analyze(self):
        for token in self.tokens:
            if token not in reserved_words and token not in special_symbols and not self.is_float(token) and not self.is_int(token):
                if token not in self.variables:
                    self.variables[token] = "id" + str(self.variable_id)
                    self.variable_id += 1
        print(self.variables)
        self.lexical_analyzer()
        print(self.expression)
        
