# -*- coding: UTF-8 -*-
import socket
from queue import Queue
from time import sleep
import threading


class service:
    def __init__(self):
        self.sendMsgQueue = Queue()
        self.recvMsgQueue = Queue()
        self.connect_info=[]
        self.accept_connect=[]
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host='111.67.199.68'
        self.port=2333


    def accept_request(self):
        self.s.bind((self.host, self.port))
        self.s.listen(50)
        while True:
            print('正在等待连接。。。')
            conn = self.s.accept()
            nickname=conn[0].recv(1024).decode()#连接成功先将用户昵称接收
            #print('nick:',nickname)
            self.accept_connect.append(conn)
            self.accept_connect.append(nickname)
            print(self.accept_connect)

            #self.connect_info.append('connectinfo'+'/'+str(conn[1][0])+'/'+str(conn[1][1])+'/'+nickname)
            #print(self.connect_info)
            #格式：
            #    connectinfo/192.168.29.1/4318/袅袅兮秋风
            for info in self.connect_info:#发送当前连接服务气的所有ip 端口 昵称
                conn[0].send(info.encode())
            #print(conn[0])
            #print(conn[1])
            print('连接成功')

    def sendMsg(self):
        while True:
            if self.sendMsgQueue.empty():
                #print('发送消息队列为空！！！')
                sleep(1)

            else:
                #print('大小：', self.sendMsgQueue.qsize())

                #print('555555555555555',len(self.accept_connect))
                flag=False
                length=int(len(self.accept_connect)/2)
                #print('length',length)
                msg=self.sendMsgQueue.get()
                for i in range(0,int(len(self.accept_connect)/2)):

                    #print(self.accept_connect)
                    #print('等待发送。。。',i)
                    name1=self.accept_connect[int(i*2+1)]
                    name2=msg.split('/')[2]
                    if name1==name2:
                        #print('找到收件人',i)
                        self.accept_connect[int(i*2)][0].send(msg.encode())
                        #print('转发成功？',i)
                        flag=True
                        break
                if flag==False:
                    print('未找到该用户！！！')
                    self.sendMsgQueue.put(msg)
                    sleep(1)



    def add_recvmsg_to_queue(self,conn):
        print('++++',conn)
        thread = [0]*100
        flag=[0]*100
        for j in range(0,100):
            flag[j]=True
        while True:
            i = 0
            #print('cccconn:',conn)
            for k in range(0,len(self.accept_connect)):
                if i%2!=0:
                    i=i+1
                    continue
                #print('conn:',c['conn'])
                if flag[int(i/2)]==True:
                    #print('鹅鹅鹅鹅鹅鹅饿')
                    #print(self.accept_connect)
                    thread[int(i/2)]=threading.Thread(target=self.recvthread,args=(self.accept_connect[i],))
                    thread[int(i/2)].start()
                    flag[int(i/2)] =False
                if not thread[int(i/2)].isAlive():
                    flag[int(i/2)]=True
                '''recvmsg = c[0].recv(1024).decode()
                print('调试：',i)
                if recvmsg.split('/')[0]=='message':#只接受message类型消息到接收队列
                    self.recvMsgQueue.put(recvmsg)
                    self.sendMsgQueue.put(recvmsg)'''
                i=i+1

            #print('recv队列大小：',self.recvMsgQueue.qsize())
    def recvthread(self,c):
        recvmsg = c[0].recv(1024).decode()
        if recvmsg.split('/')[0] == 'message':  # 只接受message类型消息到接收队列
            self.recvMsgQueue.put(recvmsg)
            self.sendMsgQueue.put(recvmsg)
        elif recvmsg.split('/')[0] == 'closeconnect':#断开连接，从self.connect中删除此连接
            for i in range(0,len(self.accept_connect)):
                if self.accept_connect[i][0]==c[0]:
                    a=self.accept_connect.pop(i)
                    b=self.accept_connect.pop(i)
                    print(a,b)
                    print(i,self.accept_connect)
                    print('删除成功')
                    break

    def recvMsg(self):
        print('--------')
        while True:
            if self.recvMsgQueue.empty():
                sleep(1)
            else:
                #print('接受队列大小：',self.recvMsgQueue.qsize())
                msg=self.recvMsgQueue.get().split('/')
                #print(msg)
                print(msg[0]+'\n'+msg[1]+'\t'+msg[2]+'\n'+msg[3]+'：\t'+msg[4])




    def run(self):
        #接受连接线程
        acceptrequestthread=threading.Thread(target=self.accept_request)
        # 接收消息线程
        recvmsgthread = threading.Thread(target=self.recvMsg)
        # 添加消息到发送消息队列
        addmsgthread = threading.Thread(target=self.add_recvmsg_to_queue, args=(self.accept_connect,))
        # 发送消息线程
        sendmsgthread = threading.Thread(target=self.sendMsg)

        acceptrequestthread.start()

        recvmsgthread.start()
        sendmsgthread.start()

        addmsgthread.start()

if __name__ == '__main__':
    client1=service()
    client1.run()


