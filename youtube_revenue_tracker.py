import customtkinter as ctk
from tkinter import filedialog, messagebox
import csv
import os

ctk.set_appearance_mode("dark")      # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue, dark-blue, green


def calculate_revenue(views, rate_per_view):
    return views * rate_per_view


def read_csv(file_path):
    videos = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row['title']
                views = int(row['views'])
                videos.append((title, views))
    except Exception as e:
        messagebox.showerror("CSV Error", f"Failed to read CSV file:\n{e}")
    return videos


def write_csv(videos, rate, output_path):
    try:
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'views', 'revenue'])
            for title, views in videos:
                revenue = calculate_revenue(views, rate)
                writer.writerow([title, views, f"{revenue:.2f}"])
        messagebox.showinfo("Success", f"Saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Write Error", f"Failed to write CSV file:\n{e}")


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    entry_file.delete(0, len(entry_file.get()))
    entry_file.insert(0, file_path)


def run_tracker():
    file_path = entry_file.get()
    try:
        rate = float(entry_rate.get())
    except ValueError:
        messagebox.showerror("Input Error", "Enter a valid revenue rate.")
        return

    if not os.path.isfile(file_path):
        messagebox.showerror("File Error", "Select a valid CSV file.")
        return

    videos = read_csv(file_path)
    if not videos:
        return

    output_text.configure(state="normal")
    output_text.delete("0.0", "end")
    total = 0
    for title, views in videos:
        revenue = calculate_revenue(views, rate)
        output_text.insert("end", f"{title}: {views} views → ${revenue:.2f}\n")
        total += revenue
    output_text.insert("end", f"\nTotal Revenue: ${total:.2f}")
    output_text.configure(state="disabled")

    # Save output
    save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[
                                                 ("CSV Files", "*.csv")],
                                             initialfile="video_revenue_report.csv")
    if save_path:
        write_csv(videos, rate, save_path)

# ------------------------ GUI ------------------------


app = ctk.CTk()
app.title("🎧 YouTube Revenue Tracker")
app.geometry("600x600")

# File selection
ctk.CTkLabel(app, text="📂 Video CSV File:", font=(
    "Helvetica Neue", 14)).pack(pady=(20, 5))
entry_file = ctk.CTkEntry(app, width=400)
entry_file.pack(pady=5)
ctk.CTkButton(app, text="Browse", command=browse_file).pack(pady=5)

# Revenue rate input
ctk.CTkLabel(app, text="💸 Revenue per View (e.g., 0.05):",
             font=("Helvetica Neue", 14)).pack(pady=(20, 5))
entry_rate = ctk.CTkEntry(app, width=200)
entry_rate.pack(pady=5)

# Run button
ctk.CTkButton(app, text="🚀 Calculate & Save Report", command=run_tracker,
              fg_color="#1DB954", hover_color="#1ED760").pack(pady=20)

# Output text box
output_text = ctk.CTkTextbox(app, width=520, height=250)
output_text.pack(pady=(10, 20))
output_text.configure(state="disabled")

app.mainloop()
