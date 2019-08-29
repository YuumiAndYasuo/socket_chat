from tkinter import Tk,Canvas,Button,Entry,Checkbutton,Label,PhotoImage,NW,END,scrolledtext,BooleanVar,StringVar,messagebox
from PIL import Image,ImageTk
from threading import Thread
from time import strftime,sleep,time,localtime
import pymysql
import c
import user

#登陆类
class LoginPanel:
    def __init__(self):

#图形界面区域
        self.root = Tk()
        self.root.title('登陆0.0.1')
        self.root.geometry('450x350+400+200')

        #头像区域
        self.head = Canvas(self.root)
        #self.head.create_oval(165, 15, 265, 115)
        self.head.place(x=5, y=5, heigh=120, width=440)



        #输入区域
        self.input = Canvas(self.root, bg='#ffffff')
        self.input.place(x=5, y=130, heigh=220, width=440)

        #登陆按钮
        self.loginbutton=Button(self.input,text='登陆',bg='#4fcffd',command=self.loginbuttonclickevent)
        self.loginbutton.place(x=100,y=160,heigh=40, width=240)

        #账号输入框
        self.accountinput=Entry(self.input,font=("仿宋", 16, "bold"))
        self.accountinput.place(x=130,y=60,heigh=30,width=210,)

        #密码输入框
        self.passwordinput = Entry(self.input,font=("仿宋", 16, "bold"),show='*')
        self.passwordinput.place(x=130, y=95, heigh=30, width=210)

        #自动登录checkbutton
        self.autologinvar=BooleanVar()
        self.autologincheck=Checkbutton(self.input,text='自动登录',variable=self.autologinvar,command=self.autologincheckbuttonstatusevent)
        self.autologincheck.place(x=100, y=130, heigh=15, width=80)

        #记住密码
        self.remberpasswordvar=BooleanVar()
        self.remberpasswordcheck = Checkbutton(self.input, text='记住密码',variable=self.remberpasswordvar,command=self.remberpasswordcheckbuttonstatusevent)
        self.remberpasswordcheck.place(x=190, y=130, heigh=15, width=80)

        #找回密码
        self.findpasswordbutton=Button(self.input,text='找回密码',bg='white')
        self.findpasswordbutton.place(x=290, y=130, heigh=15, width=50)

        #注册账号
        self.registerbutton=Button(self.input,text='注册账号',bg='white',command=self.registerbuttonclickevent)
        self.registerbutton.place(x=10, y=190, heigh=15, width=50)


#准备工作
        #1、获取复选框状态（自动登录，记住密码）

        #2、如果自动登录已勾选，获取最近一次登录账号及对应密码输入框并直接登录，摧毁当前窗口，打开主界面窗口，
        #3、如果仅勾选记住密码，则仅获取最近一次登录账号及对应密码输入框，等待用户操作


#对应事件监听区域

    #登录按钮点击事件
    def loginbuttonclickevent(self):
        account = self.accountinput.get().strip().replace(' ', '')
        self.accountinput.delete(0, END)
        self.accountinput.insert(END, account)
        print(account)
        password = self.passwordinput.get().strip().replace(' ', '')
        self.passwordinput.delete(0, END)
        self.passwordinput.insert(END, password)
        print(password)
        if len(account) < 8 or len(password) < 8 or not account.isdigit():
            messagebox.showinfo('登录失败', '查无此号')
            return -1
        for c in password:
            if ord(c) > 255:
                messagebox.showinfo('登录失败', '密码错误\n( ⊙ o ⊙ )')
                return -2

        print('等待连接数据库。。。')
        db = pymysql.connect('localhost', 'root', '123456', 'database1')
        cursor = db.cursor()
        print('连接成功')
        sql = "select pwd,nickname from user_info where id=%s"%account
        # print('sql',sql)
        # cursor.execute("select * from user_info")
        try:
            cursor.execute(sql)
            results=cursor.fetchall()[0]
            print('results',results)
            if results[0]==password:
                messagebox.showinfo('登录成功','登录成功')
                db.close()
                self.root.destroy()
                mainpanel=MainPanel(results[1])
                mainpanel.run()
                return 0
            messagebox.showinfo('登录失败','账号密码不匹配')
        except:
            print('登录抛出异常')
            db.rollback()
        db.close()
        return -3
        #登录操作


        #登录成功，自动保存账号，并根据记住密码复选框状态决定是否保存密码


    #自动登录勾选事件
    def autologincheckbuttonstatusevent(self):
        print('自动登录状态：',self.autologinvar.get())
        #如果为自动登录状态，则记住密码为勾选状态
        if self.autologinvar.get()==True:
            self.remberpasswordvar.set(True)


    #记住密码勾选事件
    def remberpasswordcheckbuttonstatusevent(self):
        print('记住密码状态：',self.remberpasswordvar.get())


    #注册账号按钮点击事件（未完成）
    def registerbuttonclickevent(self):
        register = RegisterPanel()
        register.run()


    #找回密码按钮点击事件（未完成）
    def findpasswordbuttonclickevent(self):
        pass

    def run(self):
        self.root.mainloop()

    pass


