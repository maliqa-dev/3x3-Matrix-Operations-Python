import sys
import time
import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. MATRIX ENGINE (WITHOUT NUMPY - PURE PYTHON)
# ==========================================
class PurePythonMatrixEngine:
    @staticmethod
    def add(A, B):
        res = [[A[r][c] + B[r][c] for c in range(3)] for r in range(3)]
        return res, "Logic: Nested loops iterating 3x3 indices -> C[r][c] = A[r][c] + B[r][c]"

    @staticmethod
    def subtract(A, B):
        res = [[A[r][c] - B[r][c] for c in range(3)] for r in range(3)]
        return res, "Logic: Nested loops iterating 3x3 indices -> C[r][c] = A[r][c] - B[r][c]"

    @staticmethod
    def multiply(A, B):
        res = [[0.0 for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    res[i][j] += A[i][k] * B[k][j]
        return res, "Logic: Triple nested loops (O(n^3)) -> C[i][j] += A[i][k] * B[k][j]"

    @staticmethod
    def elem_multiply(A, B):
        res = [[A[r][c] * B[r][c] for c in range(3)] for r in range(3)]
        return res, "Logic: Element-by-element loop -> C[r][c] = A[r][c] * B[r][c]"

    @staticmethod
    def transpose(M, name="A"):
        res = [[M[c][r] for c in range(3)] for r in range(3)]
        return res, f"Logic: Index swap -> {name}^T[r][c] = {name}[c][r]"

    @staticmethod
    def determinant(M, name="A"):
        det = (
            M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
        )
        return round(det, 4), f"Logic: Rule of Sarrus / Cofactor expansion across Row 1 for |{name}|"

    @staticmethod
    def inverse(M, name="A"):
        det, _ = PurePythonMatrixEngine.determinant(M, name)
        if abs(det) < 1e-9:
            raise ValueError(f"Matrix {name} is Singular (Determinant = 0). Inverse does not exist!")

        # Cofactor Matrix
        cof = [[0.0]*3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                minor = [
                    [M[i][j] for j in range(3) if j != c]
                    for i in range(3) if i != r
                ]
                minor_det = minor[0][0]*minor[1][1] - minor[0][1]*minor[1][0]
                sign = 1 if (r + c) % 2 == 0 else -1
                cof[r][c] = sign * minor_det

        # Adjugate (Transpose of Cofactor) divided by Determinant
        adj, _ = PurePythonMatrixEngine.transpose(cof, "Cof")
        inv = [[round(adj[r][c] / det, 4) for c in range(3)] for r in range(3)]
        return inv, f"Logic: Manual 2x2 Minors -> Cofactor -> Adjugate / |{name}|"


# ==========================================
# 2. COMMAND LINE INTERFACE (CLI) MODE
# ==========================================
def run_cli():
    print("\n" + "="*54)
    print("   MATRIX STUDIO PRO 3x3 — PURE PYTHON CLI EDITION")
    print("="*54)

    def input_matrix(label):
        print(f"\nEnter 3x3 Matrix {label} (3 numbers separated by spaces per row):")
        rows = []
        for r in range(3):
            while True:
                try:
                    vals = [float(x) for x in input(f"  Row {r+1}: ").strip().split()]
                    if len(vals) != 3:
                        print("  [!] Please enter exactly 3 numbers.")
                        continue
                    rows.append(vals)
                    break
                except ValueError:
                    print("  [!] Invalid input. Enter numbers only.")
        return rows

    A = input_matrix("A")
    B = input_matrix("B")

    while True:
        print("\n--- SELECT OPERATION (PURE PYTHON - NO NUMPY) ---")
        print("1. Addition (A + B)          6. Transpose B (B^T)")
        print("2. Subtraction (A - B)       7. Determinant A |A|")
        print("3. Matrix Multiply (A x B)   8. Determinant B |B|")
        print("4. Element-wise (A * B)      9. Inverse A (A^-1)")
        print("5. Transpose A (A^T)        10. Inverse B (B^-1)")
        print("11. Re-enter Matrices        0. Exit")
        choice = input("Enter choice (0-11): ").strip()

        if choice == "0":
            print("Exiting Pure Python CLI. Goodbye!")
            break
        elif choice == "11":
            A = input_matrix("A")
            B = input_matrix("B")
            continue

        try:
            start = time.perf_counter()
            if choice == "1": res, note = PurePythonMatrixEngine.add(A, B)
            elif choice == "2": res, note = PurePythonMatrixEngine.subtract(A, B)
            elif choice == "3": res, note = PurePythonMatrixEngine.multiply(A, B)
            elif choice == "4": res, note = PurePythonMatrixEngine.elem_multiply(A, B)
            elif choice == "5": res, note = PurePythonMatrixEngine.transpose(A, "A")
            elif choice == "6": res, note = PurePythonMatrixEngine.transpose(B, "B")
            elif choice == "7": res, note = PurePythonMatrixEngine.determinant(A, "A")
            elif choice == "8": res, note = PurePythonMatrixEngine.determinant(B, "B")
            elif choice == "9": res, note = PurePythonMatrixEngine.inverse(A, "A")
            elif choice == "10": res, note = PurePythonMatrixEngine.inverse(B, "B")
            else:
                print("[!] Invalid choice.")
                continue
            elapsed = (time.perf_counter() - start) * 1_000_000
            print(f"\n[Logic]: {note}")
            print(f"[Time ]: {elapsed:.2f} microseconds")
            print("[Result]:")
            if isinstance(res, list):
                for row in res:
                    print("  ", [round(x, 3) for x in row])
            else:
                print("  ", res)
        except Exception as e:
            print(f"\n[Error]: {e}")


# ==========================================
# 3. MODERN CYBER-GLASS GUI MODE
# ==========================================
class MatrixStudioPureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MatrixStudio Pro 3x3 — Pure Python (No NumPy) Edition")
        self.root.geometry("940x680")
        self.root.configure(bg="#0F0E17")
        self.root.resizable(False, False)

        self.BG = "#0F0E17"
        self.CARD = "#1A1829"
        self.ACCENT = "#F59E0B"     # Amber Gold Glow
        self.ACCENT_2 = "#EC4899"   # Rose Pink Glow
        self.TEXT = "#FFFFFE"
        self.ENTRY_BG = "#252338"

        self.build_ui()
        self.load_sample()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#161424", height=65)
        header.pack(fill="x")
        tk.Label(header, text="MATRIX STUDIO PRO", font=("Segoe UI", 18, "bold"),
                 bg="#161424", fg=self.ACCENT).pack(side="left", padx=25, pady=15)
        tk.Label(header, text="3x3 MATRIX ENGINE  |  WITHOUT NUMPY (PURE PYTHON)",
                 font=("Segoe UI", 10, "bold"), bg="#161424", fg="#F472B6").pack(side="right", padx=25)

        top_frame = tk.Frame(self.root, bg=self.BG)
        top_frame.pack(pady=15, padx=25, fill="x")

        self.entries_a = self.create_matrix_card(top_frame, "MATRIX A (3x3)", "#F59E0B", "left")
        self.entries_b = self.create_matrix_card(top_frame, "MATRIX B (3x3)", "#EC4899", "right")

        util_frame = tk.Frame(self.root, bg=self.BG)
        util_frame.pack(pady=5)
        utils = [
            ("Load Sample Data", self.load_sample, "#D97706"),
            ("Swap A <-> B", self.swap_matrices, "#DB2777"),
            ("Identity A", self.set_identity_a, "#059669"),
            ("Clear All", self.clear_all, "#DC2626"),
        ]
        for text, cmd, color in utils:
            tk.Button(util_frame, text=text, command=cmd, bg=color, fg="white",
                      font=("Segoe UI", 9, "bold"), relief="flat", padx=14, pady=6,
                      cursor="hand2").pack(side="left", padx=8)

        op_frame = tk.LabelFrame(self.root, text=" MATRIX OPERATIONS (PURE LOOPS) ", bg=self.CARD,
                                 fg=self.ACCENT, font=("Segoe UI", 10, "bold"), bd=1, relief="groove")
        op_frame.pack(padx=25, pady=12, fill="x")

        ops = [
            ("Addition (A + B)", lambda: self.execute("Addition (A + B)", PurePythonMatrixEngine.add, True)),
            ("Subtraction (A - B)", lambda: self.execute("Subtraction (A - B)", PurePythonMatrixEngine.subtract, True)),
            ("Matrix Multiply (A x B)", lambda: self.execute("Matrix Multiplication (A x B)", PurePythonMatrixEngine.multiply, True)),
            ("Element-wise (A * B)", lambda: self.execute("Element-wise Multiplication", PurePythonMatrixEngine.elem_multiply, True)),
            ("Transpose A (A^T)", lambda: self.execute("Transpose of Matrix A", lambda a: PurePythonMatrixEngine.transpose(a, "A"), False, "A")),
            ("Transpose B (B^T)", lambda: self.execute("Transpose of Matrix B", lambda b: PurePythonMatrixEngine.transpose(b, "B"), False, "B")),
            ("Determinant |A|", lambda: self.execute("Determinant of Matrix A", lambda a: PurePythonMatrixEngine.determinant(a, "A"), False, "A")),
            ("Determinant |B|", lambda: self.execute("Determinant of Matrix B", lambda b: PurePythonMatrixEngine.determinant(b, "B"), False, "B")),
            ("Inverse A (A^-1)", lambda: self.execute("Inverse of Matrix A", lambda a: PurePythonMatrixEngine.inverse(a, "A"), False, "A")),
            ("Inverse B (B^-1)", lambda: self.execute("Inverse of Matrix B", lambda b: PurePythonMatrixEngine.inverse(b, "B"), False, "B")),
        ]

        for idx, (label, command) in enumerate(ops):
            r, c = divmod(idx, 5)
            btn = tk.Button(op_frame, text=label, command=command, bg="#252338", fg=self.TEXT,
                            activebackground=self.ACCENT, activeforeground="#0F0E17",
                            font=("Segoe UI", 9, "bold"), relief="flat", width=20, pady=8, cursor="hand2")
            btn.grid(row=r, column=c, padx=7, pady=7)

        out_frame = tk.LabelFrame(self.root, text=" LIVE EXECUTION & RESULT CONSOLE ", bg=self.CARD,
                                  fg="#F472B6", font=("Segoe UI", 10, "bold"), bd=1, relief="groove")
        out_frame.pack(padx=25, pady=5, fill="both", expand=True)

        self.meta_label = tk.Label(out_frame, text="Ready | Pure Python 2D List Engine Active.",
                                   bg=self.CARD, fg="#FBBF24", font=("Consolas", 10, "bold"), anchor="w")
        self.meta_label.pack(fill="x", padx=15, pady=(8, 2))

        self.result_box = tk.Text(out_frame, height=7, bg="#09080E", fg="#FFFFFE",
                                  font=("Consolas", 12, "bold"), relief="flat", padx=15, pady=10)
        self.result_box.pack(fill="both", expand=True, padx=15, pady=(2, 12))

    def create_matrix_card(self, parent, title, border_color, side):
        card = tk.LabelFrame(parent, text=f" {title} ", bg=self.CARD, fg=border_color,
                             font=("Segoe UI", 11, "bold"), padx=22, pady=12)
        card.pack(side=side, expand=True, fill="both", padx=10)
        grid = []
        for r in range(3):
            row_entries = []
            for c in range(3):
                e = tk.Entry(card, width=8, font=("Consolas", 13, "bold"), justify="center",
                             bg=self.ENTRY_BG, fg="white", insertbackground="white", relief="flat")
                e.grid(row=r, column=c, padx=8, pady=6, ipady=5)
                row_entries.append(e)
            grid.append(row_entries)
        return grid

    def read_matrix(self, grid, name):
        mat = []
        for r in range(3):
            row = []
            for c in range(3):
                val = grid[r][c].get().strip()
                if val == "":
                    raise ValueError(f"Matrix {name} has empty cell at Row {r+1}, Col {c+1}!")
                row.append(float(val))
            mat.append(row)
        return mat

    def format_output(self, res):
        if isinstance(res, (int, float)):
            return f"Scalar Value = {res}"
        lines = []
        for row in res:
            formatted_row = "   ".join(f"{val:9.3f}" for val in row)
            lines.append(f"[ {formatted_row} ]")
        return "\n".join(lines)

    def execute(self, title, func, needs_both, target="A"):
        try:
            start = time.perf_counter()
            if needs_both:
                A = self.read_matrix(self.entries_a, "A")
                B = self.read_matrix(self.entries_b, "B")
                res, logic = func(A, B)
            else:
                M = self.read_matrix(self.entries_a if target == "A" else self.entries_b, target)
                res, logic = func(M)
            elapsed_us = (time.perf_counter() - start) * 1_000_000

            self.meta_label.config(text=f"Operation: {title}  |  Time: {elapsed_us:.2f} us  |  {logic}")
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, self.format_output(res))
        except Exception as e:
            messagebox.showerror("Input / Math Error", str(e))

    def load_sample(self):
        sample_a = [[2, 4, 1], [3, 1, 5], [1, 2, 3]]
        sample_b = [[1, 0, 2], [2, 3, 1], [4, 1, 2]]
        for r in range(3):
            for c in range(3):
                self.entries_a[r][c].delete(0, tk.END)
                self.entries_a[r][c].insert(0, str(sample_a[r][c]))
                self.entries_b[r][c].delete(0, tk.END)
                self.entries_b[r][c].insert(0, str(sample_b[r][c]))

    def set_identity_a(self):
        for r in range(3):
            for c in range(3):
                self.entries_a[r][c].delete(0, tk.END)
                self.entries_a[r][c].insert(0, "1" if r == c else "0")

    def swap_matrices(self):
        for r in range(3):
            for c in range(3):
                va = self.entries_a[r][c].get()
                vb = self.entries_b[r][c].get()
                self.entries_a[r][c].delete(0, tk.END)
                self.entries_a[r][c].insert(0, vb)
                self.entries_b[r][c].delete(0, tk.END)
                self.entries_b[r][c].insert(0, va)

    def clear_all(self):
        for r in range(3):
            for c in range(3):
                self.entries_a[r][c].delete(0, tk.END)
                self.entries_b[r][c].delete(0, tk.END)
        self.result_box.delete("1.0", tk.END)
        self.meta_label.config(text="Cleared all fields.")


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        root = tk.Tk()
        app = MatrixStudioPureGUI(root)
        root.mainloop()