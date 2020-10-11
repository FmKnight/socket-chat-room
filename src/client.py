from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, messagebox 
import socket 
import threading 
from settings import Local_Host,Local_Port



class ChatClient:

    client_socket = None
    last_received_message = None

    def __init__(self):
        self.initialize_socket()
        self.listen_for_incoming_messages_in_a_thread()    #监听消息

        
    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 初始化socket :TCP、IPV4
        remote_ip = Local_Host # IP地址
        remote_port = Local_Port #TCP 端口
        self.client_socket.connect((remote_ip, remote_port)) #连接远程服务端

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))  
        thread.start()
    
    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode('utf-8')
            #判断发送消息的是否为新的客户端连接
            if "joined" in message:
                user = message.split(":")[1]
                message = user + " has joined"
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
            else:
                self.chat_transcript_area.insert('end', message + '\n')
                self.chat_transcript_area.yview(END)
        so.close()




class GUI:
    
    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.password_widget = None
        self.enter_text_widget = None
        self.join_button = None
        self.initialize_gui()                 #图形化界面
        self.chat_client = ChatClient()
        self.chat_client.listen_for_incoming_messages_in_a_thread()
        

    def login(self,so):
        message = (self.name_widget.get()+'-'+self.password_widget.get()).encode('utf-8')
        so.send(message)

    def initialize_gui(self): # GUI 初始化
        self.root.title("北落师门聊天室")
        self.root.iconbitmap(r"E:\生活\Photo\图标\fm-4(32X32).ico") 
        self.root.resizable(0, 0)  #固定窗口大小
        self.display_chat_box()
        self.display_name_section()
        self.display_chat_entry_box()


    def display_name_section(self):
        frame = Frame()
        Label(frame, text='昵称:', font=("Serif", 12)).pack(side='left', padx=20)
        self.name_widget = Entry(frame, width=30, borderwidth=2)
        self.name_widget.pack(side='left', anchor='e')      
        Label(frame, text='密码:', font=("Serif", 12)).pack(side='left', padx=5)
        self.password_widget = Entry(frame,width=20,borderwidth=2,show="*")
        self.password_widget.pack(side='left',anchor='e')
        self.join_button = Button(frame,text="加入群聊", width=10, command=self.on_join)
        self.join_button.pack(side='left',padx=5)
        frame.pack(side='top', anchor='n')

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text='聊天区', font=("Serif", 12)).pack(side='left', anchor='w',padx=15)
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12),borderwidth=2)
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL) 
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        #设置聊天区消息不可修改
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')  
        self.chat_transcript_area.pack(side='left', padx=5,pady=5)
        scrollbar.pack(side='left', fill='y')
        frame.pack(side='top',anchor='n')

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='请输入需要发送的消息:', font=("Serif", 12)).pack(side='top', anchor='w',pady=5)
        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12),borderwidth=2)
        self.enter_text_widget.pack(side='left',pady=5)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def input_empty(self):
        #发送消息前需先加入群聊
        if len(self.name_widget.get()) == 0 or len(self.password_widget.get()) == 0:
            messagebox.showerror("输入错误", "昵称或密码为空，请重新输入！")
            return
    def on_join(self):
        self.input_empty()
        #确定昵称后不可修改
        self.name_widget.config(state='disabled')
        self.password_widget.config(state='disabled')
        self.join_button.config(state='disabled')
        self.chat_client.initialize_socket()
        self.login(self.chat_client.client_socket)
        self.chat_client.client_socket.send(("joined:" + self.name_widget.get()).encode('utf-8'))

    def on_enter_key_pressed(self, event):
        self.input_empty()
        self.send_chat()
        self.clear_text()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')

    def send_chat(self):
        senders_name = self.name_widget.get().strip() + ": "
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (senders_name + data).encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n')
        self.chat_transcript_area.yview(END)
        self.chat_client.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def on_close_window(self):
        if messagebox.askokcancel("退出", "确定退出吗?"):
            self.root.destroy()
            self.chat_client.client_socket.close()
            exit(0)


if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()
