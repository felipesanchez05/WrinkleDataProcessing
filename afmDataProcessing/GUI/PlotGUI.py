import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from pathlib import Path
import json

from ResultsPlotting import plot_results


def browse_results_file():
    path = filedialog.askopenfilename(title="Select results JSON file", filetypes=[("JSON files", "*.json")])
    if not path:
        return
    results_file_var.set(path)

    # auto-fill the pruned counterpart if it exists alongside the results file
    stem = Path(path).stem
    if stem.endswith('_fit_results'):
        stem = stem[: -len('_fit_results')]
    guess = Path(path).parent / f"{stem}_fit_pruned.json"
    if guess.exists():
        pruned_file_var.set(str(guess))


def browse_pruned_file():
    path = filedialog.askopenfilename(title="Select pruned results JSON file (optional)", filetypes=[("JSON files", "*.json")])
    if path:
        pruned_file_var.set(path)


def browse_output_dir():
    path = filedialog.askdirectory(title="Select output folder")
    if path:
        output_dir_var.set(path)


def log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)


def plot():
    results_path = results_file_var.get()
    pruned_path = pruned_file_var.get()
    output_dir = output_dir_var.get()

    if not results_path:
        messagebox.showerror("Missing input", "Please select a results JSON file.")
        return
    if not output_dir:
        messagebox.showerror("Missing output", "Please select an output folder.")
        return

    log_box.delete('1.0', tk.END)
    try:
        with open(results_path) as f:
            all_results = json.load(f)

        if pruned_path:
            with open(pruned_path) as f:
                pruned_results = json.load(f)
        else:
            log("No pruned results file selected; NoOutliers plots will be empty.")
            pruned_results = []

        stem = Path(results_path).stem
        if stem.endswith('_fit_results'):
            stem = stem[: -len('_fit_results')]

        log(f"Plotting {len(all_results)} results ({len(pruned_results)} pruned)...")
        plot_results(all_results, pruned_results, output_dir, stem)
        log(f"Done. Plots written to {Path(output_dir) / stem}")
    except Exception as exc:
        log(f"Error: {exc}")
        messagebox.showerror("Plotting failed", str(exc))


root = tk.Tk()
root.title("Plot Results")

results_file_var = tk.StringVar()
pruned_file_var = tk.StringVar()
output_dir_var = tk.StringVar()

tk.Label(root, text="Results JSON file:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
tk.Entry(root, textvariable=results_file_var, width=50, state='readonly').grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=browse_results_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Pruned JSON file (optional):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
tk.Entry(root, textvariable=pruned_file_var, width=50, state='readonly').grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=browse_pruned_file).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Output folder:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
tk.Entry(root, textvariable=output_dir_var, width=50, state='readonly').grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=browse_output_dir).grid(row=2, column=2, padx=5, pady=5)

plot_button = tk.Button(root, text="Plot", command=plot)
plot_button.grid(row=3, column=0, padx=5, pady=10)

log_box = scrolledtext.ScrolledText(root, width=70, height=12)
log_box.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
