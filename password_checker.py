import tkinter as tk
from tkinter import ttk
import re


class PasswordStrengthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = ttk.Label(
            main_frame,
            text="Password Strength Checker(Akhil's)",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Password entry
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(password_frame, text="Enter Password:").pack(side=tk.LEFT)

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="*",
            width=30
        )
        self.password_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.password_entry.bind("<KeyRelease>", self.on_password_change)

        # Show password checkbox
        self.show_password_var = tk.IntVar()
        show_password_check = ttk.Checkbutton(
            main_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility
        )
        show_password_check.pack(pady=(0, 20))

        # Strength meter
        strength_frame = ttk.Frame(main_frame)
        strength_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(strength_frame, text="Strength:").pack(side=tk.LEFT)

        self.strength_meter = ttk.Progressbar(
            strength_frame,
            orient=tk.HORIZONTAL,
            length=200,
            mode='determinate'
        )
        self.strength_meter.pack(side=tk.LEFT, padx=(10, 0))

        self.strength_label = ttk.Label(strength_frame, text="", width=15)
        self.strength_label.pack(side=tk.LEFT, padx=(10, 0))

        # Feedback text
        self.feedback_text = tk.Text(
            main_frame,
            height=8,
            width=45,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Arial", 9)
        )
        self.feedback_text.pack()

        # Check button
        check_button = ttk.Button(
            main_frame,
            text="Check Password",
            command=self.evaluate_password
        )
        check_button.pack(pady=(10, 0))

    def toggle_password_visibility(self):
        if self.show_password_var.get() == 1:
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def on_password_change(self, event=None):
        self.evaluate_password()

    def evaluate_password(self):
        password = self.password_var.get()
        score = 0
        feedback = []

        # Length check
        length = len(password)
        if length == 0:
            self.update_display(0, "Enter a password")
            return
        elif length < 8:
            score += length * 2
            feedback.append("❌ Too short (min 8 chars)")
        elif length < 12:
            score += length * 3
            feedback.append("⚠️ Decent length (12+ recommended)")
        else:
            score += length * 4
            feedback.append("✅ Excellent length")

        # Character diversity
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

        if has_upper:
            score += 10
            feedback.append("✅ Uppercase letters")
        else:
            feedback.append("❌ Missing uppercase letters")

        if has_lower:
            score += 10
            feedback.append("✅ Lowercase letters")
        else:
            feedback.append("❌ Missing lowercase letters")

        if has_digit:
            score += 10
            feedback.append("✅ Numbers")
        else:
            feedback.append("❌ Missing numbers")

        if has_special:
            score += 15
            feedback.append("✅ Special characters")
        else:
            feedback.append("❌ Missing special characters")

        # Common pattern checks
        if re.search(r'(.)\1{2,}', password):
            score -= 15
            feedback.append("⚠️ Repeated characters")

        if password.lower() in ['password', '123456', 'qwerty', 'letmein']:
            score = 10
            feedback.append("⚠️ Very common password")

        # Ensure score is between 0 and 100
        score = max(0, min(100, score))

        self.update_display(score, feedback)

    def update_display(self, score, feedback):
        # Update progress bar
        self.strength_meter['value'] = score

        # Set strength label and color
        if score == 0:
            strength_text = ""
            color = "black"
        elif score < 40:
            strength_text = "Weak"
            color = "red"
        elif score < 70:
            strength_text = "Moderate"
            color = "orange"
        elif score < 90:
            strength_text = "Strong"
            color = "blue"
        else:
            strength_text = "Very Strong"
            color = "green"

        self.strength_label.config(text=strength_text, foreground=color)

        # Update feedback text
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)

        if isinstance(feedback, list):
            for item in feedback:
                self.feedback_text.insert(tk.END, f"{item}\n")
        else:
            self.feedback_text.insert(tk.END, feedback)

        self.feedback_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()
