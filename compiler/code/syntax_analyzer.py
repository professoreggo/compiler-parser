import tkinter as tk
from tkinter import Canvas
from collections import deque
class SyntaxAnalyzer:
    def __init__(self, expression , dictionary):
        self.expression = expression
        self.precedence = {'=': 0, '+': 1, '-': 1, '*': 2, '/': 2, '**': 3}
        self.right_associative = {'**'}
        self.output = []
        self.operators = []
        self.dictionary = dictionary

    def is_number(self, token):
        try:
            float(token)  # Try converting the token to a float
            return True
        except ValueError:
            return False
        


    def infix_to_postfix(self):  # Shunting-yard algorithm
        try:
            tokens = self.expression.split()
            i = 0
            while i < len(tokens):
                token = tokens[i]
            
                # Handle '**' as a single operator
                if token == '*' and i + 1 < len(tokens) and tokens[i + 1] == '*':
                    token = '**'
                    i += 1  # Skip the next token

                if self.is_number(token):  # Operand (number or float)
                    self.output.append(token)
                elif token.isalpha():  # Variable
                    self.output.append(token)
                elif token in self.precedence:  # Operator
                    while (self.operators and self.operators[-1] != '(' and
                           (self.precedence[self.operators[-1]] > self.precedence[token] or
                            (self.precedence[self.operators[-1]] == self.precedence[token] and
                            token not in self.right_associative))):
                        self.output.append(self.operators.pop())
                    self.operators.append(token)
                elif token == '(':  # Left parenthesis
                    self.operators.append(token)
                elif token == ')':  # Right parenthesis
                    while self.operators and self.operators[-1] != '(':
                        self.output.append(self.operators.pop())
                    if not self.operators:
                        raise ValueError("Mismatched parentheses detected.")
                    self.operators.pop()  # Discard '('
                else:
                    raise ValueError(f"Invalid token detected: {token}")
            
                i += 1

            while self.operators:  # Pop all remaining operators
                if self.operators[-1] == '(':
                    raise ValueError("Mismatched parentheses detected.")
                self.output.append(self.operators.pop())
        
            return ' '.join(self.output)

        except Exception as e:
            return False


    def postfix_to_tree(self):
        try:
            stack = []
            for token in self.output:
                if self.is_number(token) or token.isalpha():  # Operand (number, float, or variable)
                    stack.append({'value': token, 'left': None, 'right': None})
                elif token in self.precedence:  # Operator
                    right = stack.pop()
                    left = stack.pop()
                    stack.append({'value': token, 'left': left, 'right': right})
            return stack[-1]  # The root of the tree
        except Exception as e:
            return False
class TreeVisualizer:
    def __init__(self, root, dictionary):
        self.root = root
        self.dictionary = dictionary  # Store the dictionary for value replacement
        self.window = tk.Tk()
        self.canvas = Canvas(self.window, width=1200, height=600)  # Increase width for more space
        self.canvas.pack()
        self.draw_tree(self.root, 600, 50, 300, 0)  # Start with larger initial x_offset and centered x

    def draw_tree(self, node, x, y, x_offset, depth):
        if node is None:
            return

        # Replace the node's value with the corresponding value from the dictionary if it exists
        node_value = self.dictionary.get(node['value'], node['value'])

        # Draw the node as a circle with the value inside
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
        self.canvas.create_text(x, y, text=node_value)

        # Calculate new x_offset for children to avoid overlap at deeper levels
        new_x_offset = x_offset // 2 if x_offset > 40 else 40  # Set a minimum offset to keep nodes spaced apart

        # Draw left child
        if node['left']:
            left_x = x - new_x_offset
            self.canvas.create_line(x, y + 20, left_x, y + 70)
            self.draw_tree(node['left'], left_x, y + 70, new_x_offset, depth + 1)

        # Draw right child
        if node['right']:
            right_x = x + new_x_offset
            self.canvas.create_line(x, y + 20, right_x, y + 70)
            self.draw_tree(node['right'], right_x, y + 70, new_x_offset, depth + 1)

    def show(self):
        self.window.mainloop()
