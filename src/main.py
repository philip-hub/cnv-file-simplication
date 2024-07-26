import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def truncate_to_sig_figs(value, sig_figs):
    """Truncate a value to the specified number of significant figures."""
    if value == 0:
        return 0
    else:
        return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)

def average_rows_by_arm(df, n, progress_callback):
    """Average every n rows within each 'arm' group in the dataframe."""
    result = []
    total_groups = df['arm'].nunique()
    current_group = 0
    
    for arm, group in df.groupby('arm'):
        group = group.reset_index(drop=True)
        numeric_cols = group.select_dtypes(include=[np.number]).columns
        non_numeric_cols = group.select_dtypes(exclude=[np.number]).columns

        for i in range(0, len(group), n):
            chunk = group.iloc[i:i+n]
            if len(chunk) == 0:
                continue

            avg_chunk = chunk[numeric_cols].mean().to_frame().T
            avg_chunk[non_numeric_cols] = chunk.iloc[0][non_numeric_cols].values
            avg_chunk['Pos'] = chunk.iloc[-1]['Pos']

            result.append(avg_chunk)
        
        current_group += 1
        progress_callback(current_group / total_groups * 100)
    
    return pd.concat(result, ignore_index=True)

def process_tsv(file_path, keep_every_20th, average_every_20th, progress_callback):
    df = pd.read_csv(file_path, sep='\t' if file_path.endswith('.tsv') else '\s+')
    df = df[['arm', 'Pos', 'v', 'lcv']]

    if average_every_20th:
        df = average_rows_by_arm(df, 20, progress_callback)
    elif keep_every_20th:
        df = df.iloc[::20, :]

    df['v'] = df['v'].apply(lambda x: truncate_to_sig_figs(x, 4))
    df['lcv'] = df['lcv'].apply(lambda x: truncate_to_sig_figs(x, 4))
    
    progress_callback(100)
    return df

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("TSV and DAT files", "*.tsv *.dat"), ("All files", "*.*")])
    if file_path:
        input_path.set(file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".tsv", filetypes=[("TSV files", "*.tsv"), ("All files", "*.*")])
    if file_path:
        return file_path
    return None

def run_processing():
    input_file = input_path.get()
    keep_every_20th = keep_20th_var.get()
    average_every_20th = average_20th_var.get()

    if keep_every_20th and average_every_20th:
        messagebox.showerror("Error", "Both 'Keep every 20th row' and 'Average every 20th row' cannot be selected.")
        return

    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return

    output_file = save_file()
    if output_file:
        progress_bar['value'] = 0
        root.update_idletasks()
        
        def progress_callback(progress):
            progress_bar['value'] = progress
            root.update_idletasks()
        
        processed_df = process_tsv(input_file, keep_every_20th, average_every_20th, progress_callback)
        processed_df.to_csv(output_file, sep='\t', index=False)
        messagebox.showinfo("Success", f"Processing complete. Processed file saved as '{output_file}'.")

# Create the main window
root = tk.Tk()
root.title("CNV File Simplification")

# Input file selection
tk.Label(root, text="Input TSV/DAT File:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
input_path = tk.StringVar()
tk.Entry(root, textvariable=input_path, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=5)

# Options
keep_20th_var = tk.BooleanVar()
average_20th_var = tk.BooleanVar()

tk.Checkbutton(root, text="Keep every 20th row", variable=keep_20th_var).grid(row=1, column=0, columnspan=3, padx=10, pady=5)
tk.Checkbutton(root, text="Average every 20th row", variable=average_20th_var).grid(row=2, column=0, columnspan=3, padx=10, pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Run button
tk.Button(root, text="Run", command=run_processing).grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
