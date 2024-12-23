import tkinter as tk
from tkinter import messagebox
import re

class AssemblyCodeGenerator:
    def __init__(self, source_code_output):

        self.source_code_output = source_code_output
        self.assembly_code = []

    def generate_assembly_code(self):

        if not self.source_code_output:
            messagebox.showerror("Error", "No source code output found to generate assembly code.")
            return

        # Split the source code output into lines
        intermediate_lines = self.source_code_output.split("\n")
        self.assembly_code = []

        # Mapping to assembly instructions
        for line in intermediate_lines:
            line = line.strip()
            if not line:
                continue

            if "=" in line:  # Handle assignment
                lhs, rhs = line.split("=", 1)
                lhs, rhs = lhs.strip(), rhs.strip()

                # Handle arithmetic expressions
                if any(op in rhs for op in ["+", "-", "*", "/"]):
                    tokens = re.split(r'(\+|\-|\*|/)', rhs) 
                    register = "R2"  # Assume a single register for simplicity

                    first_operand = tokens[0].strip()

                    # Load the first identifier into the register if it's not a digit
                    if not first_operand.isdigit():
                        self.assembly_code.append(f"LD {register}, {first_operand}")

                    # Process the remaining tokens
                    for i in range(1, len(tokens), 2):
                        operator = tokens[i]
                        operand = tokens[i + 1].strip()

                        if operand.isdigit():
                            # Use the number directly in the operation
                            if operator == "+":
                                self.assembly_code.append(f"ADD {register}, {operand}")
                            elif operator == "-":
                                self.assembly_code.append(f"SUB {register}, {operand}")
                            elif operator == "*":
                                self.assembly_code.append(f"MUL {register}, {operand}")
                            elif operator == "/":
                                self.assembly_code.append(f"DIV {register}, {operand}")
                        else:
                            # Load the identifier into the register and perform the operation
                            if i == 1 and first_operand.isdigit():
                                self.assembly_code.append(f"LD {register}, {operand}")
                            if operator == "+":
                                self.assembly_code.append(f"ADD {register}, {first_operand}")
                            elif operator == "-":
                                self.assembly_code.append(f"SUB {register}, {first_operand}")
                            elif operator == "*":
                                self.assembly_code.append(f"MUL {register}, {first_operand}")
                            elif operator == "/":
                                self.assembly_code.append(f"DIV {register}, {first_operand}")

                    # Store the result in the left-hand side identifier
                    self.assembly_code.append(f"STR {lhs}, {register}")
                else:
                    # Simple assignment
                    self.assembly_code.append(f"MOV {rhs}, {lhs}")
            else:
                self.assembly_code.append(f"# Unrecognized statement: {line}")

        self.display_assembly_code()  # Automatically display the generated assembly code

    def display_assembly_code(self):
        """
        Displays the generated assembly code in a new Tkinter window.
        """
        if not self.assembly_code:
            messagebox.showerror("Error", "No assembly code generated.")
            return

        assembly_window = tk.Toplevel()
        assembly_window.title("Assembly Code Generator")

        # Add a Text widget to display the assembly code
        text_widget = tk.Text(assembly_window, width=60, height=20, font=("Courier New", 12))
        text_widget.pack(pady=10, padx=10)

        # Insert the assembly code into the text widget
        for instruction in self.assembly_code:
            text_widget.insert(tk.END, instruction + "\n")

        text_widget.config(state=tk.DISABLED)

    def run(self):
        """
        Executes the generation and display of assembly code.
        """
        self.generate_assembly_code()
        self.display_assembly_code()
