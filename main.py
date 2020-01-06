#!/usr/bin/python

# pip install mysql-connector-python

import mysql.connector as mariadb
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

def tkn(root, widget, *args, **kwargs):
	class limbo():
		def grid(self, column, row, *args, **kwargs):
			self.obj.grid(column=column, row=row, *args, **kwargs)
			return self.obj
		def pack(self, *args, **kwargs):
			self.obj.pack(*args, **kwargs)
			return self.obj

	lim = limbo()
	lim.obj = widget(root, *args, **kwargs)

	return lim

def connect_db():

	pop = tk.Toplevel()
	pop.title('Connect DB')
	pop.resizable(0, 0)
	mfr = tkn(pop, ttk.Frame).grid(0, 0, padx=24, pady=18)
	
	tkn(mfr, tk.Label, text='Username: ', font=('',10)).grid(0, 0, sticky='e', pady=(8, 0))
	username_entry = tkn(mfr, ttk.Entry, width=14).grid(1, 0, pady=(8, 0))

	tkn(mfr, tk.Label, text='Password: ', font=('', 10)).grid(0, 1, sticky='e', pady=(8, 0))
	password_entry = tkn(mfr, ttk.Entry, width=14, show='•').grid(1, 1, pady=(8, 0))

	tkn(mfr, ttk.Separator).grid(0, 2, columnspan=2, pady=(14, 14), sticky='ew')

	tkn(mfr, tk.Label, text='Database: ', font=('', 10)).grid(0, 3, sticky='e', pady=(0, 18))
	database_entry = tkn(mfr, ttk.Entry, width=14).grid(1, 3, pady=(0, 18))
	
	def connect_event():
		try:
			global mariadb_connection, cursor
			mariadb_connection = mariadb.connect(user=username_entry.get(), password=password_entry.get(), database=database_entry.get())
			cursor = mariadb_connection.cursor()
			pop.destroy()
		except Exception as E:
			showerror('Error', E)

	connect_button = tkn(mfr, ttk.Button, text='Connect', width=22, command=connect_event).grid(0, 4, columnspan=2)
	pop.grab_set()

	def on_exit():
		if cursor==None:
			connect_db()
			pop.destroy()

	pop.protocol('WM_DELETE_WINDOW', on_exit)

root = tk.Tk()
root.resizable(0, 0)
frm = tkn(root, tk.Frame).grid(0, 0, padx=24, pady=18)

cmd_output = tkn(frm, tk.Text, width=40, height=20, state='disabled', font=('Consolas', 10)).grid(0, 0)
cmd_entry = tkn(frm, ttk.Entry, width=40, font=('Consolas', 10)).grid(0, 1)
tkn(frm, tk.Label, text=';', font=('Consolas', 10)).grid(0, 1, columnspan=2, sticky='e')

def cmd_send(a):
	cursor.execute("SELECT * FROM Book")
	print(dir(cursor))
	# try:
	# 	cmd_output.insert(tk.END, cursor.execute(cmd_entry.get())+'\n')
	# except Exception as E:
	# 	cmd_output.insert(tk.END, str(E)+'\n')
	cmd_output.see(tk.END)
	cmd_entry.delete(0, tk.END)

cmd_entry.bind('<Return>', cmd_send)

mariadb_connection = None
cursor = None

root.after(250, connect_db)

def on_exit():
	if mariadb_connection != None: mariadb_connection.close()
	if cursor != None: cursor.close()
	root.destroy()

root.protocol('WM_DELETE_WINDOW', on_exit)

tk.mainloop()