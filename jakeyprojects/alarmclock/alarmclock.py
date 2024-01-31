from datetime import datetime
from tkinter import *

current_timestamp = 0
alarm_timestamp = 0

def ttime():
    if display_time.winfo_ismapped():
        display_time.pack_forget()
    elif entry.winfo_ismapped():
        entry.pack_forget() 
        display_time.pack()
    else:
        display_time.pack()
    update()

def update():
    global current_timestamp
    current_time = datetime.today()
    current_timestamp = int(current_time.timestamp())
    formatted_time = current_time.strftime('%A, %B %d, %Y %I:%M:%S %p')
    display_time.config(text=formatted_time)
    display_time.after(1000, update)

def alarm():
    if display_time.winfo_ismapped():
        display_time.pack_forget()
        entry.pack()
    elif entry.winfo_ismapped():
        entered_value = entry.get()
        if entered_value == sample_format or entered_value == '' or entered_value == wrong_format:
            entry.delete(0, END)
            entry.pack_forget()
        elif is_valid_format(entered_value):
            datetime_obj = datetime.strptime(entered_value, '%m/%d/%y %H:%M')
            global alarm_timestamp
            alarm_timestamp = int(datetime.timestamp(datetime_obj))
            print(f'Alarm set at {alarm_timestamp}.')
        else:
            entry.delete(0,END)
            entry.insert(0,wrong_format)
    else:
        entry.pack()
        if entry.get() == '':
            entry.insert(0,sample_format)
    print(f"Now at {current_timestamp}")

def alarm_check():
    global current_timestamp
    global alarm_timestamp
    while True:
        if alarm_timestamp == current_timestamp:
            print("Beep")

def is_valid_format(date_str):
    try:
        datetime_obj = datetime.strptime(date_str, '%m/%d/%y %H:%M')
        return True
    except ValueError:
        return False

root = Tk()
custom_font = ("DS-DIGITAL", 32)
custom_font2 = ("Pixeloid Sans Bold", 15)
display_time = Label(root,font=custom_font,fg="#00FF00",bg="black")
timebtn = Label(root, bg="#563d2d")
timebtn.pack(side=LEFT)
timebtn1 = Label(timebtn, bg="#ffffff")
timebtn1.pack()
left = Button(timebtn1,activebackground="#563d2d",activeforeground="#ffffff",font=custom_font2,fg="#ffffff",bg="#f58607",relief=FLAT,text="TIME", command=ttime)
left.pack()
alarmbtn = Label(root, bg="#563d2d")
alarmbtn.pack(side=RIGHT)
alarmbtn1 = Label(alarmbtn, bg="#ffffff")
alarmbtn1.pack()
right = Button(alarmbtn1,activebackground="#563d2d",activeforeground="#ffffff",font=custom_font2,fg="#ffffff",bg="#f58607",relief=FLAT,text="ALARM",command=alarm)
right.pack()
entry = Entry(root,font=custom_font,fg="#00FF00",bg="black",width=33)
sample_format="Enter here: MM/DD/YY 23:00"
wrong_format="Wrong Format"
entry.insert(0,sample_format)
update()
root.resizable(False, False)
root.mainloop()