class MainPanel:
    def __init__(self,loginnickname):
        self.myuser=user.user(loginnickname)


        self.root=Tk()
        self.root.title('聊天主界面0.0.1')
        self.root.geometry('350x600+400+50')

        #个人信息区域
        self.head=Canvas(self.root,bg='orange')
        self.head.create_oval(30,30,80,80)
        self.head.place(x=5,y=5,heigh=120,width=340)

        #好友区域
        self.frend = Canvas(self.root, bg='pink')
        self.frend.place(x=5, y=130, heigh=420, width=340)

        #设置区域
        self.setting = Canvas(self.root, bg='yellow')
        self.setting.place(x=5, y=555, heigh=40, width=340)

        #好友栏
        self.frendstext=scrolledtext.ScrolledText(self.frend)
        self.frendstext.place(x=5,y=5,heigh=410,width=330)

        #自己的昵称名标签
        self.myselfnicknamelable=Label(self.head,text=self.myuser.getnickname())
        self.myselfnicknamelable.place(x=100,y=30)

        friendnum=10
        for i in range(friendnum):
            Thread(target=self.friendbuttonthread,args=('用户'+str(i+1),)).start()


    #绑定对应好友事件
    def friendbuttonthread(self,friendname):
        friendbutton=Button(self.frendstext,text=friendname,bg='#ecf3d8',heigh=2,width=44,command=lambda:self.friendsbuttonclickevent(friendname))
        self.frendstext.window_create(END, window=friendbutton)

    #监听事件

    #好友按钮点击事件
    def friendsbuttonclickevent(self,friendname):
        print(friendname)

        self.client=c.client(self.myuser,friendname)
        #Thread(target=ChatPanel(self.myuser,friendname,self.client).run).start()
        print('66666666666666')
        Thread(target=self.client.connectandaddmsgtoqueue).start()
        print('77777777777777')
        ChatPanel(self.myuser, friendname, self.client).run()
        print('88888888888888')


    #连接数据库，获取好友列表
    #每个用户建立一个数据库
        #好友信息table    昵称    账号     其他（待补充）
    def getmyfriendsinfo(self):
        pass


    def run(self):
        self.root.mainloop()



class ChatPanel:
    def __init__(self,myuser,frienduser,client):
        self.client=client
        self.root = Tk()
        self.frienduser=frienduser#暂时未用户名， 不是user对像！！！！！！！
        self.myuser = myuser
        self.root.title('登录用户: '+self.myuser.getnickname())
        self.root.geometry('700x600+400+50')
        #标题
        self.headtitle = Canvas(self.root, bg='yellow')
        self.headtitle.place(x=5, y=5, heigh=40, width=690)

        #好友名字标签
        titlenamelable=Label(self.headtitle,text=self.frienduser)
        titlenamelable.place(x=200,y=5, heigh=30, width=300)
        #聊天信息
        self.chattext = Canvas(self.root, bg='orange')
        self.chattext.place(x=5, y=45, heigh=400, width=490)
        #输入区域
        self.input = Canvas(self.root, bg='pink')
        self.input.place(x=5, y=445, heigh=150, width=490)
        #好友信息区域
        self.info = Canvas(self.root, bg='#d9ffb3')
        self.info.place(x=495, y=45, heigh=550, width=200)


        #发送按钮
        closebutton=Button(self.input,text='发送',command=self.sendbuttonclickevent)
        closebutton.place(x=400, y=110, heigh=30, width=80)
        #关闭按钮
        closebutton=Button(self.input,text='关闭',command=self.closebuttonclickevent)
        closebutton.place(x=310, y=110, heigh=30, width=80)

        #聊天信息框
        self.chattextvar=StringVar
        self.chatscrolltext=scrolledtext.ScrolledText(self.chattext,font=("仿宋", 16, "normal"))
        self.chatscrolltext.place(x=5,y=5,heigh=390,width=480)

        # 信息输入框
        self.inputchattext = scrolledtext.ScrolledText(self.input, font=("仿宋", 16, "normal"))
        self.inputchattext.place(x=5, y=5, heigh=100, width=480)



