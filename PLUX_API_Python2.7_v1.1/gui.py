import tkinter as tk
import threading
import time
from pynput import keyboard
from tkinter import ttk
from win32api import GetSystemMetrics
from PIL import ImageTk, Image
from Device import MyDevice as dev
from DeviceFunction import GlobalFunction as devFunction

def make_frame(master, x, y, w, h, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w, *args, **kwargs)
    f.pack_propagate(0) # don't shrink
    f.place(x=x, y=y)
    return f

def make_label(master, x, y, w, h, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0) # don't shrink
    f.place(x=x, y=y)
    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)
    return label

def make_button(master, x, y, w, h, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0) # don't shrink
    f.place(x=x, y=y)
    button = tk.Button(f, *args, **kwargs)
    button.pack(fill=tk.BOTH, expand=1)
    return button

def make_image(master, x, y, w, h, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0) # don't shrink
    f.place(x=x, y=y)
    img = tk.PhotoImage(f, *args, **kwargs)
    img.pack(fill=tk.BOTH, expand=1)
    return img

def make_comboBox(master, x, y, w, h, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0) # don't shrink
    f.place(x=x, y=y)
    cb = ttk.Combobox(f, *args, **kwargs)
    cb.pack(fill=tk.BOTH, expand=1)
    return cb

def resize_icon(file_path, w, h):
    image = Image.open(file_path)
    image = image.resize((w, h), Image.ANTIALIAS)
    return image

def clearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def startRecordDevice(method):
    #Declare device with your Device's MAC Address
    device = dev("00:07:80:4D:2E:9E")
    device.setModel(method)
    devFunction.exampleStart(device)

def changeFrame(frame, status_label, result_label):
    global checkFrame
    
    filename = 'mouse.txt'
    current_state = 'idle'
    idle_count = 0
    while checkFrame:
        file = open(filename, 'r')
        state = file.read()
        if  state != current_state:
            if state == 'left':
                idle_count = 0
                frame['bg'] = '#fc643a'
                status_label['text'] = 'Status : Clicked'
                result_label['text'] = 'Result : Left Click'
                current_state = 'left'
            elif state == 'right':
                idle_count = 0
                frame['bg'] = '#3ad5fc'
                status_label['text'] = 'Status : Clicked'
                result_label['text'] = 'Result : Right Click'
                current_state = 'right'
        else:
            idle_count += 1
        
        if idle_count == 5:
            frame['bg'] = '#ffd04f'
            status_label['text'] = 'Status : Idle'
            result_label['text'] = 'Result : - '
            idle_count = 0
            
        time.sleep(1)

def runCallBack(frame, status_label, result_label, button, graph_btn, method):
    global checkFrame
    
    frame['bg'] = '#ffd04f'
    status_label['text'] = 'Status : Idle'
    result_label['text'] = 'Result : - '
    
    button['text'] = 'Press Q to Stop'
    button['state'] = 'disabled'
    button['bg'] = '#d9d2d2'
    
    run_thread = threading.Thread(target=startRecordDevice, args=(method, ))
    run_thread.start()
    
    method_file = open('method.txt', 'w')
    method_file.write(method)
    method_file.close()
    
    def pressListener(key):
        if key.char == 'q':
            stopRunCallBack(frame, status_label, result_label, button, listener, graph_btn, method)
    checkFrame = True
    
    frame_thread = threading.Thread(target=changeFrame, args=(frame, status_label, result_label))
    frame_thread.start()
            
    listener = keyboard.Listener(on_press=pressListener)
    listener.start()
    
def stopRunCallBack(frame, status_label, result_label, button, listener, graph_btn, method):
    global checkFrame
    
    checkFrame = False
    frame['bg'] = '#f2f2f2'
    status_label['text'] = 'Status :'
    result_label['text'] = 'Result :'
    
    button['state'] = 'normal'
    button['text'] = 'Run'
    button['bg'] = '#6b84ff'
    button['command'] = lambda:runCallBack(frame, status_label, result_label, button, graph_btn, method)
    
    graph_btn['state'] = 'normal'
    graph_btn['bg'] = '#00d66e'
    
    mouse_file = open('mouse.txt', 'w')
    mouse_file.write('idle')
    mouse_file.close()

def showFrame(frame_list, selected):
    for frame in frame_list.items():
        if frame[0] == selected:
            continue
        clearFrame(frame[1])

def showGraph(frame, graph_btn):
    graph_img = ImageTk.PhotoImage(resize_icon('emg_signal.png', 612, 323))
    graph = make_label(frame, (GetSystemMetrics(0) - 250) / 2 - 300, (GetSystemMetrics(1) - 150) / 2 + 20,
               612, 323, text="Result : ", bg="#ffffff", fg="black", font="Bahnschrift 16 bold", anchor=tk.W,
               image=graph_img)
    graph.photo = graph_img
    
    graph_btn['text'] = 'Hide Graph'
    graph_btn['command'] = lambda:destroyGraph(frame, graph, graph_btn)

