'''
    ui.py
'''

import main
import json
import tkinter as tk
from tkinter.constants import *
from tkinter.filedialog import askdirectory, askopenfile

debug = lambda cls, info: print(f'[{cls: ^10}] {info}')

def setentry(entry: tk.Entry, text: str) -> None:
    entry.delete(0, END)
    entry.insert(0, text)

class App(tk.Tk):
    def __init__(self):
        '''
        Represents the app.
        '''
        
        # Settings
        tk.Tk.__init__(self)
        self.title('BWF')
        self.geometry('650x300')
        
        # Instances
        self.decryption_instances = 0
        self.encryption_instances = 0
        
        self.decryption_string = tk.StringVar(value = f'Decrypt')
        self.encryption_string = tk.StringVar(value = f'Encrypt')
        
        # Encoding options
        self.encryptor: main.Encryptor = None
        self.backend: main.Backend = eval(f"main.{open('./user/settings').read()}")
        
        # Sequence start
        self.home()
    
    def set_instances_counter(self, instance: str, inc: bool) -> None:
        '''
        Increment or decrement instances counters.
        '''
        
        if 'decrypt' in instance:
            self.decryption_instances += 1 if inc else -1
            self.decryption_string.set(f'Decrypt\n({self.decryption_instances} instances)')
        else:
            self.encryption_instances += 1 if inc else -1
            self.encryption_string.set(f'Encrypt\n({self.encryption_instances} instances)')
    
    def clear(self) -> None:
        '''
        Remove every widget from the window.
        '''
        
        for widget in self.winfo_children(): widget.destroy()
    
    def home(self, encryption_key: bytes = None) -> None:
        '''
        Home page.
        '''
        
        self.clear()
        if encryption_key: self.encryptor = main.Encryptor(encryption_key)
        self.geometry('530x215')
        
        decryption = tk.Button(self, textvariable = self.decryption_string, command = self.decrypt, width = 35, height = 10)
        encryption = tk.Button(self, textvariable = self.encryption_string, command = self.encrypt, width = 35, height = 10)
        settings = tk.Button(self, text = '#', width = 2, height = 1, command = self.settings)
        
        # Griding
        tk.Label(self, text = 'BWF', font = ('Arial', 25)).grid(row = 1, column = 1, sticky = 'w', padx = 5)
        decryption.grid(row = 2, column = 1, padx = 5, pady = 5)
        encryption.grid(row = 2, column = 2, padx = 5, pady = 5)
        
        settings.grid(row = 1, column = 2, sticky = 'e', padx = 5)

    def settings(self) -> None:
        '''
        Settings page.
        '''
        
        def on_save(*_):
            '''
            Handle settings saving.
            '''
            
            # Encryption
            if pwd.get(): self.encryptor = main.Encryptor(pwd.get())
            
            # Backend
            be = backend.curselection()
            if len(be):
                new = main.BACKENDS[be[0]]
                self.backend = eval(f'main.{new}')
                open('./user/settings.json', 'w').write(new)
            
            # Quit
            # top.destroy()
            
        
        top = tk.Toplevel(self)
        top.geometry('150x200')
        
        backend = tk.Listbox(top, height = 6)
        [backend.insert(*a) for a in enumerate(main.BACKENDS)]
        
        pwd = tk.Entry(top)
        save = tk.Button(top, text = 'Save', command = on_save)
        
        # Packing
        tk.Label(top, text = 'Backend').pack()
        backend.pack()
        tk.Label(top, text = 'Encryption key').pack()
        pwd.pack()
        save.pack()
        
        top.mainloop()
    
    def decrypt(self) -> None:
        '''
        Decryption process page.
        '''
        
        def on_confirm(*_):
            '''
            Handle decryption.
            '''
            
            res = self.backend.decrypt_to_folder(self.encryptor,
                                                 source_entry.get(),
                                                 target_entry.get())
            
            self.finish('Finished job:\n' + json.dumps(res, indent = 3))
        
        def on_cancel(*_):
            self.set_instances_counter('decrypt', 0)
            top.destroy()
        
        top = tk.Toplevel(self)
        top.geometry('400x400')
        self.set_instances_counter('decrypt', 1)
        
        source_entry = tk.Entry(top)
        target_entry = tk.Entry(top)
        
        source_select = tk.Button(top, text = 'Source (rtf)', command = lambda *_: setentry(source_entry, askopenfile(mode = 'r').name))
        target_select = tk.Button(top, text = 'Target (dir)', command = lambda *_: setentry(target_entry, askdirectory()))
        
        close = tk.Button(top, text = 'Cancel', command = on_cancel)
        confirm = tk.Button(top, text = 'OK', command = on_confirm)
        
        # Packing
        source_entry.pack()
        target_entry.pack()
        
        source_select.pack()
        target_select.pack()
        
        close.pack()
        confirm.pack()
        
        top.mainloop()
    
    def encrypt(self) -> None:
        '''
        Encryption process page.
        '''
        
        def on_confirm(*_):
            '''
            Handle encryption.
            '''
            
            source = source_entry.get()
            target = target_entry.get()
            
            res = self.backend.encrypt_to_rtf(
                self.encryptor,
                source,
                target
            )
            
            self.finish('Finished job:\n' + json.dumps(res, indent = 3))
        
        def on_cancel(*_):
            self.set_instances_counter('encrypt', 0)
            top.destroy()
        
        top = tk.Toplevel(self)
        top.geometry('400x400')
        self.set_instances_counter('encrypt', 1)
        
        source_entry = tk.Entry(top)
        target_entry = tk.Entry(top)
        
        source_select = tk.Button(top, text = 'Source (dir)', command = lambda *_: setentry(source_entry, askdirectory()))
        target_select = tk.Button(top, text = 'Target (rtf)', command = lambda *_: setentry(target_entry, askopenfile(mode = 'r').name))
        
        close = tk.Button(top, text = 'Cancel', command = on_cancel)
        confirm = tk.Button(top, text = 'OK', command = on_confirm)
        
        # Packing
        source_entry.pack()
        target_entry.pack()
        
        source_select.pack()
        target_select.pack()
        
        close.pack()
        confirm.pack()
        
        top.mainloop()

    def finish(self, text: str) -> None:
        '''
        Shows a popup with a result.
        '''
        
        top = tk.Toplevel(self)
        tk.Label(top, text = text, anchor = 'w').pack()
        top.mainloop()
        

if __name__ == '__main__':
    
    app = App()
    app.mainloop()