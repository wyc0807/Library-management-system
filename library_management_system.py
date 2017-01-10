# -*- coding: utf-8 -*-		//注意：路径有中文用sublime无法运行！！！！！
from tkinter import *
from tkinter import ttk
import Pmw
import sqlite3
import time

conn=sqlite3.connect("library.db")	#连接数据库
c=conn.cursor()

class Application(Frame):
	def __init__(self,master=None):
		Frame.__init__(self, master)
		self.pack()
		self.set_panel()
		Pmw.initialise(root)		
	
	#主界面
	def set_panel(self):
		global enter_ID,enter_password
		self.logo = PhotoImage(file="01.png")
		panel=Label(root,image=self.logo)
		w = self.logo.width()
		h = self.logo.height()
		root.geometry("%dx%d+0+0" % (w, h))
		root.iconbitmap('icon.ico')
		panel.pack(side='top', fill='both', expand='yes')
		tip = Label(panel,text='请输入ID和密码并选择:',font='YaHei 13 bold').place(x=350,y=160)
		ID_tip=Label(panel,text='ID:').place(x=325,y=230)
		enter_ID = Entry(panel)
		enter_ID.place(x=370,y=230,width=180,height=25)
		password_tip=ttk.Label(panel,text='密码:').place(x=320,y=280)
		enter_password = Entry(panel)
		enter_password.place(x=370,y=280,width=180,height=25)
		enter_password['show']='●'
		stu_button = ttk.Button(root,text='读者',command=self.stu_button_click).place(x=340,y=340)#,fg='#a1dbcd',bg='#383a39'#.pack(side="left",padx=50,ipadx=50,anchor='n')
		admin_button = ttk.Button(root,text='管理员',command=self.admin_button_click).place(x=470,y=340)#,fg='#a1dbcd',bg='#383a39'#.pack(side="right",padx=50,ipadx=50,anchor='n')	#主界面
	
	 #读者界面
	def stu_button_click(self):  
		global stu
		global query
		global dropdown
		global name,reader_ID
		if (enter_ID.get()=='')or(enter_password.get()==''):	#某一个输入框为空,.get()函数用于获取输入框输入的字符串
			exe=Toplevel()
			Label(exe,text='ID或密码错误！').pack()
			ttk.Button(exe,text='返回',command=exe.withdraw).pack()
			return
		c.execute("SELECT ID,password FROM readers WHERE ID=? AND password=? ",(enter_ID.get(),enter_password.get()))
		x=c.fetchall()
		if(x==[]):
			exe=Toplevel()
			Label(exe,text='ID或密码错误！').pack()
			ttk.Button(exe,text='返回',command=exe.withdraw).pack()
			return
		c.execute("SELECT ID,name FROM readers WHERE ID=?",(enter_ID.get(),))
		m=c.fetchall()
		reader_ID=m[0][0]
		name=m[0][1]

		stu=Toplevel()
		stu.geometry('1300x700')
		stu.title("%s     %s" % (enter_ID.get(),name))
		self.logo3=PhotoImage(file="02.png")
		image_lable=Label(stu,image=self.logo3).pack(side="top")
		tip=Label(stu,text='请选择查询方式并输入:',font='KaiTi 20 bold',bg='light blue').place(x=500,y=150)		
		query = Entry(stu)   #query为读者的输入框
		query.place(x=400,y=220,width=500,height=30)
		query_button = ttk.Button(stu,text='查询',style='C.TButton',command=self.stu_query_click).place(x=917,y=217,width=70,height=36)		
		admin_items = ('书名','索书号','作者','出版社')
		dropdown = Pmw.ComboBox(stu,label_text='查询条件',labelpos='nw',scrolledlist_items = admin_items,)   #读者查询的下拉选择菜单选择查询方式
		dropdown.place(x=285,y=205,width=100)
		first = admin_items[0]
		dropdown.selectitem(first)

	#读者界面的查询
	def stu_query_click(self):
		table=Toplevel()                        #新面板
		table.title('读者查询')
		tree=ttk.Treeview(table,columns=('col1','col2','col3','col4','col5','col6','col7','col8'))   #Treeview创建表格
		tree.column('col1', width=100, anchor='w')  
		tree.column('col2', width=200, anchor='w')
		tree.column('col3', width=150, anchor='w')
		tree.column('col4', width=200, anchor='w')
		tree.column('col5', width=300, anchor='w')
		tree.column('col6', width=100, anchor='center')
		tree.column('col7', width=50, anchor='center')
		tree.column('col8', width=50, anchor='center')
		tree.heading('col1', text='ISBN')
		tree.heading('col2', text='书名')
		tree.heading('col3', text='索书号')
		tree.heading('col4', text='作者')
		tree.heading('col5', text='出版社')
		tree.heading('col6', text='馆藏地')
		tree.heading('col7', text='可借量')
		tree.heading('col8', text='借出量')
		if dropdown.get()=='书名':                             #查询
			s1='%'+query.get()+'%'
			for x in c.execute("SELECT * FROM bookinfo WHERE title LIKE ? ORDER BY title DESC",(s1,)):
				tree.insert('',0,values=(x))
		elif dropdown.get()=='作者':
			s2='%'+query.get()+'%'
			for x in c.execute("SELECT * FROM bookinfo WHERE author LIKE ? ORDER BY author DESC",(s2,)):
				tree.insert('',0,values=(x))
		elif dropdown.get()=='出版社':
			s3='%'+query.get()+'%'
			for x in c.execute("SELECT * FROM bookinfo WHERE publisher LIKE ? ORDER BY publisher DESC",(s3,)):
				tree.insert('',0,values=(x))
		elif dropdown.get()=='索书号':
			s4='%'+query.get()+'%'
			for x in c.execute("SELECT * FROM bookinfo WHERE title_id LIKE ? ORDER BY title_id DESC",(s4,)):
				tree.insert('',0,values=(x))
		def DBClick(event):	#双击书籍的信息弹出对话框进行借阅和归还
			item = tree.selection()[0]
			content=tree.item(item,"values")
			num=int(content[6])
			lent=int(content[7])
			borrow_panel=Toplevel()
			borrow_panel.title('借还书')			
			def borrow():
				nonlocal num
				nonlocal lent
				ISOTIMEFORMAT='%Y-%m-%d %X'
				s=time.strftime(ISOTIMEFORMAT,time.localtime())
				if num==0:
					err_panel=Toplevel()           #书已借完时再借的错误提示
					b_tip=Label(err_panel,text='已借完，不可借阅。').pack()
					b_ret=ttk.Button(err_panel,text='返回',command=err_panel.withdraw).pack()
					return	
				num -= 1
				lent += 1
				c.execute("UPDATE bookinfo SET available=available-1 WHERE ISBN=?",(content[0],))
				c.execute("UPDATE bookinfo SET lent=lent+1 WHERE ISBN=?",(content[0],))
				c.execute("INSERT INTO borrows VALUES(?,?,?,?,?)",(content[0],content[1],reader_ID,name,s))
				c.execute("INSERT INTO reader_borrows VALUES(?,?,?,?,?,?,?,?,'-')",(reader_ID,content[0],content[1],content[2],content[3],content[4],content[5],s))
				conn.commit()
				bor_panel=Toplevel()
				bor_tip=Label(bor_panel,text='借阅成功！').pack()
				bor_retu=ttk.Button(bor_panel,text='确定',command=bor_panel.withdraw).pack()
				b_num.config(text='可借量: '+str(num))
				b_lent.config(text='借出量: '+str(lent))
			def ret():    #点击归还后数据库以及界面的变化
				global reader_ID
				nonlocal num
				nonlocal lent
				ISOTIMEFORMAT='%Y-%m-%d %X'
				s=time.strftime(ISOTIMEFORMAT,time.localtime())
				if lent==0:
					err_panel=Toplevel()           #书已借完时再借的错误提示
					b_tip=Label(err_panel,text='操作错误，库存已满。').pack()
					b_ret=ttk.Button(err_panel,text='返回',command=err_panel.withdraw).pack()
					return
				num += 1
				lent -= 1
				c.execute("UPDATE bookinfo SET available=available+1 WHERE ISBN=?",(content[0],))
				c.execute("UPDATE bookinfo SET lent=lent-1 WHERE ISBN=?",(content[0],))
				c.execute("SELECT * FROM reader_borrows WHERE reader_ID=? AND ISBN=? AND return_time='-'",(reader_ID,content[0]))
				x=c.fetchall()
				if(x==[]):
					exe=Toplevel()
					Label(exe,text='没有借过此书，无法归还！').pack()
					ttk.Button(exe,text='返回',command=exe.withdraw).pack()
					return
				c.execute("UPDATE reader_borrows SET return_time=? WHERE reader_ID=? AND ISBN=?",(s,reader_ID,content[0]))
				conn.commit()
				ret_panel=Toplevel()
				ret_tip=Label(ret_panel,text='归还成功！').pack()
				ret_retu=ttk.Button(ret_panel,text='确定',command=ret_panel.withdraw).pack()
				b_num.config(text='可借量: '+str(num))
				b_lent.config(text='借出量: '+str(lent))
			b_ISBN=Label(borrow_panel,text='ISBN: '+content[0]).pack()
			b_title=Label(borrow_panel,text='书名: '+content[1]).pack()
			b_titleid=Label(borrow_panel,text='索书号: '+content[2]).pack()
			b_author=Label(borrow_panel,text='作者: '+content[3]).pack()
			b_publisher=Label(borrow_panel,text='出版社: '+content[4]).pack()
			b_location=Label(borrow_panel,text='馆藏地: '+content[5]).pack()
			b_num=Label(borrow_panel,text='可借量: '+str(num))
			b_num.pack()
			b_lent=Label(borrow_panel,text='借出量: '+str(lent))
			b_lent.pack()		
			b_borrow=ttk.Button(borrow_panel,text='借阅',command=borrow).pack(side='left',fill=X)
			b_return=ttk.Button(borrow_panel,text='归还',command=ret).pack(side='right',fill=X)		
		tree.bind("<Double-1>", DBClick)
		tree.pack()
	
	#管理员界面
	def admin_button_click(self):    
		global admin_query   #管理员的输入框
		global dropdown2,tab2    #管理员查询界面的下拉菜单，添加书的界面
		global buyISBN,buytitle,buytitleid,buyauthor,buypublisher,buylocation,buynum   #管理员查询界面的下拉选择菜单
		
		if (enter_ID.get()=='')or(enter_password.get()==''):
			exe=Toplevel()
			Label(exe,text='ID或密码错误！').pack()
			ttk.Button(exe,text='返回',command=exe.withdraw).pack()
			return
		c.execute("SELECT ID,password FROM admin WHERE ID=? AND password=? ",(enter_ID.get(),enter_password.get()))
		x=c.fetchall()
		if(x==[]):
			exe=Toplevel()
			Label(exe,text='ID或密码错误！').pack()
			ttk.Button(exe,text='返回',command=exe.withdraw).pack()
			return
		c.execute("SELECT ID FROM admin WHERE ID=?",(enter_ID.get(),))
		m=c.fetchall()
		admin_ID=m[0][0]

		admin=Toplevel()
		admin.geometry('1000x600')
		admin.title('管理员系统     '+admin_ID)
		notebook=ttk.Notebook(admin)
		notebook.pack(ipadx=250,ipady=200)
		self.image1=PhotoImage(file="03.png")
		f1=Frame(notebook)
		bg1=Label(f1,image=self.image1,width=5000,height=1600).pack()
		f2=Frame(notebook)
		bg2=Label(f2,image=self.image1,width=5000,height=1600).pack()
		f3=Frame(notebook)
		bg3=Label(f3,image=self.image1,width=3500,height=1600).pack()
		
		tab1=notebook.add(f1,text='书籍的采购与淘汰')       #NoteBook控件的第一页，淘汰功能
		admin_tip=Label(f1,text='查询你想进行操作的书籍:',font='Times 15 bold').place(x=380,y=120)
		admin_query = Entry(f1)
		admin_query.place(x=265,y=200,width=500,height=30)
		admin_query_button = ttk.Button(f1,text='查询',command=self.admin_query_click).place(x=770,y=196,width=70,height=36)
		admin_items = ('书名','索书号','作者','出版社')
		dropdown2 = Pmw.ComboBox(f1,label_text='查询条件',labelpos='nw',scrolledlist_items = admin_items,)      #查询条件的下拉菜单
		dropdown2.place(x=155,y=190,width=100)
		first = admin_items[0]     #下拉菜单初始显示'书名'，即item[0]
		dropdown2.selectitem(first)
		
		tab2=notebook.add(f2,text='增添采购的新书')  #NoteBook控件的第二页，新书入库功能
		buy_ISBN=Label(f2,text='ISBN:').place(x=350,y=100)
		buyISBN=Entry(f2)                  
		buyISBN.place(x=400,y=101,width=200)
		buy_title=Label(f2,text='书名:').place(x=350,y=140)
		buytitle=Entry(f2)
		buytitle.place(x=400,y=141,width=200)
		buy_titleid=Label(f2,text='索书号:').place(x=350,y=180)
		buytitleid=Entry(f2)
		buytitleid.place(x=400,y=181,width=200)
		buy_author=Label(f2,text='作者:').place(x=350,y=220)
		buyauthor=Entry(f2)
		buyauthor.place(x=400,y=221,width=200)
		buy_publisher=Label(f2,text='出版社:').place(x=350,y=260)
		buypublisher=Entry(f2)
		buypublisher.place(x=400,y=261,width=200)
		buy_location=Label(f2,text='馆藏地:').place(x=350,y=300)
		buylocation=Entry(f2)
		buylocation.place(x=400,y=301,width=200)
		buy_num=Label(f2,text='数量:').place(x=350,y=340)
		buynum=Entry(f2)
		buynum.place(x=400,y=341,width=200)
		buy=ttk.Button(f2,text='提交',command=self.buy_newbook).place(x=450,y=390,height=30)
		
		tab3=notebook.add(f3,text='信息记录')  #NoteBook控件的第三页，信息查询功能
		
		def borrow_h():    #显示借阅历史
			table=Toplevel()
			table.title('借阅历史')
			tree=ttk.Treeview(table,columns=('col1','col2','col3','col4','col5'))   #Treeview创建表格
			tree.column('col1', width=100, anchor='w')	#设置表格的行列信息
			tree.column('col2', width=200, anchor='w')
			tree.column('col3', width=100, anchor='center')  
			tree.column('col4', width=100, anchor='center')
			tree.column('col5', width=200, anchor='center')
			tree.heading('col1', text='ISBN')
			tree.heading('col2', text='书名')
			tree.heading('col3', text='借阅人ID')
			tree.heading('col4', text='借阅人姓名')
			tree.heading('col5', text='借出时间')
			for x in c.execute("SELECT * FROM borrows;"):
				tree.insert('',0,values=(x))
			tree.pack()
		def add_h():    #显示采购历史
			table=Toplevel()
			table.title('采购历史')
			tree=ttk.Treeview(table,columns=('col1','col2','col3','col4'))   #Treeview创建表格
			tree.column('col1', width=100, anchor='w')  #设置表格的行列信息
			tree.column('col2', width=200, anchor='w')
			tree.column('col3', width=50, anchor='center')
			tree.column('col4', width=200, anchor='center')
			tree.heading('col1', text='ISBN')
			tree.heading('col2', text='书名')
			tree.heading('col3', text='数量')
			tree.heading('col4', text='采购时间')
			for x in c.execute("SELECT * FROM buys;"):
				tree.insert('',0,values=(x))
			tree.pack()
		def die_h():     #显示淘汰历史
			table=Toplevel()
			table.title('淘汰历史')
			tree=ttk.Treeview(table,columns=('col1','col2','col3','col4'))   #Treeview创建表格
			tree.column('col1', width=100, anchor='w')  #设置表格的行列信息
			tree.column('col2', width=200, anchor='w')
			tree.column('col3', width=50, anchor='center')
			tree.column('col4', width=200, anchor='center')
			tree.heading('col1', text='ISBN')
			tree.heading('col2', text='书名')
			tree.heading('col3', text='数量')
			tree.heading('col4', text='淘汰时间')
			for x in c.execute("SELECT * FROM dies;"):
				tree.insert('',0,values=(x))
			tree.pack()
		def readers():   #显示读者信息
			table=Toplevel()
			table.title('读者信息')
			tree=ttk.Treeview(table,columns=('col1','col2'))   #Treeview创建表格
			tree.column('col1', width=100, anchor='w')  #设置表格的行列信息
			tree.column('col2', width=100, anchor='center')
			tree.heading('col1', text='ID')
			tree.heading('col2', text='姓名')
			for x in c.execute("SELECT ID,name FROM readers ORDER BY ID DESC"):
				tree.insert('',0,values=(x))
			def DBClick1(event):		#双击显示该读者借过的所有书
				item = tree.selection()[0]
				content=tree.item(item,"values")
				borrow_book=Toplevel()
				borrow_book.title('借阅的书')
				tree1=ttk.Treeview(borrow_book,columns=('col1','col2','col3','col4','col5','col6','col7','col8'))   #Treeview创建表格
				tree1.column('col1', width=100, anchor='w')  
				tree1.column('col2', width=150, anchor='w')
				tree1.column('col3', width=150, anchor='w')
				tree1.column('col4', width=150, anchor='w')
				tree1.column('col5', width=200, anchor='w')
				tree1.column('col6', width=100, anchor='center')
				tree1.column('col7', width=150, anchor='center')
				tree1.column('col8', width=150, anchor='center')

				tree1.heading('col1', text='ISBN')
				tree1.heading('col2', text='书名')
				tree1.heading('col3', text='索书号')
				tree1.heading('col4', text='作者')
				tree1.heading('col5', text='出版社')
				tree1.heading('col6', text='馆藏地')
				tree1.heading('col7', text='借出时间')
				tree1.heading('col8', text='归还时间')
				for y in c.execute("SELECT ISBN,title,title_ID,author,publisher,location,borrow_time,return_time FROM reader_borrows WHERE reader_ID=? ORDER BY return_time",(content[0],)):
					tree1.insert('',0,values=(y))
				tree1.pack()
			tree.bind("<Double-1>", DBClick1)
			tree.pack()
		c.execute("SELECT SUM(available) FROM bookinfo ")
		booksum=c.fetchone()[0]
		c.execute("SELECT SUM(lent) FROM bookinfo ")
		booksum_borrow=c.fetchone()[0]
		c.execute("SELECT SUM(num) FROM dies ")
		booksum_die=c.fetchone()[0]
		booksum_tip=Label(f3,text='当前在馆可借图书共%d本,已借出图书共%d本，已淘汰图书共%d本'%(booksum,booksum_borrow,booksum_die),font='YaHei 15 bold').place(x=175,y=70)
		b_his=ttk.Button(f3,text='借阅历史',command=borrow_h).place(x=195,y=140,width=170,height=80)
		a_his=ttk.Button(f3,text='采购历史',command=add_h).place(x=595,y=140,width=170,height=80)
		d_his=ttk.Button(f3,text='淘汰历史',command=die_h).place(x=195,y=340,width=170,height=80)
		r_info=ttk.Button(f3,text='读者信息',command=readers).place(x=595,y=340,width=170,height=80)
	def admin_query_click(self):     #管理员界面的查询
		table=Toplevel()                        #新面板
		table.title('管理员查询')
		tree=ttk.Treeview(table,columns=('col1','col2','col3','col4','col5','col6','col7','col8'))   #Treeview创建表格
		tree.column('col1', width=100, anchor='w')  #设置表格的行列信息
		tree.column('col2', width=200, anchor='w')
		tree.column('col3', width=150, anchor='w')
		tree.column('col4', width=180, anchor='w')
		tree.column('col5', width=260, anchor='w')
		tree.column('col6', width=100, anchor='center')
		tree.column('col7', width=50, anchor='center')
		tree.column('col8', width=50, anchor='center')
		tree.heading('col1', text='ISBN')
		tree.heading('col2', text='书名')
		tree.heading('col3', text='索书号')
		tree.heading('col4', text='作者')
		tree.heading('col5', text='出版社')
		tree.heading('col6', text='馆藏地')
		tree.heading('col7', text='可借量')
		tree.heading('col8', text='借出量')
		if dropdown2.get()=='书名':                             #查询
			s1='%'+admin_query.get()+'%'
			for x in c.execute("SELECT * FROM bookinfo WHERE title LIKE ? ORDER BY title DESC",(s1,)):
				tree.insert('',0,values=(x))
		elif dropdown2.get()=='作者':
			s2='%'+admin_query.get()+'%'
			for x in c.execute("SELECT * FROM bookinfo WHERE author LIKE ? ORDER BY title DESC",(s2,)):
				tree.insert('',0,values=(x))
		elif dropdown2.get()=='出版社':
			s3='%'+admin_query.get()+'%'
			for x in c.execute("SELECT * FROM bookinfo WHERE publisher LIKE ? ORDER BY title DESC",(s3,)):
				tree.insert('',0,values=(x))
		elif dropdown2.get()=='索书号':
			s4='%'+admin_query.get()+'%'
			for x in c.execute("SELECT * FROM bookinfo WHERE title_id LIKE ? ORDER BY title DESC",(s4,)):
				tree.insert('',0,values=(x))
		def DBClick(event):	#管理员界面双击书籍的信息弹出对话框进行采购已有的书和淘汰操作
			item = tree.selection()[0]
			content=tree.item(item,"values")
			num=int(content[6])
			lent=int(content[7])
			AddDie_panel=Toplevel()	
			AddDie_panel.geometry('400x300')
			AddDie_panel.title('书籍的采购与淘汰')
			AddDie_ISBN=Label(AddDie_panel,text='ISBN: '+content[0]).pack()         #显示书籍信息
			AddDie_title=Label(AddDie_panel,text='书名: '+content[1]).pack()
			AddDie_titleid=Label(AddDie_panel,text='索书号: '+content[2]).pack()
			AddDie_author=Label(AddDie_panel,text='作者: '+content[3]).pack()
			AddDie_publisher=Label(AddDie_panel,text='出版社: '+content[4]).pack()
			AddDie_location=Label(AddDie_panel,text='馆藏地: '+content[5]).pack()
			AddDie_num=Label(AddDie_panel,text='可借量: '+str(num))
			AddDie_num.pack()
			AddDie_lent=Label(AddDie_panel,text='借出量: '+str(lent))
			AddDie_lent.pack()
			Add_tip=Label(AddDie_panel,text='采购数量:').place(x=85,y=199)
			Add_num=Entry(AddDie_panel)
			Add_num.place(x=145,y=200,width=100)
			Die_tip=Label(AddDie_panel,text='淘汰数量:').place(x=85,y=239)
			Die_num=Entry(AddDie_panel)
			Die_num.place(x=145,y=240,width=100)		
			
			def add():  #采购已有的书
				nonlocal num
				ISOTIMEFORMAT='%Y-%m-%d %X'
				s=time.strftime(ISOTIMEFORMAT,time.localtime())
				if Add_num.get()=='':
					err=Toplevel()
					Label(err,text='输入错误！').pack()
					ttk.Button(err,text='返回',command=err.withdraw).pack()
					return
				for x in Add_num.get():
					if(x>='0')and(x<='9'):
						pass
					else:
						err=Toplevel()
						Label(err,text='输入错误！').pack()
						ttk.Button(err,text='返回',command=err.withdraw).pack()
						return
				num+=int(Add_num.get())
				AddDie_num.config(text='可借量: '+str(num))
				c.execute("UPDATE bookinfo SET available=available+? WHERE ISBN=?",(int(Add_num.get()),content[0]))
				c.execute("INSERT INTO buys VALUES(?,?,?,?);",(content[0],content[1],int(Add_num.get()),s))
				conn.commit()
				exe=Toplevel()
				Label(exe,text='提交成功！').pack()
				ttk.Button(exe,text='确定',command=exe.withdraw).pack()
			def die():	#淘汰书
				nonlocal num
				nonlocal lent
				ISOTIMEFORMAT='%Y-%m-%d %X'
				s=time.strftime(ISOTIMEFORMAT,time.localtime())
				if Die_num.get()=='':
					err=Toplevel()
					Label(err,text='输入错误！').pack()
					ttk.Button(err,text='返回',command=err.withdraw).pack()
					return
				for x in Die_num.get():
					if(x>='0')and(x<='9'):
						pass
					else:
						err=Toplevel()
						Label(err,text='输入错误！').pack()
						ttk.Button(err,text='返回',command=err.withdraw).pack()
						return
				if (num>lent) and ((num-lent)>=int(Die_num.get())):
					num-=int(Die_num.get())
					AddDie_num.config(text='可借量: '+str(num))
					c.execute("UPDATE bookinfo SET available=available-? WHERE ISBN=?",(int(Die_num.get()),content[0]))
					c.execute("INSERT INTO dies VALUES(?,?,?,?);",(content[0],content[1],int(Die_num.get()),s))
					if num==lent==0:
						c.execute("DELETE FROM bookinfo WHERE ISBN=?",(content[0],))
					conn.commit()
					exe=Toplevel()
					Label(exe,text='提交成功！').pack()
					ttk.Button(exe,text='确定',command=exe.withdraw).pack()
					return
				else :
					Err=Toplevel()
					Label(Err,text='数量错误！').pack()
					ttk.Button(Err,text='返回',command=Err.withdraw).pack()
					return
			Add=ttk.Button(AddDie_panel,text='提交',command=add).place(x=255,y=198)
			Die=ttk.Button(AddDie_panel,text='提交',command=die).place(x=255,y=238)
		tree.bind("<Double-1>", DBClick)		
		tree.pack()
	def buy_newbook(self):   #增添新书功能
		confirm=Toplevel(tab2)
		def err():
			Label(confirm,text='数据输入错误，请重新输入！').pack()
			ttk.Button(confirm,text='返回',command=confirm.withdraw).pack()
		if (buyISBN.get()=='')or(buytitle.get()=='')or(buytitleid.get()=='')or(buyauthor.get()=='')or(buypublisher.get()=='')or(buylocation.get()=='')or(buynum.get()==''):
			err()
			return
		for x in buynum.get():
			if(x>='0')and(x<='9'):
				pass
			else:
				er=Toplevel()
				Label(er,text='数量输入错误！').pack()
				ttk.Button(er,text='返回',command=er.withdraw).pack()
				return
		ISOTIMEFORMAT='%Y-%m-%d %X'
		s=time.strftime(ISOTIMEFORMAT,time.localtime())
		s1=buyISBN.get()
		s2=buytitle.get()
		s3=buytitleid.get()
		s4=buyauthor.get()
		s5=buypublisher.get()
		s6=buylocation.get()
		s7=int(buynum.get())
		c.execute("SELECT * FROM bookinfo WHERE ISBN=?",(s1,))
		x=c.fetchall()		#检查库存，若有ISBN匹配则说明不是新书
		if (x!=[]):		
			Label(confirm,text='库中已有此书，不属于新书入库，请在查询界面进行采购操作！').pack()
			ttk.Button(confirm,text='返回',command=confirm.withdraw).pack()
			return
		c.execute("INSERT INTO bookinfo VALUES(?,?,?,?,?,?,?,0);",(s1,s2,s3,s4,s5,s6,s7))    #插入新书信息
		c.execute("INSERT INTO buys VALUES(?,?,?,?);",(s1,s2,s7,s))   #插入添新书的历史记录
		conn.commit()
		Label(confirm,text='提交成功！').pack()
		ttk.Button(confirm,text='确定',command=confirm.withdraw).pack()


 
root=Tk()
Pmw.initialise(root)
root.title("欢迎使用图书管理系统！")
app=Application(root)
app.mainloop()