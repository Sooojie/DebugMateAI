
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from debugger import debug_code, ask_follow_up


# ---------- Theme ----------
BG = "#111111"
PANEL = "#161616"
BORDER = "#555555"
FG = "#FFFFFF"
MUTED = "#B8B8B8"
ACCENT = "#2D7DDB"
BUTTON_HOVER = "#3C8DE8"


class DebugMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DebugMate AI")
        self.root.geometry("1100x760")
        self.root.minsize(800, 580)
        self.root.configure(bg=BG)

        self.last_answer = ""
        self.last_code = ""
        self.last_language = ""
        self.busy = False

        self.configure_styles()
        self.build_ui()

    def configure_styles(self):
        style = ttk.Style()

        # Use a theme that allows us to customize comboboxes.
        style.theme_use("clam")

        style.configure(
            "DebugMate.TCombobox",
            fieldbackground=PANEL,
            background=PANEL,
            foreground=FG,
            arrowcolor=FG,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=5
        )

        style.map(
            "DebugMate.TCombobox",
            fieldbackground=[("readonly", PANEL)],
            foreground=[("readonly", FG)],
            selectbackground=[("readonly", PANEL)],
            selectforeground=[("readonly", FG)]
        )

    def build_ui(self):
        # Main grid:
        # Row 0 = title
        # Row 1 = column headings
        # Row 2 = editors and AI output
        # Row 3 = action buttons

        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # ---------- Title ----------
        header = tk.Frame(
            self.root,
            bg=BG,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        header.grid(
            row=0, column=0, columnspan=2,
            sticky="nsew", padx=8, pady=(8, 0)
        )

        tk.Label(
            header,
            text="DEBUGMATE AI",
            font=("Segoe UI", 16, "bold"),
            bg=BG,
            fg=FG,
            pady=15
        ).pack(fill="x")

        # ---------- Column headings ----------
        left_heading = self.make_panel(self.root)
        left_heading.grid(
            row=1, column=0, sticky="nsew",
            padx=(8, 0), pady=0
        )

        right_heading = self.make_panel(self.root)
        right_heading.grid(
            row=1, column=1, sticky="nsew",
            padx=(0, 8), pady=0
        )

        tk.Label(
            left_heading,
            text="LANGUAGE",
            bg=PANEL, fg=FG,
            font=("Segoe UI", 10, "bold"),
            pady=8
        ).pack(fill="x")

        self.language = tk.StringVar(value="Python")

        self.language_box = ttk.Combobox(
            left_heading,
            textvariable=self.language,
            values=[
                "Python", "C++", "C#", "Java",
                "JavaScript", "SQL", "Other"
            ],
            state="readonly",
            style="DebugMate.TCombobox"
        )
        self.language_box.pack(
            fill="x", padx=10, pady=(0, 8)
        )

        tk.Label(
            right_heading,
            text="EXPLANATION",
            bg=PANEL, fg=FG,
            font=("Segoe UI", 10, "bold"),
            pady=8
        ).pack(fill="x")

        self.detail = tk.StringVar(
            value="Beginner-friendly"
        )

        self.detail_box = ttk.Combobox(
            right_heading,
            textvariable=self.detail,
            values=[
                "Brief", "Beginner-friendly", "Detailed"
            ],
            state="readonly",
            style="DebugMate.TCombobox"
        )
        self.detail_box.pack(
            fill="x", padx=10, pady=(0, 8)
        )

        # ---------- Left column: source code and error ----------
        left_column = tk.Frame(
            self.root,
            bg=BG,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        left_column.grid(
            row=2, column=0, sticky="nsew",
            padx=(8, 0), pady=0
        )

        left_column.grid_rowconfigure(1, weight=3)
        left_column.grid_rowconfigure(3, weight=1)
        left_column.grid_columnconfigure(0, weight=1)

        tk.Label(
            left_column,
            text="SOURCE CODE",
            bg=BG, fg=FG,
            font=("Segoe UI", 10, "bold"),
            pady=8
        ).grid(row=0, column=0, sticky="ew")

        code_frame = tk.Frame(left_column, bg=BG)
        code_frame.grid(
            row=1, column=0, sticky="nsew",
            padx=8, pady=(0, 8)
        )
        code_frame.grid_rowconfigure(0, weight=1)
        code_frame.grid_columnconfigure(0, weight=1)

        self.code_input = tk.Text(
            code_frame,
            bg=PANEL,
            fg=FG,
            insertbackground=FG,
            selectbackground=ACCENT,
            font=("Consolas", 11),
            wrap="none",
            undo=True,
            relief="flat",
            padx=8,
            pady=8
        )
        self.code_input.grid(
            row=0, column=0, sticky="nsew"
        )

        code_scroll = ttk.Scrollbar(
            code_frame,
            orient="vertical",
            command=self.code_input.yview
        )
        code_scroll.grid(row=0, column=1, sticky="ns")
        self.code_input.configure(
            yscrollcommand=code_scroll.set
        )

        tk.Label(
            left_column,
            text="ERROR MESSAGE",
            bg=BG, fg=FG,
            font=("Segoe UI", 10, "bold"),
            pady=8
        ).grid(row=2, column=0, sticky="ew")

        self.error_input = tk.Text(
            left_column,
            height=5,
            bg=PANEL,
            fg=FG,
            insertbackground=FG,
            selectbackground=ACCENT,
            font=("Consolas", 10),
            wrap="word",
            relief="flat",
            padx=8,
            pady=8
        )
        self.error_input.grid(
            row=3, column=0, sticky="nsew",
            padx=8, pady=(0, 8)
        )

        # ---------- Right column: AI output ----------
        right_column = tk.Frame(
            self.root,
            bg=BG,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        right_column.grid(
            row=2, column=1, sticky="nsew",
            padx=(0, 8), pady=0
        )

        right_column.grid_rowconfigure(1, weight=1)
        right_column.grid_columnconfigure(0, weight=1)

        tk.Label(
            right_column,
            text="AI DIAGNOSIS",
            bg=BG, fg=FG,
            font=("Segoe UI", 10, "bold"),
            pady=8
        ).grid(row=0, column=0, sticky="ew")

        output_frame = tk.Frame(right_column, bg=BG)
        output_frame.grid(
            row=1, column=0, sticky="nsew",
            padx=8, pady=(0, 8)
        )
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        self.output = tk.Text(
            output_frame,
            bg=PANEL,
            fg=FG,
            insertbackground=FG,
            selectbackground=ACCENT,
            font=("Segoe UI", 10),
            wrap="word",
            relief="flat",
            padx=10,
            pady=10,
            state="disabled"
        )
        self.output.grid(
            row=0, column=0, sticky="nsew"
        )

        output_scroll = ttk.Scrollbar(
            output_frame,
            orient="vertical",
            command=self.output.yview
        )
        output_scroll.grid(row=0, column=1, sticky="ns")
        self.output.configure(
            yscrollcommand=output_scroll.set
        )

        # Follow-up question area, inside the AI column.
        followup = tk.Frame(right_column, bg=BG)
        followup.grid(
            row=2, column=0, sticky="ew",
            padx=8, pady=(0, 8)
        )
        followup.grid_columnconfigure(0, weight=1)

        self.question = tk.StringVar()

        self.question_entry = tk.Entry(
            followup,
            textvariable=self.question,
            bg=PANEL,
            fg=FG,
            insertbackground=FG,
            relief="flat",
            font=("Segoe UI", 10)
        )
        self.question_entry.grid(
            row=0, column=0, sticky="ew",
            ipady=7, padx=(0, 6)
        )
        self.question_entry.bind(
            "<Return>",
            lambda event: self.start_follow_up()
        )

        self.followup_button = tk.Button(
            followup,
            text="Ask AI",
            command=self.start_follow_up,
            bg=ACCENT,
            fg=FG,
            activebackground=BUTTON_HOVER,
            activeforeground=FG,
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2"
        )
        self.followup_button.grid(row=0, column=1)

        # ---------- Bottom buttons ----------
        footer = tk.Frame(self.root, bg=BG)
        footer.grid(
            row=3, column=0, columnspan=2,
            sticky="ew", padx=8, pady=(0, 8)
        )

        for column in range(3):
            footer.grid_columnconfigure(column, weight=1)

        self.debug_button = self.make_button(
            footer, "Debug Code", self.start_debug
        )
        self.debug_button.grid(
            row=0, column=0, sticky="ew", padx=(0, 2)
        )

        self.example_button = self.make_button(
            footer, "Load Example", self.load_example
        )
        self.example_button.grid(
            row=0, column=1, sticky="ew", padx=2
        )

        self.clear_button = self.make_button(
            footer, "Clear", self.clear_inputs
        )
        self.clear_button.grid(
            row=0, column=2, sticky="ew", padx=(2, 0)
        )

        # Status line
        self.status = tk.StringVar(value="Ready")

        tk.Label(
            self.root,
            textvariable=self.status,
            bg=BG,
            fg=MUTED,
            anchor="w",
            font=("Segoe UI", 9)
        ).grid(
            row=4, column=0, columnspan=2,
            sticky="ew", padx=10, pady=(0, 5)
        )

    # ---------- UI helpers ----------

    def make_panel(self, parent):
        return tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def make_button(self, parent, label, command):
        return tk.Button(
            parent,
            text=label,
            command=command,
            bg=PANEL,
            fg=FG,
            activebackground=ACCENT,
            activeforeground=FG,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=8,
            pady=10,
            cursor="hand2"
        )

    def show_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def set_busy(self, busy, status):
        self.busy = busy
        self.status.set(status)

        state = "disabled" if busy else "normal"

        self.debug_button.configure(state=state)
        self.example_button.configure(state=state)
        self.clear_button.configure(state=state)
        self.followup_button.configure(state=state)

    # ---------- Debugging ----------

    def start_debug(self):
        if self.busy:
            return

        code = self.code_input.get(
            "1.0", "end-1c"
        ).strip()

        error = self.error_input.get(
            "1.0", "end-1c"
        ).strip()

        if not code:
            messagebox.showwarning(
                "Missing Code",
                "Please enter the code you want to debug."
            )
            return

        language = self.language.get()
        detail = self.detail.get()

        self.last_code = code
        self.last_language = language
        self.last_answer = ""

        self.set_busy(True, "Analyzing code...")
        self.show_output(
            "Please wait while DebugMate analyzes your code..."
        )

        threading.Thread(
            target=self.run_debug,
            args=(language, code, error, detail),
            daemon=True
        ).start()

    def run_debug(self, language, code, error, detail):
        try:
            answer = debug_code(
                language, code, error, detail
            )
            self.root.after(
                0, lambda: self.debug_success(answer)
            )
        except Exception as exc:
            self.root.after(
                0, lambda message=str(exc):
                self.show_error(message)
            )

    def debug_success(self, answer):
        self.last_answer = answer
        self.show_output(answer)
        self.set_busy(False, "Analysis complete")

    # ---------- Follow-up questions ----------

    def start_follow_up(self):
        if self.busy:
            return

        if not self.last_answer:
            messagebox.showinfo(
                "No Diagnosis Yet",
                "Debug some code before asking a follow-up."
            )
            return

        question = self.question.get().strip()

        if not question:
            return

        self.question.set("")
        self.set_busy(True, "Answering question...")

        threading.Thread(
            target=self.run_follow_up,
            args=(
                self.last_language,
                self.last_code,
                self.last_answer,
                question
            ),
            daemon=True
        ).start()

    def run_follow_up(self, language, code, answer, question):
        try:
            reply = ask_follow_up(
                language, code, answer, question
            )
            self.root.after(
                0, lambda: self.follow_up_success(reply)
            )
        except Exception as exc:
            self.root.after(
                0, lambda message=str(exc):
                self.show_error(message)
            )

    def follow_up_success(self, reply):
        combined = (
            self.last_answer
            + "\n\n--- Follow-up Answer ---\n\n"
            + reply
        )
        self.last_answer = combined
        self.show_output(combined)
        self.set_busy(False, "Answer complete")

    def show_error(self, error):
        self.show_output(
            "Request failed:\n\n" + error
        )
        self.set_busy(False, "Request failed")

    # ---------- Example and reset ----------

    def load_example(self):
        if self.busy:
            return

        self.language.set("Python")

        self.code_input.delete("1.0", "end")
        self.code_input.insert(
            "1.0",
            "numbers = [10, 20, 30]\n"
            "print(numbers[3])\n"
        )

        self.error_input.delete("1.0", "end")
        self.error_input.insert(
            "1.0",
            "IndexError: list index out of range"
        )

        self.status.set("Example loaded")

    def clear_inputs(self):
        if self.busy:
            return

        self.code_input.delete("1.0", "end")
        self.error_input.delete("1.0", "end")
        self.question.set("")

        self.last_answer = ""
        self.last_code = ""
        self.last_language = ""

        self.show_output("")
        self.status.set("Ready")


if __name__ == "__main__":
    root = tk.Tk()
    app = DebugMateApp(root)
    root.mainloop()
