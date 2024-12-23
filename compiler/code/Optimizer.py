import tkinter as tk
from tkinter import messagebox
import re

class CodeOptimizer:
    def __init__(self, source_code_output):
        self.source_code_output = source_code_output
        self.intermediate_code = []
        self.temp_counter = 1

    def get_temp(self):

        temp_var = f"Temp{self.temp_counter}"
        self.temp_counter += 1
        return temp_var

    def generate_intermediate_code(self, expr):

        tokens = re.split(r'(\+|\-|\*|/)', expr)
        output_stack = []  # For postfix expression
        operator_stack = []  # For operators

        precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

        def process_operator(op):
            while (operator_stack and
                   operator_stack[-1] != "(" and
                   precedence[operator_stack[-1]] >= precedence[op]):
                output_stack.append(operator_stack.pop())
            operator_stack.append(op)

        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if token.isalnum() or re.match(r'\d+\.\d+', token):  # Operand
                output_stack.append(token)
            elif token in precedence:  # Operator
                process_operator(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output_stack.append(operator_stack.pop())
                operator_stack.pop()  # Pop '('

        while operator_stack:
            output_stack.append(operator_stack.pop())

        # Generate intermediate code from postfix
        stack = []
        for token in output_stack:
            if token.isalnum() or re.match(r'\d+\.\d+', token):  # Operand
                stack.append(token)
            elif token in precedence:  # Operator
                right = stack.pop()
                left = stack.pop()
                temp_var = self.get_temp()
                self.intermediate_code.append(f"{temp_var} = {left} {token} {right}")
                stack.append(temp_var)

        return stack.pop()

    def optimize_code(self):
        if len(self.intermediate_code) > 1:
            last_assignment = self.intermediate_code[-1]
            second_last = self.intermediate_code[-2]

            # Extract temp variable from the second last line
            if "=" in second_last:
                second_last_lhs, second_last_rhs = second_last.split("=", 1)
                second_last_lhs = second_last_lhs.strip()

            # Replace the temp variable in the final assignment with its computation
            if second_last_lhs in last_assignment:
                optimized_final = last_assignment.replace(second_last_lhs, second_last_rhs.strip())
                self.intermediate_code[-1] = optimized_final
                self.intermediate_code.pop(-2)  # Remove the second last line

    def display_optimized_code(self):
        
        if not self.intermediate_code:
            messagebox.showerror("Error", "No intermediate code generated.")
            return

        optimized_window = tk.Toplevel()
        optimized_window.title("Optimized Code")

        text_widget = tk.Text(optimized_window, width=60, height=20, font=("Helvetica", 12))
        text_widget.pack(pady=10, padx=10)

        for line in self.intermediate_code:
            text_widget.insert(tk.END, line + "\n")

        text_widget.config(state=tk.DISABLED)

    def run(self):
      
        if "=" not in self.source_code_output:
            messagebox.showerror("Error", "Invalid input: No '=' found in expression.")
            return

        lhs, rhs = self.source_code_output.split("=", 1)
        lhs = lhs.strip()
        rhs = rhs.strip()

        final_result = self.generate_intermediate_code(rhs)
        self.intermediate_code.append(f"{lhs} = {final_result}")

        self.optimize_code()
        self.display_optimized_code()


    
