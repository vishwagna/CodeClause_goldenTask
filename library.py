import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
# Connecting to Database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
conn.execute('''create table if not exists library(book_name text,
              id text primary key NOT NULL,author_name text,
              book_status text,card_id text)''')

root=Tk()
root.title('LIBRARY MANAGEMENT SYSTEM')
root.geometry('1000x600')
root.resizable(False,False)
Label(root, text='LIBRARY MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 18, 'bold'), bg='#025464', fg='White').pack(side=TOP, fill=X)
book_status = StringVar()
book_name = StringVar()
id = StringVar()
author_name = StringVar()
card_id = StringVar()
def Card_Id():
    cid = sd.askstring('Issuer\'s Card ID', 'Enter the Issuer\'s Card ID?')
    while not cid:
     mb.showerror('Empty value is not allowed', 'Enter issuer\'s card id')
     cid = sd.askstring('Issuer\'s Card ID', 'Enter the Issuer\'s Card ID?')
    else:
      return cid
def show_records():
    global conn, cursor
    global tree
    tree.delete(*tree.get_children())
    curr = conn.execute('SELECT * FROM Library')
    data = curr.fetchall()
    for records in data:
        tree.insert('', END, values=records)
def clear_fields():
    global book_status, id, book_name, author_name, card_id
    book_status.set('Available')
    for i in ['id', 'book_name', 'author_name', 'card_id']:
        exec(f"{i}.set('')")
        bk_id.config(state='normal')
    try:
      tree.selection_remove(tree.selection()[0])
    except:
           pass
def clear_and_display():
     clear_fields()
     show_records()
def view_record():
         global book_name, id, book_status, author_name, card_id
         global tree
         if not tree.focus():
           mb.showerror('Select a row!', 'Row must be selected to view it.')
           return
         current_item_selected = tree.focus()
         values_in_selected_item = tree.item(current_item_selected)
         selection = values_in_selected_item['values']
         book_name.set(selection[0]) ; id.set(selection[1]) ; book_status.set(selection[3])
         author_name.set(selection[2])
def add():
    global conn
    global book_name, id, author_name, book_status
    if id.get() and book_name.get() and author_name.get():
        if book_status.get() == 'Issued':
            card_id.set(Card_Id())
        else:
            card_id.set('N/A')
        surety = mb.askyesno('Are you sure?','Do you really want to add this data?\nBook id cannot be changed in future!!')
        if surety:
            try:
                    conn.execute(
                    'INSERT INTO Library (book_name, id, author_name, book_status, card_id) VALUES (?, ?, ?, ?, ?)',
                            (book_name.get(), id.get(), author_name.get(), book_status.get(), card_id.get()))
                    conn.commit()
                    clear_and_display()
        
                    mb.showinfo('Success', 'The new record was successfully added to your database')
            except sqlite3.IntegrityError:
                    mb.showerror('Book ID already in use!',
                                'The Book ID you are trying to enter is already in the database!')
    else:
        mb.showerror('empty values not allowed','please fill all fields to continue!!')
def update_record():
   def update():
       global book_status, book_name, id, author_name, card_id
       global conn, tree
       if book_status.get() == 'Issued':
             card_id.set(Card_Id())
       else:
             card_id.set('N/A')
       cursor.execute('UPDATE Library SET book_name=?, book_status=?, author_name=?, card_id=? WHERE id=?', (book_name.get(), book_status.get(), author_name.get(), card_id.get(), id.get()))
       conn.commit()
       clear_and_display()
       edit.destroy()
       bk_id.config(state='normal')
       clear.config(state='normal')
   view_record()
   bk_id.config(state='disable')
   clear.config(state='disable')
   edit = Button(r_frame, text='Update Record', font=('Gill Sans MT', 13), bg='steelblue', width=20, command=update)
   edit.place(x=50, y=375)
def remove_record():
 if not tree.selection():
  mb.showerror('Error!', 'Please select an item from the database')
  return
 current_item = tree.focus()
 values = tree.item(current_item)
 selection = values["values"]
 cursor.execute('DELETE FROM Library WHERE id=?', (selection[1], ))
 conn.commit()
 tree.delete(current_item)
 mb.showinfo('Done', 'The record you wanted to delete was successfully deleted.')
 clear_and_display()
def delete_inventory():
 if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire inventory?\n\nThis command cannot be reversed'):
  tree.delete(*tree.get_children())
  cursor.execute('DELETE FROM Library')
  conn.commit()
 else:
  return
def change_availability():
 global card_id, tree, conn
 if not tree.selection():
  mb.showerror('Error!', 'Please select a book from the database')
  return
 current_item = tree.focus()
 values = tree.item(current_item)
 BK_id = values['values'][1]
 BK_status = values["values"][3]
 if BK_status == 'Issued':
  surety = mb.askyesno('Is return confirmed?', 'Has the book been returned to you?')
  if surety:
       cursor.execute('UPDATE Library SET book_status=?, card_id=? WHERE id=?', ('Available', 'N/A', BK_id))
       conn.commit()
  else: mb.showinfo(
      'Cannot be returned', 'The book status cannot be set to Available unless it has been returned')
 else:
     cursor.execute('UPDATE Library SET book_status=?, card_id=? where id=?', ('Issued', Card_Id(), BK_id))
     conn.commit()
 clear_and_display()
r_frame = Frame(root, bg='#57C5B6')
r_frame.place(x=700, y=35, relwidth=0.3, relheight=0.96)
Label(r_frame, text='Book Name',font=('Georgia',15)).place(x=98, y=25)
Entry(r_frame, width=25, font=('Times New Roman',14), text=book_name).place(x=35, y=65)
Label(r_frame,text='Book Id',font=('Georgia',15)).place(x=118, y=105)
bk_id=Entry(r_frame, width=25, font=('Times New Roman',14), text=id)
bk_id.place(x=35, y=145)
Label(r_frame, text='Author Name',font=('Georgia',15)).place(x=98, y=185)
Entry(r_frame, width=25, font=('Times New Roman',14), text=author_name).place(x=35, y=225)
Label(r_frame, text='Book Status',font=('Georgia',15)).place(x=98, y=265)
opt = OptionMenu(r_frame, book_status, *['Available', 'Issued'])
opt.configure(font=('Times New Roman',14), width=12)
opt.place(x=75, y=305)
submit = Button(r_frame, text='Add new record', font=('Gill Sans MT', 13), bg='#159895', width=20,command=add)
submit.place(x=50, y=375)
clear = Button(r_frame, text='Clear fields', font=('Gill Sans MT', 13), bg='#159895', width=20,command=clear_fields)
clear.place(x=50, y=435)


btm_frame = Frame(root, bg='#27E1C1')
btm_frame.place(x=0, y=500, relheight=0.4, relwidth=0.7)
Button(btm_frame, text='Delete book record', font=('Gill Sans MT', 13), bg='#159895', width=17,command=remove_record).place(x=8, y=30)
Button(btm_frame, text='Delete full inventory', font=('Gill Sans MT', 13), bg='#159895', width=17,command=delete_inventory).place(x=178, y=30)
Button(btm_frame, text='Update book details', font=('Gill Sans MT', 13), bg='#159895', width=17,command=update_record).place(x=348, y=30)
Button(btm_frame, text='Change Book Availability', font=('Gill Sans MT', 13), bg='#159895', width=19,command=change_availability).place(x=518, y=30)
top_frame = Frame(root)
top_frame.place(x=0, y=35, relheight=0.785, relwidth=0.7)
Label(top_frame, text='LIBRARY CATALOGUE', bg='#DAFFFB', font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)
tree = ttk.Treeview(top_frame, selectmode=BROWSE, columns=('Book Name', 'Book ID', 'Author', 'Status', 'Issuer Card ID'))
XScrollbar = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
YScrollbar = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
XScrollbar.pack(side=BOTTOM, fill=X)
YScrollbar.pack(side=RIGHT, fill=Y)
tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)
tree.heading('Book Name', text='Book Name', anchor=CENTER)
tree.heading('Book ID', text='Book ID', anchor=CENTER)
tree.heading('Author', text='Author', anchor=CENTER)
tree.heading('Status', text='Status of the Book', anchor=CENTER)
tree.heading('Issuer Card ID', text='Card ID of the Issuer', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=225, stretch=NO)
tree.column('#2', width=70, stretch=NO)
tree.column('#3', width=150, stretch=NO)
tree.column('#4', width=105, stretch=NO)
tree.column('#5', width=132, stretch=NO)
tree.place(y=30, x=0, relheight=0.9, relwidth=1)
clear_and_display()

root.update()
root.mainloop()