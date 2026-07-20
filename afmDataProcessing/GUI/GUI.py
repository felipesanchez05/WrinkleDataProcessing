import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from pathlib import Path
import threading
import queue

import numpy as np

from ProfileFitting import fit_profiles
from WrinkleProcessing import compute_energies as wrinkle_compute_energies, write_results as wrinkle_write_results
from FractureMechanics import compute_energies as fracture_compute_energies, write_results as fracture_write_results
from StatsPrune import prune_outliers, write_pruned_results
from ResultsPlotting import plot_results

WRINKLE_AE_THRESHOLD = 50  # hard cap for physically unreasonable data, matches StatsPrune.py

LENGTH = 10e-6  # standard flake length in meters, matches WrinkleProcessing.py

gui_queue = queue.Queue()


def browse_input_file():
    path = filedialog.askopenfilename(title="Select data file")
    if path:
        input_file_var.set(path)


def browse_output_dir():
    path = filedialog.askdirectory(title="Select output folder")
    if path:
        output_dir_var.set(path)


def log(message):
    gui_queue.put(('log', message))


def report_progress(done, total):
    gui_queue.put(('progress', done, total))


def process_in_background(input_path, output_dir, thickness, pixel_width, strain, run_wrinkle, run_fracture):
    try:
        data = np.loadtxt(input_path)

        log("Fitting wrinkle profiles...")
        profiles = fit_profiles(data, pixel_width, progress_callback=report_progress, log_callback=log)

        if run_wrinkle:
            log("Computing wrinkle adhesion energy...")
            stem = f"{input_path.stem}_wrinkle"
            results = wrinkle_compute_energies(profiles, LENGTH, thickness, strain)
            wrinkle_write_results(results, output_dir, stem, LENGTH, thickness, strain)
            log("Detecting outliers...")
            pruned = prune_outliers(results, WRINKLE_AE_THRESHOLD, log_callback=log)
            write_pruned_results(pruned, output_dir, stem)
            log("Plotting results...")
            plot_results(results, pruned, output_dir, stem)
            log("Wrinkle analysis complete.")

        if run_fracture:
            log("Computing fracture mechanics adhesion energy...")
            stem = f"{input_path.stem}_fracture"
            results = fracture_compute_energies(profiles, thickness)
            fracture_write_results(results, output_dir, stem, thickness)
            log("Detecting outliers...")
            ae_threshold = np.mean([r['Adhesion energy'] for r in results]) * 4
            pruned = prune_outliers(results, ae_threshold, log_callback=log)
            write_pruned_results(pruned, output_dir, stem)
            log("Plotting results...")
            plot_results(results, pruned, output_dir, stem)
            log("Fracture mechanics analysis complete.")

        gui_queue.put(('done', str(output_dir)))
    except Exception as exc:
        gui_queue.put(('error', str(exc)))


def run():
    input_file = input_file_var.get()
    output_dir = output_dir_var.get()

    if not input_file:
        messagebox.showerror("Missing input", "Please select a data file.")
        return
    if not output_dir:
        messagebox.showerror("Missing output", "Please select an output folder.")
        return
    run_wrinkle = wrinkle_var.get()
    run_fracture = fracture_var.get()
    if not run_wrinkle and not run_fracture:
        messagebox.showerror("Missing method", "Please select at least one analysis method.")
        return
    try:
        thickness = float(thickness_var.get()) * 1e-9
        pixel_width = float(pixel_width_var.get()) * 1e-6
    except ValueError:
        messagebox.showerror("Invalid input", "Thickness and pixel width must be numbers.")
        return

    strain = 0.0
    if run_wrinkle:
        try:
            strain = float(strain_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Strain must be a number.")
            return

    run_button['state'] = 'disabled'
    progress['value'] = 0
    log_box.delete('1.0', tk.END)
    log(f"Processing {Path(input_file).name}...")

    thread = threading.Thread(
        target=process_in_background,
        args=(Path(input_file), Path(output_dir), thickness, pixel_width, strain, run_wrinkle, run_fracture),
        daemon=True,
    )
    thread.start()


def poll_queue():
    try:
        while True:
            item = gui_queue.get_nowait()
            kind = item[0]
            if kind == 'log':
                log_box.insert(tk.END, item[1] + "\n")
                log_box.see(tk.END)
            elif kind == 'progress':
                _, done, total = item
                progress['maximum'] = total
                progress['value'] = done
            elif kind == 'done':
                log_box.insert(tk.END, f"Done. Results written to {item[1]}\n")
                log_box.see(tk.END)
                run_button['state'] = 'normal'
            elif kind == 'error':
                log_box.insert(tk.END, f"Error: {item[1]}\n")
                log_box.see(tk.END)
                messagebox.showerror("Processing failed", item[1])
                run_button['state'] = 'normal'
    except queue.Empty:
        pass
    root.after(100, poll_queue)


root = tk.Tk()
root.title("Wrinkle Processing")

input_file_var = tk.StringVar()
output_dir_var = tk.StringVar()
thickness_var = tk.StringVar()
pixel_width_var = tk.StringVar()
strain_var = tk.StringVar(value="0.0101")
wrinkle_var = tk.BooleanVar(value=True)
fracture_var = tk.BooleanVar(value=False)

tk.Label(root, text="Data file:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
tk.Entry(root, textvariable=input_file_var, width=50, state='readonly').grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=browse_input_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Output folder:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
tk.Entry(root, textvariable=output_dir_var, width=50, state='readonly').grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse...", command=browse_output_dir).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Thickness (nm):").grid(row=2, column=0, sticky='e', padx=5, pady=5)
tk.Entry(root, textvariable=thickness_var, width=15).grid(row=2, column=1, sticky='w', padx=5, pady=5)

tk.Label(root, text="Pixel width (microns):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
tk.Entry(root, textvariable=pixel_width_var, width=15).grid(row=3, column=1, sticky='w', padx=5, pady=5)

tk.Label(root, text="Strain (wrinkle only):").grid(row=4, column=0, sticky='e', padx=5, pady=5)
tk.Entry(root, textvariable=strain_var, width=15).grid(row=4, column=1, sticky='w', padx=5, pady=5)

tk.Label(root, text="Analysis method:").grid(row=5, column=0, sticky='e', padx=5, pady=5)
method_frame = tk.Frame(root)
method_frame.grid(row=5, column=1, sticky='w', padx=5, pady=5)
ttk.Checkbutton(method_frame, text="Wrinkle Processing", variable=wrinkle_var).pack(side='left')
ttk.Checkbutton(method_frame, text="Fracture Mechanics", variable=fracture_var).pack(side='left', padx=(10, 0))

run_button = tk.Button(root, text="Run", command=run)
run_button.grid(row=6, column=0, padx=5, pady=10)

progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress.grid(row=6, column=1, columnspan=2, padx=5, pady=10, sticky='we')

log_box = scrolledtext.ScrolledText(root, width=70, height=12)
log_box.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

root.after(100, poll_queue)
root.mainloop()
