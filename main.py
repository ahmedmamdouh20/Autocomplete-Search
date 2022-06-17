import nltk
import tkinter as tk
from tkinter import END
# nltk.download('punkt')

def read_file(file_name):
    with open(file_name, encoding='iso-8859-1') as f:
        file = ""
        for line in f.readlines():
            file += line.strip()
        f.close()
        return file


words = read_file('Sport_-_50K.txt.txt')
nltk_tokens = nltk.word_tokenize(words)
words_bigram = list(nltk.bigrams(nltk_tokens))

# print(words_bigram)


table = []
for tupple in words_bigram:
    if tupple[0] not in table:
        table.append(tupple[0])

rows, cols = (len(table), len(table))
raw_table = [[0 for i in range(cols)] for j in range(rows)]

for tuple in words_bigram:
    i = table.index(tuple[0])
    j = table.index(tuple[1])
    raw_table[i][j] += 1

for i in range(len(table)):
    repetition = words.count(table[i])
    for j in range(len(raw_table)):
        if repetition == 0:
            repetition = 1
        raw_table[i][j] = raw_table[i][j] / repetition


def complete(word, table, raw_table):
    index = []
    try:
        i = table.index(word)  # raw_table[i]
    except ValueError:
        return []
    for counter in range(5):
        maxi = 0
        indexx = 0
        for j in range(len(raw_table[i])):
            if raw_table[i][j] > maxi and j not in index:
                maxi = raw_table[i][j]
                indexx = j
        index.append(indexx)
    completed = []
    for i in range(len(index)):
        if index[i] != 0:
            completed.append(table[index[i]])
    return completed


# print(*raw_table, sep='\n')

# --------------------------------- GUI --------------------------------------

gui = tk.Tk()
gui.geometry('701x470')  # Size of the window
gui.title("Google")  # Adding a title
gui.configure(bg='white')

img = tk.PhotoImage(file="google.png")
label = tk.Label(gui, image=img)
label.place(x=0, y=0)

font1 = ('Times', 24, 'bold')
e1_str = tk.StringVar()
e1 = tk.Entry(gui, font=font1, textvariable=e1_str)
e1.grid(row=0, column=1, padx=20, pady=0, ipadx=100)
e1.place(x=85, y=168, width=525)
l1 = tk.Listbox(gui, height=5, font=font1, relief='flat', bg='white', highlightcolor='white')
l1.grid(row=1, column=1)
l1.place(x=85, y=205, width=525)


def my_update(my_widget):
    gui = my_widget.widget
    try:
        index = int(gui.curselection()[0])
        value = gui.get(index)
        e1_str.set(e1.get() + ' ' + value)
        l1.delete(0, END)
    except IndexError:
        pass



def get_data(*args):
    search_str = e1.get()  # user entered string
    l1.delete(0, END)
    my_list = complete(search_str, table, raw_table)
    for element in my_list:
        l1.insert(tk.END, element)


l1.bind("<<ListboxSelect>>", my_update)

e1_str.trace('w', get_data)

gui.mainloop()  # Keep the window open