def destroyGraph(frame, graph, graph_btn):
    graph.pack_forget()
    make_frame(frame, (GetSystemMetrics(0) - 250) / 2 - 300, (GetSystemMetrics(1) - 150) / 2 + 20,
               612, 323, bg='#ffffff')
    
    graph_btn['text'] = 'Show Graph'
    graph_btn['command'] = lambda:showGraph(frame, graph_btn)
    

def createHomePage():
    global main_frame, home_button
    clearFrame(main_frame)
    main_frame = make_frame(window, 220, 60, GetSystemMetrics(0) - 250, GetSystemMetrics(1) - 150, bg="#ffffff")
    click_frame = make_frame(main_frame, (GetSystemMetrics(0) - 250) / 2 - 300, (GetSystemMetrics(1) - 150) / 2 - 400,
               600, 250, bg="#f2f2f2", highlightbackground="black", highlightthickness=0.5)
    make_frame(main_frame, (GetSystemMetrics(0) - 250) / 2 + 320, (GetSystemMetrics(1) - 150) / 2 - 400,
               50, 50, bg="#ffd04f")
    make_label(main_frame, (GetSystemMetrics(0) - 250) / 2 + 380, (GetSystemMetrics(1) - 150) / 2 - 400,
               200, 30, text="Idle / No Click", bg="#ffffff", fg="black", 
               font="Bahnschrift 14", anchor=tk.W)
    make_frame(main_frame, (GetSystemMetrics(0) - 250) / 2 + 320, (GetSystemMetrics(1) - 150) / 2 - 340,
               50, 50, bg="#fc643a")
    make_label(main_frame, (GetSystemMetrics(0) - 250) / 2 + 380, (GetSystemMetrics(1) - 150) / 2 - 340,
               200, 30, text="Left Click", bg="#ffffff", fg="black", 
               font="Bahnschrift 14", anchor=tk.W)
    make_frame(main_frame, (GetSystemMetrics(0) - 250) / 2 + 320, (GetSystemMetrics(1) - 150) / 2 - 280,
               50, 50, bg="#3ad5fc")
    make_label(main_frame, (GetSystemMetrics(0) - 250) / 2 + 380, (GetSystemMetrics(1) - 150) / 2 - 280,
               200, 30, text="Right Click", bg="#ffffff", fg="black", 
               font="Bahnschrift 14", anchor=tk.W)
    run_status = make_label(main_frame, (GetSystemMetrics(0) - 250) / 2 - 300, (GetSystemMetrics(1) - 150) / 2 - 130,
               200, 30, text="Status : ", bg="#ffffff", fg="black", 
               font="Bahnschrift 16 bold", anchor=tk.W)
    run_result = make_label(main_frame, (GetSystemMetrics(0) - 250) / 2 - 300, (GetSystemMetrics(1) - 150) / 2 - 80,
               200, 30, text="Result : ", bg="#ffffff", fg="black", 
               font="Bahnschrift 16 bold", anchor=tk.W)
    make_label(main_frame, (GetSystemMetrics(0) - 250) / 2 - 50, (GetSystemMetrics(1) - 150) / 2 - 130, 170, 30, text='Method',
            font="Bahnschrift 14", bg='#ffffff', anchor=tk.W)
    cb_method = make_comboBox(main_frame, (GetSystemMetrics(0) - 250) / 2 + 130, (GetSystemMetrics(1) - 150) / 2 - 130, 170, 30,
            font="Bahnschrift 14", state='readonly')
    cb_method['values'] = ('KNN', 'SVM')
    cb_method.current(0)
    graph_button = make_button(main_frame, (GetSystemMetrics(0) - 250) / 2 - 50, (GetSystemMetrics(1) - 150) / 2 - 90, 170, 50, text='Show Graph',
            font="Bahnschrift 14 bold", border=0, bg='#d9d2d2', compound=tk.CENTER,
            fg='#ffffff', activebackground='#018c49',
            state='disabled', command=lambda:showGraph(main_frame, graph_button))
    run_button = make_button(main_frame, (GetSystemMetrics(0) - 250) / 2 + 130, (GetSystemMetrics(1) - 150) / 2 - 90, 170, 50, text='Run',
            font="Bahnschrift 14 bold", border=0, bg='#6b84ff', compound=tk.CENTER,
            fg='#ffffff', activebackground='#3246a8', command=lambda:runCallBack(click_frame, run_status, run_result, run_button, graph_button, cb_method.get()))
    

