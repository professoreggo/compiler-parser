import re
import tkinter as tk
from tkinter import Canvas, messagebox
from reserved_words import reserved_words

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class SemanticAnalyzer:
    def __init__(self, expression, is_float, dictionary):
        self.expression = expression
        self.is_float = is_float
        self.dictionary = dictionary

    def semantic_analysis(self):
        expr = self.expression

        has_float = self.is_float

        if "=" not in expr:
            messagebox.showerror("Error", "Invalid input: No '=' found in expression.")
            return

        lhs, rhs = expr.split("=", 1)
        lhs = lhs.strip()

        root = self.build_tree(lhs, rhs.strip())

        if has_float:
            root = self.modify_tree_to_float(root)

        self.display_tree_in_new_window(root)

    def build_tree(self, lhs, rhs):
        analyzer = SyntaxAnalyzer(f"{lhs} = {rhs}")
        postfix_expr = analyzer.infix_to_postfix()
        tree = analyzer.postfix_to_tree()
        return tree

    def modify_tree_to_float(self, node):
        if node is None:
            return None

        if node['value'].isdigit():
            float_node = {'value': "int to float "+str(float(node['value'])), 'left': {'value': node['value'], 'left': None, 'right': None}, 'right': None}  
            return float_node   
        else:
            node['left'] = self.modify_tree_to_float(node['left']) 
            node['right'] = self.modify_tree_to_float(node['right'])  
            return node

    def display_tree_in_new_window(self, root):
        visualizer = TreeVisualizer(root,self.dictionary)
        visualizer.show()

class SyntaxAnalyzer:
    def __init__(self, expression):
        self.expression = expression
        self.precedence = {'=': 0, '+': 1, '-': 1, '*': 2, '/': 2, '**': 3}
        self.right_associative = {'**'}
        self.output = []
        self.operators = []

    def is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def infix_to_postfix(self):
        tokens = self.expression.split()

        
        new_expression = tokens[0]
        last_token = tokens[0]

        for token in tokens[1:]:
            if self.is_number(last_token) and token.isalpha() and token not in reserved_words:
                new_expression += " * " + token
            elif last_token.isalpha() and self.is_number(token) and last_token not in reserved_words:
                new_expression += " * " + token
            elif last_token.isalpha() and token.isalpha() and last_token not in reserved_words and token not in reserved_words:
                new_expression += " * " + token
            elif (self.is_number(last_token) or last_token.isalpha()) and token == '(' and last_token not in reserved_words:
                new_expression += " * " + token
            else:
                new_expression += " " + token

            last_token = token

        new_expression = new_expression.replace('^', '**')
        new_expression = new_expression.replace('pi', '3.14')
        tokens = new_expression.split()

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '*' and i + 1 < len(tokens) and tokens[i + 1] == '*':
                token = '**'
                i += 1

            if self.is_number(token):
                self.output.append(token)
            elif token.isalpha():
                self.output.append(token)
            elif token in self.precedence:
                while (self.operators and self.operators[-1] != '(' and
                       (self.precedence[self.operators[-1]] > self.precedence[token] or
                        (self.precedence[self.operators[-1]] == self.precedence[token] and
                         token not in self.right_associative))):
                    self.output.append(self.operators.pop())
                self.operators.append(token)
            elif token == '(':
                self.operators.append(token)
            elif token == ')':
                while self.operators and self.operators[-1] != '(':
                    self.output.append(self.operators.pop())
                self.operators.pop()
            i += 1

        while self.operators:
            self.output.append(self.operators.pop())

        return ' '.join(self.output)

    def postfix_to_tree(self):
        stack = []
        for token in self.output:
            if self.is_number(token) or token.isalpha():
                stack.append({'value': token, 'left': None, 'right': None})
            elif token in self.precedence:
                right = stack.pop()
                left = stack.pop()
                stack.append({'value': token, 'left': left, 'right': right})
        return stack[-1]

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
