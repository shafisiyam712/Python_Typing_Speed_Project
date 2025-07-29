import tkinter as tk
from tkinter import messagebox
import random
import time
import csv
import os

# Paragraphs
paragraphs = [
    "Technology has revolutionized the way we live, work, and communicate. It continues to evolve rapidly, impacting nearly every aspect of our lives.",
    "The Earth revolves around the Sun in an elliptical orbit, taking approximately 365.25 days to complete a full rotation. This motion defines our calendar year.",
    "A healthy lifestyle involves a balanced diet, regular exercise, adequate sleep, and mental well-being. It significantly reduces the risk of chronic diseases.",
    "The internet has become a global platform for information sharing, social interaction, entertainment, and e-commerce. It has transformed modern society.",
    "Space exploration has led to incredible discoveries about the universe, from black holes to the possibility of life on other planets.",
    "Climate change is one of the most pressing issues of our time, caused by rising greenhouse gas emissions and deforestation.",
    "Artificial intelligence is reshaping industries by automating tasks, improving decision-making, and enabling smart systems.",
    "Reading books improves vocabulary, enhances imagination, and develops critical thinking. It's a habit that nurtures the mind.",
    "Renewable energy sources like solar, wind, and hydro power are essential for building a sustainable future and reducing carbon footprints.",
    "Education empowers individuals and societies by fostering knowledge, skills, and values essential for personal and collective growth.",
    "Time management is crucial for productivity. Prioritizing tasks and minimizing distractions can lead to greater achievements.",
]

# Globals
start_time = 0
selected_para = ""
countdown = 60
timer_id = None
csv_file = "typing_results.csv"
high_score_file = "high_score.txt"
high_score = 0


def start_test():
    global start_time, selected_para, countdown, high_score, timer_id

    selected_para = random.choice(paragraphs)
    text_display.config(state='normal')
    text_display.delete('1.0', tk.END)
    text_display.insert(tk.END, selected_para)
    text_display.config(state='disabled')

    input_box.delete('1.0', tk.END)
    start_time = time.time()
    countdown = 60
    timer_label.config(text=f"Time left: {countdown}s")
    update_timer()

def update_timer():
    global countdown, timer_id
    if countdown > 0:
        countdown -= 1
        timer_label.config(text=f"Time left: {countdown}s")
        timer_id = root.after(1000, update_timer)
    else:
        end_test()

def end_test():
    global high_score, timer_id

    if timer_id:
        root.after_cancel(timer_id)

    end_time = time.time()
    user_input = input_box.get('1.0', tk.END).strip()

    if not user_input:
        messagebox.showwarning("Empty Input", "You haven't typed anything.")
        return

    time_taken = end_time - start_time
    time_taken = max(time_taken, 1)
    words_typed = len(user_input.split())
    wpm = round((words_typed / time_taken) * 60, 2)

    total_words = selected_para.split()
    typed_words = user_input.split()

    correct = 0
    errors = 0
    highlighted_text = ""

    for i in range(len(total_words)):
        try:
            if total_words[i] == typed_words[i]:
                highlighted_text += total_words[i] + " "
                correct += 1
            else:
                highlighted_text += f"[{typed_words[i]}] "
                errors += 1
        except IndexError:
            highlighted_text += "[_missing_] "
            errors += 1

    accuracy = (correct / len(total_words)) * 100

    # Update high score
    if wpm > high_score:
        high_score = wpm
        with open(high_score_file, "w") as f:
            f.write(str(high_score))

    # Save results to CSV
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([round(time_taken, 2), wpm, round(accuracy, 2), errors])

    # Display results
    input_box.delete('1.0', tk.END)
    input_box.insert(tk.END, highlighted_text)
    result = (
        f"Typing Speed: {wpm} WPM\n"
        f"Accuracy: {round(accuracy, 2)}%\n"
        f"Mistakes: {errors} word(s) incorrect\n"
        f"High Score: {high_score} WPM"
    )
    messagebox.showinfo("Result", result)


def load_high_score():
    global high_score
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as f:
            try:
                high_score = float(f.read())
            except:
                high_score = 0


# GUI setup
root = tk.Tk()
root.title("Typing Speed Test")
root.geometry("850x550")
root.resizable(False, False)

load_high_score()

tk.Label(root, text="Typing Speed Test", font=("Arial", 20, "bold")).pack(pady=10)
tk.Label(root, text="Click 'Start' to begin and type the paragraph exactly as shown below.", wraplength=800).pack()

timer_label = tk.Label(root, text=f"Time left: {countdown}s", font=("Arial", 12, "bold"), fg="red")
timer_label.pack()

text_display = tk.Text(root, height=6, width=100, wrap='word', font=("Arial", 12), state='disabled', bg="#f0f0f0")
text_display.pack(pady=10)

input_box = tk.Text(root, height=6, width=100, wrap='word', font=("Arial", 12))
input_box.pack()

frame = tk.Frame(root)
frame.pack(pady=15)

tk.Button(frame, text="Start", command=start_test, width=12, bg="green", fg="white").pack(side="left", padx=10)
tk.Button(frame, text="Submit", command=end_test, width=12, bg="blue", fg="white").pack(side="left", padx=10)
tk.Button(frame, text="Exit", command=root.quit, width=12, bg="red", fg="white").pack(side="left", padx=10)

root.mainloop()

