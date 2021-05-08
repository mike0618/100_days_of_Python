from tkinter import *
from tkinter import messagebox
from string import ascii_lowercase, ascii_uppercase, digits
from random import randint, choice, shuffle
import pyperclip


# ---------------------------- ENCRYPTION/DECRYPTION ---------------------------- #
def crypt(pw, decrypt=False):
    k = 1
    if decrypt:
        k = -1
    key = key_entry.get()
    password = ''
    if key.isdigit():
        for i in range(len(pw)):
            password += chr(ord(pw[i]) + k * int(key[i % len(key)]))
        return password
    else:
        return pw


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def passgen():
    l_list = [choice(ascii_lowercase) for _ in range(randint(3, 5))]
    up_list = [choice(ascii_uppercase) for _ in range(randint(3, 5))]
    n_list = [choice(digits) for _ in range(randint(2, 4))]
    s_list = [choice('!?#$%&*()+-,.') for _ in range(randint(2, 4))]

    password_list = l_list + up_list + n_list + s_list
    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.delete(0, END)
    pass_entry.insert(END, password)
    pyperclip.copy(password)
    info_label.config(fg='#499c59', text='New password copied to clipboard')


# ---------------------------- SHOW/HIDE PASSWORDS ------------------------------- #
def show():
    site = site_entry.get()
    login = login_entry.get()
    if site or login:
        info_label.config(text='')
        i_site = ''
        i_login = ''
        with open('data.txt') as f:
            for string in f:
                entry = string.split()
                if site == entry[0]:
                    i_site += f'{entry[1]} : {crypt(entry[2], True)}\n'
                if login == entry[1]:
                    i_login += f'{entry[0]} : {crypt(entry[2], True)}\n'
        text.focus()
        text.delete(1.0, END)
        if i_site:
            text.insert(END, f'{site}\n{i_site}\n')
        if i_login:
            text.insert(END, f'{login}\n{i_login}\n')
        text.grid(row=6, column=0, columnspan=3)
        hide_btn.grid(row=5, column=0)
    else:
        text.delete(1.0, END)
        info_label.config(fg='#fec269', text='Fill out "Website" or "Login" field')


def hide():
    text.grid_remove()
    text.delete(1.0, END)
    hide_btn.grid_remove()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    site = site_entry.get()
    login = login_entry.get()
    passw = pass_entry.get()
    exists = False

    if site and login and passw:
        with open('data.txt') as f:
            for string in f:
                entry = string.split()
                if site == entry[0] and login == entry[1] and passw == crypt(entry[2]):
                    exists = True
                    info_label.config(fg='#fec269', text='This entry already exists')
                    break
        if not exists:
            is_ok = messagebox.askokcancel(title=site, message=f'These are the details entered:\nLogin: {login}'
                                                               f'\nPassword: {passw}\nIs it ok to save?')
            if is_ok:
                with open('data.txt', 'a') as f:
                    f.write(f'{site} {login} {crypt(passw)}\n')
                    login_entry.delete(0, END)
                    pass_entry.delete(0, END)
                    info_label.config(fg='#499c59', text=f'Entry for {site} added')
                    site_entry.delete(0, END)
    else:
        info_label.config(fg='#fec269', text='Fill out the form')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
# window.minsize(width=600, height=500)
window.config(padx=30, pady=20, bg='#363636')

canvas = Canvas(width=320, height=140, bg='#363636', highlightthickness=0)
logo = PhotoImage(file='key.png')
canvas.create_image(160, 70, image=logo)
logo_text = canvas.create_text(200, 45, text='My Pass', fill='#fec269', font=('Courier', 21, 'bold italic'))
canvas.grid(row=0, column=0, columnspan=2, rowspan=2)

site_label = Label(pady=5, text=' Website:', fg='white', bg='#363636', font=('Courier', 13, 'bold'))
site_label.grid(row=2, column=0)
login_label = Label(pady=5, text='   Login:', fg='white', bg='#363636', font=('Courier', 13, 'bold'))
login_label.grid(row=3, column=0)
pass_label = Label(pady=5, text='Password:', fg='white', bg='#363636', font=('Courier', 13, 'bold'))
pass_label.grid(row=4, column=0)
info_label = Label(pady=5, text='', fg='#499c59', bg='#363636', font=('Courier', 13, 'bold'))
info_label.grid(row=7, column=1, columnspan=2)
key_label = Label(text='PIN:', fg='white', bg='#363636', font=('Courier', 13, 'bold'))
key_label.grid(row=0, column=2, sticky='s')

site_entry = Entry(width=55)
site_entry.focus()
site_entry.grid(row=2, column=1, columnspan=2)
login_entry = Entry(width=55)
login_entry.grid(row=3, column=1, columnspan=2)
pass_entry = Entry(width=34)
pass_entry.grid(row=4, column=1)
key_entry = Entry(width=20, fg='white', bg='white')
key_entry.grid(row=1, column=2, sticky='n')

gen_btn = Button(padx=42, pady=1, text="Generate", anchor='s', highlightthickness=0, fg='white', bg='#363636',
                 activeforeground='white', activebackground='#595959', font=('Courier', 13, 'normal'), command=passgen)
gen_btn.grid(row=4, column=2)
show_btn = Button(padx=118, pady=1, text="Show", anchor='s', highlightthickness=0, fg='white', bg='#363636',
                  activeforeground='white', activebackground='#7d5d30', font=('Courier', 13, 'normal'), command=show)
show_btn.grid(row=5, column=1)
hide_btn = Button(padx=24, pady=1, text="Hide", anchor='s', highlightthickness=0, fg='white', bg='#7d5d30',
                  activeforeground='white', activebackground='#499c59', font=('Courier', 13, 'normal'), command=hide)
add_btn = Button(padx=66, pady=1, text="Add", anchor='s', highlightthickness=0, fg='white', bg='#363636',
                 activeforeground='white', activebackground='#499c59', font=('Courier', 13, 'normal'), command=save)
add_btn.grid(pady=3, row=5, column=2)

text = Text(width=67, height=13)

window.mainloop()