def createAccuracyPage():
    global main_frame
    clearFrame(main_frame)
    main_frame = make_frame(window, 220, 60, GetSystemMetrics(0) - 250, GetSystemMetrics(1) - 150, bg="#ffffff")
    knn_table_frame = make_frame(main_frame, 10, 50, 200, 30, bg="#ffffff")
    table_list = [('Class', 'Precision', 'Recall', 'F1-Score'), ('Idle', 1.00, 1.00, 1.00),
              ('Left Click', 1.00, 1.00, 1.00), ('Right Click', 1.00, 1.00, 1.00)]
    total_rows = len(table_list)
    total_columns = len(table_list[0])
    
    make_label(main_frame, 10, 10, 200, 30, text="KNN Method", bg="#ffffff", fg="black", 
               font="Bahnschrift 14", anchor=tk.W)
    
    for i in range(total_rows):
        for j in range(total_columns):
            e = tk.Entry(knn_table_frame)
            e.grid(row=i, column=j)
            e.insert(tk.END, table_list[i][j])
            
    svm_table_frame = make_frame(main_frame, 10, 190, 200, 30, bg="#ffffff")        
    make_label(main_frame, 10, 150, 200, 30, text="SVM Method", bg="#ffffff", fg="black", 
               font="Bahnschrift 14", anchor=tk.W)
    
    for i in range(total_rows):
        for j in range(total_columns):
            e = tk.Entry(svm_table_frame)
            e.grid(row=i, column=j)
            e.insert(tk.END, table_list[i][j])


def createInformationPage():
    global main_frame
    clearFrame(main_frame)
    main_frame = make_frame(window, 220, 60, GetSystemMetrics(0) - 250, GetSystemMetrics(1) - 150, bg="#ffffff")
                            
    make_label(main_frame, 10, 10, 200, 30, text="How System Works ?", bg="#ffffff", fg="black", 
               font="Bahnschrift 16 bold", anchor=tk.W)
    img = ImageTk.PhotoImage(resize_icon('../Images/system_flow.jpg', 800, 80))
    system_img = make_label(main_frame, 10, 60, 800, 80, bg="#ffffff", fg="black", 
               font="Bahnschrift 14", anchor=tk.W, image=img)
    system_img.photo = img
    info_file = open('info.txt', 'r')
    make_label(main_frame, 10, 140, 870, 300, text=info_file.read(), bg="#ffffff", fg="black", 
               font="Bahnschrift 14", anchor=tk.CENTER, justify=tk.LEFT)
                            

window = tk.Tk()
window.title("Click Classification")
window.geometry(str(GetSystemMetrics(0)) + 'x' + str(GetSystemMetrics(1)))
window.configure(bg="#f2f2f2")

checkClick = False
run_button = tk.Button()
main_frame = make_frame(window, 220, 60, GetSystemMetrics(0) - 250, GetSystemMetrics(1) - 150, bg="#ffffff")
make_label(window, 0, 0, GetSystemMetrics(0), 50, text="Click Classification", 
           bg="#3246a8", fg="white", font="Corbel 16 bold", anchor=tk.W, padx=10)
           
make_frame(window, 0, 50, 200, GetSystemMetrics(1), bg="#ffffff")
           
home_icon = ImageTk.PhotoImage(resize_icon('../Images/home.png', 20, 20))
home_button = make_button(window, 0, 100, 200, 50, text=' Home', image=home_icon,
            font="Bahnschrift 14 bold", border=0, bg='white', compound=tk.LEFT,
            anchor=tk.W, padx=25, activebackground='#6b84ff',
            command=lambda:createHomePage()).pack(fill=tk.BOTH, expand=1)
            
accuracy_icon = ImageTk.PhotoImage(resize_icon('../Images/acc.png', 30, 30))
accuracy_button = make_button(window, 0, 170, 200, 50, text='Accuracy', image=accuracy_icon,
            font="Bahnschrift 14 bold", border=0, bg='white', compound=tk.LEFT,
            anchor=tk.W, padx=20, activebackground='#6b84ff',
            command=lambda:createAccuracyPage()).pack(fill=tk.BOTH, expand=1)
            
lamp_icon = ImageTk.PhotoImage(resize_icon('../Images/lamp.jpg', 30, 30))
info_button = make_button(window, 0, 240, 200, 50, text='Information', image=lamp_icon,
            font="Bahnschrift 14 bold", border=0, bg='white', compound=tk.LEFT,
            anchor=tk.W, padx=20, activebackground='#6b84ff',
            command=lambda:createInformationPage())

star_icon = ImageTk.PhotoImage(resize_icon('../Images/star.png', 20, 20))
credit_button = make_button(window, 0, 310, 200, 50, text='Credit', image=star_icon,
            font="Bahnschrift 14 bold", border=0, bg='white', compound=tk.LEFT,
            anchor=tk.W, padx=25, activebackground='#6b84ff').pack(fill=tk.BOTH, expand=1)
            
createHomePage()
window.mainloop()