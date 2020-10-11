


# socket(TCP)多线程图形化界面聊天室实例

## 概述
使用python自带的GUI库tkinter，以及多线程模块threading，实现socket(tcp)多线程图形界面聊天室。


## 实现

两个py文件，一个服务端server.py,一个客户端client.py,图形化界面放在了客户端。

## 使用

1、运行server.py,服务端启动，创建套接字并监听消息。
2、运行client.py，弹出图形化界面，输入用户名以及密码，加入聊天室。(可同时运行多个实例)

## 说明

运行服务端代码，服务正在监听等待请求消息：

![服务端监听](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/1.png)


运行客户端代码client.py，可以看到服务端显示有客户端请求：

![显示客户端请求](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/3.png)

此时客户端部分，桌面会弹出一个新的页面，如下所示：

![图形化界面](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/2.png)

图形化界面主要包含三个部分：

*   聊天区：用于展示(多个)客户端发送的请求消息
*   用户信息区：用户的昵称、密码，点击加入群聊，服务端进行身份验证，通过后，可以开始聊天。
*   消息编写发送区：键入需要发送的消息，回车发送。

键入昵称与密码后，服务端会进行身份验证，主要是通过将昵称与密码结合成字符串，发送至服务端，服务端将其与自身保存的用户字典中的用户进行匹配。

若在字典中，则验证通过，服务器端显示成功连接：

![连接成功](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/4.png)

此时客户端的昵称、密码输入框以及加入群聊按钮都被禁用，即不允许再修改身份：

![禁用按钮](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/5.png)

若身份验证失败，则服务端显示身份验证失败，断开连接：

![验证失败，断开连接](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/6.png)

此时客户端弹出身份验证失败提示框：

![](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/7.png)

当新的客户端加入聊天室时，聊天区会展示该用户已加入群聊(has joined）。在三个客户端分别键入消息并发送，其结果如下：

![运行结果](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/8.png)

此处需要注意的几个地方：

*   通过tkinter的事件绑定，昵称、密码输入后，点击“加入群聊”按钮，输入框状态修改为"disabled",即无法再修改身份信息。
*   聊天区也绑定了事件<KeyPress>，即聊天区消息无法通过键盘输入或修改。

![无法修改身份](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/9.png)

*   当未输入昵称或密码，直接点击“加入群聊按钮”，或者尝试在消息区编写发送消息，系统会弹出提示框，提醒用户先进行登录。

![输入提示](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/10.png)

## 远程服务器测试

进行远程服务器测试步骤：        
1、将用于socket通信的远程服务器的端口打开，注意是**出方向**和**入方向**同时打开。

![服务器端口设置](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/11.png)

2、将远程服务器ip绑定为"0.0.0.0",即允许监听所有端口。
![远程测试端口](https://github.com/FmKnight/socket_chat_room/blob/master/socket-image/12.png)

设置后，客户端与服务端即可正常通信。

# Reference

[1] [https://www.liujiangblog.com/course/python/76](https://www.liujiangblog.com/course/python/76)

[2][http://c.biancheng.net/cpp/socket/](http://c.biancheng.net/cpp/socket/)