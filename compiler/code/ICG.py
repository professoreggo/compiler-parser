import tkinter as tk
from tkinter import messagebox

class ICGGenerator:
    def __init__(self, root, dictionary, isfloat):
        self.root = root
        self.temp_count = 0
        self.temp_map = {}
        self.dictionary = dictionary
        self.isfloat = isfloat  
        self.statement = []  # Now it's a list to store individual instructions

    def generate_icg(self):
        self._traverse_and_generate(self.root)
        return self.statement

    def _traverse_and_generate(self, node):
        if node is None:
            return None

        # recursively process left and right children
        left = self._traverse_and_generate(node['left'])
        right = self._traverse_and_generate(node['right'])

        # replace left and right with values from the dictionary if they exist
        if left in self.dictionary:
            left = self.dictionary[left]
        if right in self.dictionary:
            right = self.dictionary[right]

        if left is not None and right is not None:
            left_value = self._get_temp_or_value(left)
            right_value = self._get_temp_or_value(right)

            if node['value'] == '=':
                # Handle float conversion if necessary
                if self.isfloat and self._is_float(right_value):
                    self.temp_count += 1
                    temp_float = f"temp{self.temp_count}"
                    self.statement.append(f"{temp_float} = ({int(float(right_value))})intToFloat")  # Append as list item
                    right_value = temp_float

                # Direct assignment
                self.statement.append(f"{left_value} = {right_value}")  # Append as list item
                return left_value

            # Handle float conversion for operations
            if self.isfloat:
                if self._is_float(left_value):
                    self.temp_count += 1
                    temp_float = f"temp{self.temp_count}"
                    self.statement.append(f"{temp_float} = ({int(float(left_value))})intToFloat")  # Append as list item
                    left_value = temp_float
                if self._is_float(right_value):
                    self.temp_count += 1
                    temp_float = f"temp{self.temp_count}"
                    self.statement.append(f"{temp_float} = ({int(float(right_value))})intToFloat")  # Append as list item
                    right_value = temp_float

            # generate the result for the operator
            self.temp_count += 1
            temp_var_result = f"temp{self.temp_count}"
            self.statement.append(f"{temp_var_result} = {left_value} {node['value']} {right_value}")  # Append as list item

            # store the result in the temp map using the unique node ID
            node_id = id(node)
            self.temp_map[node_id] = temp_var_result

            return temp_var_result

        # return the value of the leaf node
        return self._format_value(node['value'])

    def _get_temp_or_value(self, node):
        """Returns the temporary variable or the formatted value of a node."""
        node_id = id(node)
        if node_id in self.temp_map:
            return self.temp_map[node_id]
        return self._format_value(node)

    def _format_value(self, value):
        """Formats the value, appending (float) if necessary."""
        if self.isfloat and isinstance(value, (int, float)):
            return f"{value}(float)"
        return value

    def _is_float(self, value):
        """Checks if the value represents a float."""
        try:
            float(value)
            return '.' in str(value) or isinstance(value, float)
        except ValueError:
            return False

    def display_optimized_code(self):
        """
        Displays the optimized intermediate code in a Tkinter window.
        """
        if not self.statement:
            messagebox.showerror("Error", "No intermediate code generated.")
            return

        ICG_window = tk.Toplevel()
        ICG_window.title("Intermediate Code Generator")

        # Add a Text widget to display the intermediate code
        text_widget = tk.Text(ICG_window, width=60, height=20, font=("Courier New", 12))
        text_widget.pack(pady=10, padx=10)

        # Insert each line from the statement list into the text widget
        for instruction in self.statement:
            text_widget.insert(tk.END, instruction + "\n")

        text_widget.config(state=tk.DISABLED)

