import socket
import user
import time
from queue import Queue
import threading
import sys
from tkinter import END

class client:
    def __init__(self,myuser,friendname):
        self.myuser=myuser
        self.friendname = friendname
        self.sendMsgQueue=Queue()
        self.recvMsgQueue=Queue()
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host='111.67.199.68'
        self.port=2333



    def connect_service(self):
        self.s.connect((self.host,self.port))
        self.s.send(self.myuser.getnickname().encode())#连接成功后将连接者昵称发送至服务器
        #print(self.s.recv(1024).decode())

    def add_sendmsg_to_queue(self,msg,senduser,recvuser):
        message=msg
        if not message:
            print('消息不能为空')
            return -1
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        msg = 'message'+'/'+ senduser.getnickname() +'/'+recvuser+ '/' + t + '/' + message
        print(msg)
        self.sendMsgQueue.put(msg)
        print(self.sendMsgQueue.qsize())



    #消息格式：
    #           message/192.168.1.119/testname/2019-08-12 15:25:37/都看过就欧弟郭德纲
    def sendMsg(self):
        while True:
            if self.sendMsgQueue.empty():
                time.sleep(1)
            else:
                #print('大小：',self.sendMsgQueue.qsize())
                self.s.send(self.sendMsgQueue.get().encode())

    def add_recvmsg_to_queue(self):
        print('++++')
        while True:

            #print('conn:',c['conn'])
            recvmsg = self.s.recv(1024).decode()
            if recvmsg.split('/')[0]=='message':#只接受message类型消息到接收队列
                self.recvMsgQueue.put(recvmsg)
            #print('recv队列大小：',self.recvMsgQueue.qsize())

    def recvMsg(self):
        #while True:
        if self.recvMsgQueue.empty():
            print('接受队列为空hhhh')
            return -1
        else:
            # print('接受队列大小：',self.recvMsgQueue.qsize())
            msg = self.recvMsgQueue.get().split('/')
            # print(msg)
            #print(msg[0] + '\n' + msg[1] + '\t' + msg[2] + '\n' + msg[3] + '：\t' + msg[4])
            #message=msg[0] + '\n' + msg[1] + '\t' + msg[2] + '\n' + msg[3] + '：\t' + msg[4]
            return msg


    def close_connect(self):#断开socket连接
        msg='closeconnect/'
        self.s.send(msg.encode())
        self.s.close()
        print('断开连接，程序已退出！！！')
        #sys.exit()

    def connectandaddmsgtoqueue(self):
        self.connect_service()
        # 添加消息到接收消息队列
        addrecvmsgthread = threading.Thread(target=self.add_recvmsg_to_queue)
        addrecvmsgthread.start()
        # 发送消息线程
        sendmsgthread = threading.Thread(target=self.sendMsg)
        sendmsgthread.start()

    def run(self):
        pass
        #nickname = '用户1'
        #self.usertest = user.user(nickname)
        #self.connect_service()
        #发送消息线程
        #sendmsgthread=threading.Thread(target=self.sendMsg)
        #sendmsgthread.start()
        # 接收消息线程
        #recvmsgthread = threading.Thread(target=self.recvMsg)
        #recvmsgthread.start()
        #添加消息到发送消息队列
        #addmsgthread = threading.Thread(target=self.add_sendmsg_to_queue,args=(self.chattingtouser,))
        #addmsgthread.start()
        # 添加消息到接收消息队列
        #addrecvmsgthread = threading.Thread(target=self.add_recvmsg_to_queue)
        #addrecvmsgthread.start()
        #time.sleep(10)
        #self.close_connect()

