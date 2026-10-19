
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from debugger import debug_code, ask_follow_up


class DebugMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DebugMate AI - Code Debugging Assistant")
        self.root.geometry("1050x820")
        self.root.minsize(780, 620)

        self.last_answer = ""
        self.last_code = ""
        self.last_language = ""

        self.build_ui()

    def build_ui(self):
        # Main application container
        main = ttk.Frame(self.root, padding=14)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="DebugMate AI",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        ttk.Label(
            main,
            text="Understand your bugs. Learn how to fix them."
        ).pack(anchor="w", pady=(0, 12))

        # Language and explanation settings
        settings = ttk.Frame(main)
        settings.pack(fill="x", pady=5)

        ttk.Label(settings, text="Language:").pack(side="left")

        self.language = tk.StringVar(value="Python")
        ttk.Combobox(
            settings,
            textvariable=self.language,
            values=[
                "Python", "C++", "C#", "Java",
                "JavaScript", "SQL", "Other"
            ],
            state="readonly",
            width=15
        ).pack(side="left", padx=(6, 20))

        ttk.Label(settings, text="Explanation:").pack(side="left")

        self.detail = tk.StringVar(value="Beginner-friendly")
        ttk.Combobox(
            settings,
            textvariable=self.detail,
            values=[
                "Brief", "Beginner-friendly", "Detailed"
            ],
            state="readonly",
            width=20
        ).pack(side="left", padx=6)

        # Source code input
        ttk.Label(
            main, text="Source Code", font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(10, 4))

        self.code_input = tk.Text(
            main,
            height=9,
            wrap="none",
            font=("Consolas", 10),
            undo=True
        )
        self.code_input.pack(fill="x")

        # Optional error message
        ttk.Label(
            main, text="Error Message (optional)",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(10, 4))

        self.error_input = tk.Text(
            main,
            height=3,
            wrap="word",
            font=("Consolas", 10)
        )
        self.error_input.pack(fill="x")

        # Action buttons
        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=10)

        self.debug_button = ttk.Button(
            buttons,
            text="Debug Code",
            command=self.start_debug
        )
        self.debug_button.pack(side="left")

        ttk.Button(
            buttons,
            text="Load Example",
            command=self.load_example
        ).pack(side="left", padx=8)

        ttk.Button(
            buttons,
            text="Clear",
            command=self.clear_inputs
        ).pack(side="left")

        self.status = tk.StringVar(value="Ready")
        ttk.Label(
            buttons, textvariable=self.status
        ).pack(side="right")

        # AI output
        ttk.Label(
            main, text="AI Diagnosis",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(4, 4))

        result_frame = ttk.Frame(main)
        result_frame.pack(fill="both", expand=True)

        self.output = tk.Text(
            result_frame,
            wrap="word",
            font=("Segoe UI", 10),
            state="disabled"
        )
        self.output.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.output.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.output.configure(yscrollcommand=scrollbar.set)

        # Follow-up questions
        ttk.Label(
            main, text="Ask a Follow-up Question",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(10, 4))

        followup_frame = ttk.Frame(main)
        followup_frame.pack(fill="x")

        self.question = tk.StringVar()
        self.question_entry = ttk.Entry(
            followup_frame,
            textvariable=self.question
        )
        self.question_entry.pack(
            side="left", fill="x", expand=True
        )
        self.question_entry.bind(
            "<Return>", lambda event: self.start_follow_up()
        )

        self.followup_button = ttk.Button(
            followup_frame,
            text="Ask AI",
            command=self.start_follow_up
        )
        self.followup_button.pack(side="left", padx=(8, 0))

    def show_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def start_debug(self):
        code = self.code_input.get("1.0", "end-1c").strip()
        error = self.error_input.get("1.0", "end-1c").strip()

        if not code:
            messagebox.showwarning(
                "Missing Code",
                "Please enter the code you want to debug."
            )
            return

        self.last_code = code
        self.last_language = self.language.get()

        self.set_busy(True, "Analyzing code...")
        self.show_output("Please wait while the AI analyzes your code.")

        # API requests must not block the Tkinter event loop.
        threading.Thread(
            target=self.run_debug,
            args=(self.last_language, code, error, self.detail.get()),
            daemon=True
        ).start()

    def run_debug(self, language, code, error, detail):
        try:
            answer = debug_code(language, code, error, detail)
            self.root.after(0, self.debug_success, answer)
        except Exception as exc:
            self.root.after(0, self.show_error, str(exc))

    def debug_success(self, answer):
        self.last_answer = answer
        self.show_output(answer)
        self.set_busy(False, "Analysis complete")

    def start_follow_up(self):
        question = self.question.get().strip()

        if not self.last_answer:
            messagebox.showinfo(
                "No Diagnosis Yet",
                "Debug some code before asking a follow-up."
            )
            return

        if not question:
            messagebox.showwarning(
                "Empty Question",
                "Please enter a follow-up question."
            )
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
            reply = ask_follow_up(language, code, answer, question)
            self.root.after(0, self.follow_up_success, reply)
        except Exception as exc:
            self.root.after(0, self.show_error, str(exc))

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
        self.show_output("Request failed:\n\n" + error)
        self.set_busy(False, "Request failed")

    def set_busy(self, busy, status):
        self.status.set(status)
        state = "disabled" if busy else "normal"
        self.debug_button.configure(state=state)
        self.followup_button.configure(state=state)

    def load_example(self):
        # A predictable bug for the live demonstration.
        example = (
            "numbers = [10, 20, 30]\n"
            "print(numbers[3])\n"
        )

        self.language.set("Python")
        self.code_input.delete("1.0", "end")
        self.code_input.insert("1.0", example)

        self.error_input.delete("1.0", "end")
        self.error_input.insert(
            "1.0",
            "IndexError: list index out of range"
        )

    def clear_inputs(self):
        self.code_input.delete("1.0", "end")
        self.error_input.delete("1.0", "end")
        self.question.set("")
        self.show_output("")
        self.last_answer = ""
        self.last_code = ""
        self.last_language = ""
        self.status.set("Ready")


if __name__ == "__main__":
    root = tk.Tk()
    app = DebugMateApp(root)
    root.mainloop()
