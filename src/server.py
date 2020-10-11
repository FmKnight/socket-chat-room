# -*- coding: UTF-8 -*-
import socket 
import threading
from settings import Local_Host,Local_Port


db = {
    'bob':'23456',
    'bb':'1',
    'cc':'1',
}   

class ChatServer:

    clients_list = []     #客户端列表
    last_received_message = ""  #接收的最新请求

    def __init__(self):
        self.server_socket = None
        self.create_listening_server()

    def create_listening_server(self):    
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #创建套接字
        local_ip = Local_Host
        local_port = Local_Port
        #此处为socket设置选项，参数"1",表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，
        # 否则操作系统会保留几分钟该端口。
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((local_ip, local_port))  #绑定ip与端口
        print("Listening for incoming messages..")
        self.server_socket.listen(5) #允许有多少个未决（等待）的连接在队列中等待，一般设置为5。
        self.receive_messages_in_a_new_thread()
    #接受消息并广播
    def authenticate(self,so):
        buffer = so.recv(256)
        if not buffer:
            return False
        login_msg = buffer.decode('utf-8')
        username,password = login_msg.split('-')
        if username in db and password==db.get(username):
            return True


    def receive_messages(self, so,client):
        if not self.authenticate(so):
            self.clients_list.remove(client)
            so.close()
            return 
        while True:
            try:
                incoming_buffer = so.recv(256) 
            except:
                print()
                break
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            self.broadcast_to_all_clients(so)  
        self.clients_list.remove(client)
        so.close()
        
    #将消息广播给全体客户端
    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode('utf-8'))

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list(client)
            print('There is a connection request from', ip, ':', str(port))
            #利用多线程，可同时处理多个客户端请求
            t = threading.Thread(target=self.receive_messages, args=(so,client))
            t.start()
    #新增客户端
    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)


if __name__ == "__main__":
    ChatServer()
