from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
from os.path import exists

BG_COLOR = "#3b474a"
CREATE_FILE_BG_COLOR = "#F1DDBF"
BUTTON_COLOR = "#E2D784"
FONT_COLOR = "#F5F5F5"
FONT = ("Consolas", 13)

# ----------------------------- CREATE DATA FILE -------------------------------- #


def new_file_window():

    def create_file():

        user_file = data_file_entry.get()
        file_path = f"./data/{user_file}.json"
        file_exists = exists(file_path)
        if file_exists:
            messagebox.showinfo("Oops", "File already exists")
        else:
            new_file = open(file_path, "w")
            new_file.close()

    new_window = Tk()
    new_window.title("Create a data file")
    new_window.attributes('-topmost', True)
    new_window.config(width=300, height=200, bg=CREATE_FILE_BG_COLOR, padx=40, pady=60)

    data_file_entry = Entry(new_window)
    data_file_entry.focus_set()
    data_file_entry.grid(column=1, row=0)

    data_file_label = Label(new_window, text="File name: ", bg=CREATE_FILE_BG_COLOR, font=FONT)
    data_file_label.grid(column=0, row=0)

    file_extension_label = Label(new_window, text=".json", bg=CREATE_FILE_BG_COLOR, font=FONT)
    file_extension_label.grid(column=2, row=0)

    create_button = Button(new_window, width=30, text="Create", command=create_file, bg=BUTTON_COLOR)
    create_button.grid(column=0, row=2, columnspan=3, pady=(20, 0))


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for let in range(randint(8, 10))] + \
                    [choice(symbols) for sym in range(randint(2, 4))] + \
                    [choice(numbers) for num in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)

    pyperclip.copy(password)

# ------------------------------ SAVE PASSWORD --------------------------------- #


def save_password():

    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
             "email": email,
             "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except (FileNotFoundError, json.JSONDecodeError):
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()

# ----------------------------- SEARCH PASSWORD -------------------------------- #


def search_password():

    website = website_entry.get().title()
    file = "data.json"
    try:
        with open(file, "r") as data_file:
            data = json.load(data_file)
            email = data[website]["email"]
            password = data[website]["password"]

    except FileNotFoundError:
        if messagebox.askyesno("Error", f"File '{file}' missing \nDo you want to create a file?"):
            new_file_window()

    except KeyError:
        messagebox.showerror("Error", f"Website '{website}' missing")

    else:
        messagebox.showinfo(website, f"Email: {email} \nPassword: {password}")

# --------------------------------- UI SETUP ----------------------------------- #

# Window


main_window = Tk()
main_window.title("Password Manager")
main_window.config(padx=30, pady=30, bg=BG_COLOR)

# Canvas
canvas = Canvas(width=200, height=170, highlightthickness=0)
bg_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=bg_image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", font=FONT, fg=FONT_COLOR, bg=BG_COLOR)
website_label.grid(column=0, row=1, sticky="E")

email_user_label = Label(text="Email/Username:", font=FONT, fg=FONT_COLOR, bg=BG_COLOR)
email_user_label.grid(column=0, row=2, sticky="E")

password_label = Label(text="Password:", font=FONT, fg=FONT_COLOR, bg=BG_COLOR)
password_label.grid(column=0, row=3, sticky="E")

# Entries
website_entry = Entry(width=30)
website_entry.grid(column=1, row=1, sticky="W")
website_entry.focus()

email_entry = Entry(width=30)
email_entry.grid(column=1, row=2, columnspan=2, sticky="W")
email_entry.insert(0, "useremail@gmail.com")

password_entry = Entry(width=30)
password_entry.grid(column=1, row=3, sticky="W")

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password, bg=BUTTON_COLOR)
generate_password_button.grid(column=2, row=3, sticky="E")

add_button = Button(text="Add data", command=save_password, bg=BUTTON_COLOR)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW", pady=(20, 0))

search_button = Button(text="Search", command=search_password, bg=BUTTON_COLOR)
search_button.grid(column=2, row=1, sticky="EW")

main_window.mainloop()