#绑定事件区域
    def sendbuttonclickevent(self):

        #获取输入信息
        t = strftime("%Y-%m-%d %H:%M:%S", localtime(time()))
        msg=self.inputchattext.get('0.0',END)
        self.inputchattext.delete('0.0',END)
        print(msg)
        #将消息加入发送消息队列
        self.client.add_sendmsg_to_queue(msg,self.myuser,self.frienduser)

        #将输入信息追加到聊天记录中

        self.chatscrolltext.insert(END,t+'\n'+self.myuser.getnickname()+'\t:'+msg)
        print('发送按钮被点击了')

    def closebuttonclickevent(self):
        print('关闭按钮被点击了')
        self.closewindow()


    def closewindow(self):
        self.client.close_connect()
        self.root.destroy()

    def recvthread(self):
        while  True:
            msg=self.client.recvMsg()
            if msg==-1:
                sleep(1)
                continue
            print('mmmsg',msg)
            self.chatscrolltext.insert(END, msg[3] + '\n' + msg[1] + '\t：' + msg[4])
            print('插入成功')
    def run(self):
        # 接收消息线程
        #Thread(target=self.client.recvMsg,args=(self.chatscrolltext,)).start()
        #self.root.mainloop()

        Thread(target=self.recvthread).start()
        print('ssssssssssssssssssssss')
        self.root.mainloop()

        #Thread(target=self.root.mainloop).start()


class RegisterPanel:
    def __init__(self):
        self.root = Tk()
        self.root.title('注册0.0.1')
        self.root.geometry('450x350+400+200')


        # 输入区域
        self.input = Canvas(self.root, bg='#ffffff')
        self.input.place(x=5, y=130, heigh=220, width=440)

        # 注册按钮
        self.loginbutton = Button(self.input, text='立即注册', bg='#4fcffd', command=self.registerbuttonclickevent)
        self.loginbutton.place(x=100, y=160, heigh=40, width=240)

        # 昵称输入框
        self.nicknameinput = Entry(self.input, font=("仿宋", 16, "bold"))
        self.nicknameinput.place(x=130, y=20, heigh=30, width=210, )


        # 账号输入框
        self.accountinput = Entry(self.input, font=("仿宋", 16, "bold"))
        self.accountinput.place(x=130, y=60, heigh=30, width=210, )

        # 密码输入框
        self.passwordinput = Entry(self.input, font=("仿宋", 16, "bold"), show='*')
        self.passwordinput.place(x=130, y=95, heigh=30, width=210)


    def registerbuttonclickevent(self):
        nickname=self.nicknameinput.get().strip().replace(' ','')
        self.nicknameinput.delete(0, END)
        self.nicknameinput.insert(END, nickname)
        print(nickname)
        account=self.accountinput.get().strip().replace(' ','')
        self.accountinput.delete(0,END)
        self.accountinput.insert(END,account)
        print(account)
        password=self.passwordinput.get().strip().replace(' ','')
        self.passwordinput.delete(0,END)
        self.passwordinput.insert(END,password)
        print(password)
        if len(account)<8 or len(password)<8 :
            messagebox.showinfo('注册失败','账号或密码过短\no(︶︿︶)o')
            return -1
        if not account.isdigit():
            messagebox.showinfo('注册失败','账号必须全为数字\n(╯﹏╰）')
            return -2
        for c in password:
            if ord(c)>255:
                messagebox.showinfo('注册失败','密码不能包含非法字符\n( ⊙ o ⊙ )')
                return -3

        print('等待连接数据库。。。')
        db=pymysql.connect('localhost','root','123456','database1')
        cursor=db.cursor()
        print('连接成功')
        sql="insert into user_info(id,nickname,pwd)value('%s','%s','%s')"%(account,nickname,password)
        #print('sql',sql)
        #cursor.execute("select * from user_info")
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()
        messagebox.showinfo('注册成功','恭喜您 注册成功\n~\(≧▽≦)/~')
        return 0

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    loginpanel = LoginPanel()
    loginpanel.run()

    #mainpanel=MainPanel()
    #mainpanel.run()

    #chatpanel=ChatPanel()
    #chatpanel.run()

    #register=RegisterPanel()
    #register.run()
