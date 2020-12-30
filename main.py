import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
import win32api
from PIL import Image


class DirectoryEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        callbackCreated(f"{datetime.datetime.now()}: {event.src_path} has been created")

    def on_deleted(self, event):
        callbackDeleted(f"{datetime.datetime.now()}: {event.src_path} has been deleted")

    def on_modified(self, event):
        callbackModified(f"{datetime.datetime.now()}: {event.src_path} has been modified")

    def on_moved(self, event):
        callbackMoved(f"{datetime.datetime.now()}: {event.src_path} moved to {event.dest_path}")


def start_observer(path):
    global observer, event_handler
    global file
    dat = str(datetime.datetime.today())
    dat = dat.replace(':', '-')
    dat = dat.replace('.', ',')
    print(dat)
    type = 'log.txt'
    filename = dat + type
    print(filename)
    file = open(filename, 'w', encoding="utf-8")
    print(f"{datetime.datetime.now()}: Started watching {path}")
    callbackCreated(f"{datetime.datetime.now()}: Started watching {path}")
    callbackDeleted(f"{datetime.datetime.now()}: Started watching {path}")
    callbackModified(f"{datetime.datetime.now()}: Started watching {path}")
    callbackMoved(f"{datetime.datetime.now()}: Started watching {path}")
    observer.schedule(event_handler, path, recursive=True)
    observer.start()


def stop_observer():
    global observer
    observer.stop()
    observer.join()
    file.close()

def callbackCreated(message):
    global sctext_logCreated
    file.write(message+'\n')
    sctext_logCreated.configure(state='normal')
    sctext_logCreated.insert('end', message+'\n')
    sctext_logCreated.configure(state='disabled')
    return True

def callbackDeleted(message):
    global sctext_logDeleted
    file.write(message+'\n')
    sctext_logDeleted.configure(state='normal')
    sctext_logDeleted.insert('end', message+'\n')
    sctext_logDeleted.configure(state='disabled')
    return True

def callbackModified(message):
    global sctext_logModified
    file.write(message+'\n')
    sctext_logModified.configure(state='normal')
    sctext_logModified.insert('end', message+'\n')
    sctext_logModified.configure(state='disabled')
    return True

def callbackMoved(message):
    global sctext_logMoved
    file.write(message+'\n')
    sctext_logMoved.configure(state='normal')
    sctext_logMoved.insert('end', message+'\n')
    sctext_logMoved.configure(state='disabled')
    return True

def exit():
    global root
    stop_observer()
    root.destroy()


def choose_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        start_observer(dir_path)

#def saving(message):
 #   file.write(message + '\n')

if __name__ == "__main__":
    event_handler = DirectoryEventHandler()
    observer = Observer()
    path = None
    # объявление элементов интерфейса
    root = tk.Tk()  # главное окно
    root.title("Folder watcher")  # его заголовок

    button_choose_dir = ttk.Button(root, text='Choose a folder', command=choose_dir)  # кнопка выбора директории
    button_exit = ttk.Button(root, text='Exit', command=exit)  # кнопка выхода
    #button_save = ttk.Button(root, text='Save', command=saving())
    sctext_logCreated = scrolledtext.ScrolledText(root, height=5, width=40, font=("Times New Roman", 12))  # окно журнала
    sctext_logDeleted = scrolledtext.ScrolledText(root, height=5, width=40, font=("Times New Roman", 12))
    sctext_logModified = scrolledtext.ScrolledText(root, height=5, width=40, font=("Times New Roman", 12))
    sctext_logMoved = scrolledtext.ScrolledText(root, height=5, width=40, font=("Times New Roman", 12))
    #sctext_log.insert(END, " in ScrolledText")
    #print(sctext_log.get(1.0, END))
    sctext_logCreated.configure(state='disabled')
    sctext_logDeleted.configure(state='disabled')
    sctext_logModified.configure(state='disabled')
    sctext_logMoved.configure(state='disabled')
    labelCreated = tk.Label(text="On created", font=("Arial 14"))
    labelDeleted = tk.Label(text="On deleted", font=("Arial 14"))
    labelModified = tk.Label(text="On modified", font=("Arial 14"))
    labelMoved = tk.Label(text="On moved", font=("Arial 14"))



    # позиционирование элементов
    root.grid()
    root.grid_rowconfigure(0, weight=1)  # включаем реагирование столбцов/строк окна на его масштабирование
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    button_choose_dir.grid(row=0, column=0, pady=10, padx=10, sticky='nw')  # размещаем элементы
    button_exit.grid(row=0, column=1, pady=10, padx=10, sticky='n')
    #button_save.grid(row=1, column=1, pady=10, padx=10, sticky='es')
    sctext_logCreated.grid(row=2, column=0, pady=10, padx=10, sticky='w')
    sctext_logDeleted.grid(row=4, column=0, pady=10, padx=10, sticky='w')
    sctext_logModified.grid(row=2, column=1, pady=10, padx=10, sticky='e')
    sctext_logMoved.grid(row=4, column=1, pady=10, padx=10, sticky='e')
    labelCreated.grid(row=1, column=0, pady=10, padx=10, sticky='w')
    labelDeleted.grid(row=3, column=0, pady=10, padx=10, sticky='w')
    labelModified.grid(row=1, column=1, pady=10, padx=10, sticky='e')
    labelMoved.grid(row=3, column=1, pady=10, padx=10, sticky='e')

    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    i = 0
    for disk in drives:
        a, b, c = win32api.GetDiskFreeSpaceEx(drives[i])
        name = drives[i]
        print(drives[i], 'Всего Мегабайт:', b / 1000000, 'Свободно Мегабайт:', a / 1000000, round(a / b * 100, 2),
              '%')
        i += 1
        frame = tk.Frame(master=root, relief=tk.RAISED, borderwidth=1)
        frame.grid(row=0, column=i + 1)
        label = tk.Label(master=frame, text=f"Диск:{name}\nВсего Мегабайт {b}\nСвободно Мегабайт {a}")
        label.pack()

    root.mainloop()  # запускаем работу основного потока программы
