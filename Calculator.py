"""Hello World Calculator.

A modern, themed desktop calculator built with Tkinter.
"""

from __future__ import annotations

import ast
import math
import tkinter as tk


class SafeEvaluator(ast.NodeVisitor):
    """Evaluate simple math expressions safely with AST."""

    ALLOWED_BINARY = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.Mod: lambda a, b: a % b,
        ast.Pow: lambda a, b: a**b,
    }

    ALLOWED_UNARY = {
        ast.UAdd: lambda a: +a,
        ast.USub: lambda a: -a,
    }

    ALLOWED_FUNCTIONS = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
    }

    ALLOWED_NAMES = {
        "pi": math.pi,
        "e": math.e,
    }

    def visit_Expression(self, node: ast.Expression) -> float:
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> float:
        op_type = type(node.op)
        if op_type not in self.ALLOWED_BINARY:
            raise ValueError("Unsupported operation")
        left = self.visit(node.left)
        right = self.visit(node.right)
        return self.ALLOWED_BINARY[op_type](left, right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> float:
        op_type = type(node.op)
        if op_type not in self.ALLOWED_UNARY:
            raise ValueError("Unsupported unary operation")
        return self.ALLOWED_UNARY[op_type](self.visit(node.operand))

    def visit_Constant(self, node: ast.Constant) -> float:
        if not isinstance(node.value, (int, float)):
            raise ValueError("Only numeric values are allowed")
        return float(node.value)

    def visit_Name(self, node: ast.Name) -> float:
        if node.id not in self.ALLOWED_NAMES:
            raise ValueError("Unsupported identifier")
        return float(self.ALLOWED_NAMES[node.id])

    def visit_Call(self, node: ast.Call) -> float:
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function call")
        func_name = node.func.id
        if func_name not in self.ALLOWED_FUNCTIONS:
            raise ValueError("Unsupported function")
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")
        if len(node.args) != 1:
            raise ValueError("Function requires exactly one argument")
        value = self.visit(node.args[0])
        return float(self.ALLOWED_FUNCTIONS[func_name](value))

    def generic_visit(self, node: ast.AST) -> float:
        raise ValueError("Invalid expression")


def safe_eval(expression: str) -> float:
    """Parse and evaluate a numeric expression without using eval."""
    normalized = expression.replace("^", "**")
    parsed = ast.parse(normalized, mode="eval")
    return SafeEvaluator().visit(parsed)


class HelloWorldCalculator(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Hello World Calculator")
        self.geometry("560x740")
        self.minsize(500, 680)

        self.expression_var = tk.StringVar(value="")
        self.preview_var = tk.StringVar(value="Preview: ")
        self.status_var = tk.StringVar(value="Ready. Create something brilliant.")
        self.memory_value = 0.0
        self.dark_mode = False
        self._status_after_id: str | None = None

        self.themes = {
            "light": {
                "bg": "#F3EFE6",
                "panel": "#FFFDF8",
                "accent": "#1D6F5F",
                "accent_alt": "#D97706",
                "text": "#1F2937",
                "muted": "#5B6473",
                "button": "#EAE4D8",
                "button_hover": "#DED5C5",
            },
            "dark": {
                "bg": "#111827",
                "panel": "#1F2937",
                "accent": "#22C55E",
                "accent_alt": "#F59E0B",
                "text": "#F9FAFB",
                "muted": "#C7CEDB",
                "button": "#2D3748",
                "button_hover": "#374151",
            },
        }

        self.configure(padx=14, pady=14)
        self._build_ui()
        self._apply_theme()
        self.expression_var.trace_add("write", self._update_preview)
        self.bind("<Key>", self._handle_keypress)
        self.entry.focus_set()

    def _theme(self) -> dict[str, str]:
        return self.themes["dark" if self.dark_mode else "light"]

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.header_frame = tk.Frame(self, bd=0, highlightthickness=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(
            self.header_frame,
            text="HELLO, WORLD CALCULATOR",
            font=("Segoe UI Semibold", 14),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = tk.Label(
            self.header_frame,
            text="Beautiful math, one expression at a time",
            font=("Segoe UI", 10),
            anchor="w",
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w")

        self.theme_button = tk.Button(
            self.header_frame,
            text="Toggle Theme",
            relief="flat",
            cursor="hand2",
            command=self._toggle_theme,
        )
        self.theme_button.grid(row=0, column=1, rowspan=2, padx=(8, 0))

        self.display_frame = tk.Frame(self, bd=0, highlightthickness=0, padx=12, pady=12)
        self.display_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.display_frame.grid_columnconfigure(0, weight=1)

        self.entry = tk.Entry(
            self.display_frame,
            textvariable=self.expression_var,
            justify="right",
            font=("Consolas", 24),
            relief="flat",
            bd=0,
            insertwidth=0,
        )
        self.entry.grid(row=0, column=0, sticky="ew")

        self.preview_label = tk.Label(
            self.display_frame,
            textvariable=self.preview_var,
            justify="right",
            anchor="e",
            font=("Segoe UI", 10),
        )
        self.preview_label.grid(row=1, column=0, sticky="ew", pady=(6, 0))

        self.button_frame = tk.Frame(self, bd=0, highlightthickness=0)
        self.button_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        for col in range(5):
            self.button_frame.grid_columnconfigure(col, weight=1)
        for row in range(7):
            self.button_frame.grid_rowconfigure(row, weight=1)

        self.buttons = {}
        layout = [
            ["MC", "MR", "M+", "M-", "<-"],
            ["C", "(", ")", "%", "/"],
            ["sin", "cos", "tan", "^", "*"],
            ["7", "8", "9", "sqrt", "-"],
            ["4", "5", "6", "log", "+"],
            ["1", "2", "3", "ln", "="],
            ["+/-", "0", ".", "pi", "e"],
        ]

        for row_index, row in enumerate(layout):
            for col_index, label in enumerate(row):
                button = tk.Button(
                    self.button_frame,
                    text=label,
                    font=("Segoe UI Semibold", 12),
                    relief="flat",
                    cursor="hand2",
                    command=lambda value=label: self._on_button(value),
                )
                button.grid(row=row_index, column=col_index, sticky="nsew", padx=4, pady=4, ipady=10)
                button.bind("<ButtonPress-1>", self._button_press_visual)
                button.bind("<ButtonRelease-1>", self._button_release_visual)
                self.buttons[label] = button

        self.history_frame = tk.Frame(self, bd=0, highlightthickness=0, padx=12, pady=10)
        self.history_frame.grid(row=3, column=0, sticky="nsew")
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_rowconfigure(1, weight=1)

        self.history_title = tk.Label(
            self.history_frame,
            text="History",
            font=("Segoe UI Semibold", 11),
            anchor="w",
        )
        self.history_title.grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.history_list = tk.Listbox(
            self.history_frame,
            font=("Consolas", 11),
            activestyle="none",
            highlightthickness=0,
            bd=0,
        )
        self.history_list.grid(row=1, column=0, sticky="nsew")
        self.history_list.bind("<Double-Button-1>", self._reuse_history)

        self.status_label = tk.Label(
            self,
            textvariable=self.status_var,
            anchor="w",
            font=("Segoe UI", 9),
            padx=2,
        )
        self.status_label.grid(row=4, column=0, sticky="ew", pady=(10, 0))

    def _apply_theme(self) -> None:
        t = self._theme()
        self.configure(bg=t["bg"])

        self.header_frame.configure(bg=t["bg"])
        self.title_label.configure(bg=t["bg"], fg=t["accent"])
        self.subtitle_label.configure(bg=t["bg"], fg=t["muted"])

        self.theme_button.configure(
            bg=t["accent_alt"],
            fg=t["panel"],
            activebackground=t["accent"],
            activeforeground=t["panel"],
            padx=10,
            pady=6,
        )

        self.display_frame.configure(bg=t["panel"])
        self.entry.configure(
            bg=t["panel"],
            fg=t["text"],
            disabledbackground=t["panel"],
            disabledforeground=t["text"],
        )
        self.preview_label.configure(bg=t["panel"], fg=t["muted"])

        self.button_frame.configure(bg=t["bg"])
        ops = {"/", "*", "-", "+", "=", "^", "%"}
        funcs = {"sin", "cos", "tan", "sqrt", "log", "ln", "pi", "e"}
        memory_keys = {"MC", "MR", "M+", "M-"}
        for label, button in self.buttons.items():
            if label in ops:
                bg_color = t["accent"]
                fg_color = t["panel"]
            elif label in funcs:
                bg_color = t["accent_alt"]
                fg_color = t["panel"]
            elif label in memory_keys:
                bg_color = t["button_hover"]
                fg_color = t["text"]
            else:
                bg_color = t["button"]
                fg_color = t["text"]
            button.configure(
                bg=bg_color,
                fg=fg_color,
                activebackground=t["button_hover"],
                activeforeground=t["text"],
            )

        self.history_frame.configure(bg=t["panel"])
        self.history_title.configure(bg=t["panel"], fg=t["text"])
        self.history_list.configure(
            bg=t["panel"],
            fg=t["text"],
            selectbackground=t["accent"],
            selectforeground=t["panel"],
        )

        self.status_label.configure(bg=t["bg"], fg=t["muted"])

    def _toggle_theme(self) -> None:
        self.dark_mode = not self.dark_mode
        self._apply_theme()
        mode = "Dark" if self.dark_mode else "Light"
        self._set_status(f"Switched to {mode} mode.")

    def _set_status(self, message: str) -> None:
        self.status_var.set(message)
        t = self._theme()
        pulse_color = t["accent_alt"]
        base_color = t["muted"]
        self.status_label.configure(fg=pulse_color)

        if self._status_after_id is not None:
            self.after_cancel(self._status_after_id)

        self._status_after_id = self.after(
            200,
            lambda: self.status_label.configure(fg=base_color),
        )

    def _update_preview(self, *_args: object) -> None:
        expression = self.expression_var.get().strip()
        if not expression:
            self.preview_var.set("Preview: ")
            return
        try:
            result = safe_eval(expression)
            self.preview_var.set(f"Preview: = {self._format_number(result)}")
        except Exception:
            self.preview_var.set("Preview: ...")

    def _button_press_visual(self, event: tk.Event) -> None:
        event.widget.configure(relief="sunken")

    def _button_release_visual(self, event: tk.Event) -> None:
        event.widget.configure(relief="flat")

    def _on_button(self, value: str) -> None:
        if value in {"MC", "MR", "M+", "M-"}:
            self._handle_memory(value)
            return
        if value == "C":
            self.expression_var.set("")
            self._set_status("Cleared expression.")
            return
        if value == "<-":
            self.expression_var.set(self.expression_var.get()[:-1])
            return
        if value == "+/-":
            current = self.expression_var.get().strip()
            if not current:
                return
            if current.startswith("-"):
                self.expression_var.set(current[1:])
            else:
                self.expression_var.set(f"-{current}")
            return
        if value == "=":
            self._evaluate_current()
            return
        if value in {"sin", "cos", "tan", "sqrt", "log", "ln", "abs"}:
            self.expression_var.set(self.expression_var.get() + f"{value}(")
            return
        if value in {"pi", "e"}:
            self.expression_var.set(self.expression_var.get() + value)
            return

        self.expression_var.set(self.expression_var.get() + value)

    def _resolve_input_value(self) -> float:
        expression = self.expression_var.get().strip()
        if not expression:
            return 0.0
        return safe_eval(expression)

    def _format_number(self, value: float) -> str:
        return f"{value:.10g}"

    def _handle_memory(self, action: str) -> None:
        if action == "MC":
            self.memory_value = 0.0
            self._set_status("Memory cleared.")
            return
        if action == "MR":
            self.expression_var.set(self._format_number(self.memory_value))
            self._set_status("Memory recalled.")
            return

        try:
            value = self._resolve_input_value()
            if action == "M+":
                self.memory_value += value
                self._set_status(
                    f"Added to memory. M = {self._format_number(self.memory_value)}"
                )
            elif action == "M-":
                self.memory_value -= value
                self._set_status(
                    f"Subtracted from memory. M = {self._format_number(self.memory_value)}"
                )
        except Exception:
            self._set_status("Memory update failed: invalid expression.")

    def _evaluate_current(self) -> None:
        expression = self.expression_var.get().strip()
        if not expression:
            self._set_status("Enter an expression first.")
            return

        try:
            result = safe_eval(expression)
            output = self._format_number(result)
            self.expression_var.set(output)
            self.history_list.insert(tk.END, f"{expression} = {output}")
            self.history_list.yview_moveto(1)
            self._set_status("Success. Double-click history to reuse result.")
        except ZeroDivisionError:
            self._set_status("Math error: division by zero.")
        except Exception:
            self._set_status("Invalid expression.")

    def _reuse_history(self, _event: tk.Event) -> None:
        selection = self.history_list.curselection()
        if not selection:
            return
        text = self.history_list.get(selection[0])
        if "=" in text:
            result = text.split("=")[-1].strip()
            self.expression_var.set(result)
            self._set_status("Result copied from history.")

    def _handle_keypress(self, event: tk.Event) -> None:
        char = event.char
        if event.keysym in {"Return", "KP_Enter"}:
            self._evaluate_current()
            return
        if event.keysym in {"BackSpace", "Delete"}:
            self.expression_var.set(self.expression_var.get()[:-1])
            return
        if event.keysym in {"Escape"}:
            self.expression_var.set("")
            self._set_status("Cleared expression.")
            return
        if event.keysym in {"s", "S"} and (event.state & 0x4):
            self.expression_var.set(self.expression_var.get() + "sin(")
            return
        if event.keysym in {"c", "C"} and (event.state & 0x4):
            self.expression_var.set(self.expression_var.get() + "cos(")
            return
        if event.keysym in {"t", "T"} and (event.state & 0x4):
            self.expression_var.set(self.expression_var.get() + "tan(")
            return
        if event.keysym in {"l", "L"} and (event.state & 0x4):
            self.expression_var.set(self.expression_var.get() + "log(")
            return
        if char in "0123456789.+-*/()%^":
            self.expression_var.set(self.expression_var.get() + char)


if __name__ == "__main__":
    app = HelloWorldCalculator()
    app.mainloop()