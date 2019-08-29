import socket



class user:
    def __init__(self,nickname='null'):
        self.ip=self.get_host_ip()
        self.nickname=nickname#自己的昵称
        self.friends=[]#存储好友信息
        #self.friends=[0]*100
    def add_friend(self):
        print(self.ip,self.nickname)
    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            self.ip = s.getsockname()[0]
        finally:
            s.close()

        return self.ip
    def getip(self):
        return self.ip
    def getnickname(self):
        return self.nickname


