import tkinter as tk
import random
import math

# ----------------------- VARIABLES ---------------------------------- #

with open("words.txt") as file:
    words_list = file.read().splitlines()

time_lapsed = 0
wpm = 0


# ----------------------- FUNCTIONS ---------------------------------- #

def radio_used():
    timer_label.config(text=f"Time: {total_time.get()}s")


def countdown(seconds):
    global time_lapsed
    global wpm
    if seconds > 0:
        root.after(1000, countdown, seconds - 1)
        timer_label.config(text=f"Time: {seconds}s")
        time_lapsed = total_time.get() - seconds
        cpm = calc_cpm()
        wpm = math.floor(cpm / 5)
        cpm_label.config(text=f"CPM: {cpm}")
        wpm_label.config(text=f"WPM: {wpm}")
    else:
        # Test has ended
        timer_label.config(text=f"Time: 0s")
        start_button["state"] = "normal"
        for button in radio_options:
            button["state"] = "normal"
        typing_area["state"] = "disabled"
        test_result = tk.Label(text=f"You typed {wpm} words per minute", fg="light blue",
                               font=("Ubuntu", 16, "bold"))
        test_result.grid(row=5, column=0, columnspan=4, pady=20)
        sample_text.config(text=get_new_words())


def start_test():
    typing_area["state"] = "normal"
    typing_area.delete("1.0", tk.END)
    for button in radio_options:
        button["state"] = "disabled"
    start_button["state"] = "disabled"
    countdown(total_time.get())


def calc_cpm():
    chars_typed = len(typing_area.get("1.0", "end-1c"))
    if chars_typed != 0:
        cpm = 60 / time_lapsed * chars_typed
        return math.floor(cpm)
    else:
        return 0


def get_new_words():
    new_words = random.sample(words_list, k=150)
    random.shuffle(new_words)
    return new_words


# ----------------------- GUI SETUP ---------------------------------- #
root = tk.Tk()
root.title("Typing Speed Test")

# Create widgets
title = tk.Label(text="Typing Speed Test", fg="#FFFFFF", font=("Ubuntu", 30, "bold"))
intro_text = tk.Label(text="Choose Time and click Start to begin test.", fg="light blue")
sample_text = tk.Message(text=get_new_words(), fg="light grey", width=600)
typing_area = tk.Text(fg="white", width="70", height="1", borderwidth="2", relief="ridge")
cpm_label = tk.Label(text="CPM: ", fg="#FFFFFF", font=("Ubuntu", 12, "normal"))
wpm_label = tk.Label(text="WPM: ", fg="#FFFFFF", font=("Ubuntu", 12, "normal"))
timer_label = tk.Label(text="Time: 60s", fg="#FFFFFF", font=("Ubuntu", 12, "normal"), anchor=tk.E)
total_time = tk.IntVar()
radio_options = [
    tk.Radiobutton(text="1 Minute", value=60, variable=total_time, command=radio_used),
    tk.Radiobutton(text="3 Minute", value=180, variable=total_time, command=radio_used),
    tk.Radiobutton(text="5 Minute", value=300, variable=total_time, command=radio_used)
]
radio_options[0].invoke()
start_button = tk.Button(text="Start", command=start_test)

# Pack widgets
title.grid(row=0, column=0, columnspan=4, pady=40)
intro_text.grid(row=1, column=0, columnspan=4)
sample_text.grid(row=2, column=0, columnspan=4, pady=30, padx=50)
typing_area.grid(row=3, column=0, columnspan=4)
typing_area["state"] = "disabled"
cpm_label.grid(row=4, column=0, pady=30)
wpm_label.grid(row=4, column=1, pady=30)
timer_label.grid(row=4, column=3, pady=30)

col = 0
for option in radio_options:
    option.grid(row=6, column=col, pady=10)
    col += 1

start_button.grid(row=6, column=3, pady=20, padx=20)

root.mainloop()
