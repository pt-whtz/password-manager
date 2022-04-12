from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import os

BG_COLOR = "#3b474a"
CREATE_FILE_BG_COLOR = "#F1DDBF"
FILES_BG_COLOR = "#c4c8c9"
BUTTON_COLOR = "#E2D784"
FONT_COLOR = "#F5F5F5"
FONT = ("Consolas", 13)

# ------------------------------ FILE MANAGEMENT -------------------------------- #


def file_creator_window():

    def create_file():

        user_file = data_file_entry.get()
        file_path = f"./data/{user_file}.json"
        file_exists = os.path.exists(file_path)
        if file_exists:
            messagebox.showinfo("Oops", "File already exists")
        else:
            new_file = open(file_path, "w")
            files_collection.insert(END, f"{user_file}.json")
            main_window.attributes('-disabled', False)
            new_window.destroy()
            new_file.close()

    new_window = Toplevel()
    new_window.title("Create a new file")
    new_window.grab_set()
    new_window.attributes('-topmost', True)
    new_window.config(width=300, height=200, bg=CREATE_FILE_BG_COLOR, padx=40, pady=60)
    new_window.protocol("WM_DELETE_WINDOW", main_window.attributes('-disabled', False))

    data_file_entry = Entry(new_window)
    data_file_entry.focus_set()
    data_file_entry.grid(column=1, row=0)

    data_file_label = Label(new_window, text="File name: ", bg=CREATE_FILE_BG_COLOR, font=FONT)
    data_file_label.grid(column=0, row=0)

    file_extension_label = Label(new_window, text=".json", bg=CREATE_FILE_BG_COLOR, font=FONT)
    file_extension_label.grid(column=2, row=0)

    save_button = Button(new_window, width=30, text="Save", command=create_file, bg=BUTTON_COLOR)
    save_button.grid(column=0, row=2, columnspan=3, pady=(20, 0))


def delete_file():

    is_selected = files_collection.curselection()
    if is_selected:
        file_name = files_collection.get(is_selected)
        if messagebox.askyesno("File Manager", f"Do you want to delete '{file_name}'?"):
            files_collection.delete(is_selected)
            os.remove(path=f"./data/{file_name}")
            messagebox.showinfo("File Manager", f"File '{file_name} deleted.'")
    else:
        messagebox.showinfo("Oops", "- collection is empty \n- or file not selected")

# ---------------------------- PASSWORD MANAGEMENT ------------------------------ #


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


def save_password():

    is_selected = files_collection.curselection()
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
             "email": email,
             "password": password,
        }
    }

    if is_selected:
        file_name = files_collection.get(is_selected)

        if len(website) == 0 or len(password) == 0 or len(email) == 0:
            messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

        else:

            try:
                with open(f"./data/{file_name}", "r") as data_file:
                    data = json.load(data_file)

            except (FileNotFoundError, json.JSONDecodeError):
                with open(f"./data/{file_name}", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                data.update(new_data)
                with open(f"./data/{file_name}", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.focus()

    else:
        messagebox.showinfo("Oops", "- collection is empty \n- or file not selected")


def search_password():

    website = website_entry.get().title()
    is_selected = files_collection.curselection()

    if is_selected:

        file_name = files_collection.get(is_selected)

        try:
            with open(f"./data/{file_name}", "r") as data_file:
                data = json.load(data_file)
                email = data[website]["email"]
                password = data[website]["password"]

        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showinfo(title="Oops", message="Website not found")

        except KeyError:
            messagebox.showerror("Error", f"Website '{website}' missing")

        else:
            messagebox.showinfo(website, f"Email: {email} \nPassword: {password}")

    else:
        messagebox.showinfo("Oops", "- collection is empty \n- or file not selected")

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

files_collection_label = Label(text="Select file from your collection:", font=FONT, fg=FONT_COLOR, bg=BG_COLOR)
files_collection_label.grid(column=1, row=5, columnspan=2, sticky="EW", pady=(20, 0))

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

save_data_button = Button(text="Save data", command=save_password, bg=BUTTON_COLOR)
save_data_button.grid(column=1, row=4, columnspan=2, sticky="EW", pady=(20, 0))

search_button = Button(text="Search", command=search_password, bg=BUTTON_COLOR)
search_button.grid(column=2, row=1, sticky="EW")

create_button = Button(text="Create", command=file_creator_window, bg=BUTTON_COLOR, width=10)
create_button.grid(column=1, row=7, pady=(10, 0))

delete_button = Button(text="Delete", command=delete_file, bg=BUTTON_COLOR, width=10)
delete_button.grid(column=2, row=7, pady=(10, 0))

# Listbox
files = os.listdir(path="./data/")
files_collection = Listbox(font=FONT, bg=FILES_BG_COLOR, highlightthickness=0, selectbackground="#383838", height=4)

for file in files:
    files_collection.insert(END, file)

files_collection.grid(column=1, row=6, columnspan=2, sticky="EW")
files_collection.lb = Listbox(files_collection, selectmode=MULTIPLE, bd=1, height=10, font=('Times', 14))


main_window.mainloop()
