from flask import Flask,request,render_template,render_template_string
import os
import sqlite3
import base64
import random
import re


app = Flask(__name__)

#Please ignore these dict and lists
submitted_flag= []

data = {'level1':'9lXe5lXe5lXe6F2MfNXeAdHbh91cp9FbzY3Ms9FdzJXImt3ZhxmZ', 'level2':'9NncyJncyJnczQ3MtBkchB3XoRHMi9lczQHbpZ2XwQ3X5pHQs9FMwQ3XtF0XJt3ZhxmZ',
	'level3':'9FSIwBHcwBHcV1mchd3Xy9kZfRmbF9VRoR3XTl2XzlGaUt3ZhxmZ', 'level4':'9d3d3d3d3d3b39FZyBzdzNXYw9Vet9FZuFiZfVHM5t3ZhxmZ',
	'level5':'9VXd1VXd1VXd1VXd1BTefRHQzI2X0BjbuB0YfRmcwc3czFGcfNjc1N2Mz9Vet9FanVHMoRHbBt3ZhxmZ', 		'level6':'9lXe5lXe5lXe5lXe5lXe5lXe5l3MuJXdwo2XzQXIsF3cfJXdwk3X0B0XrNWds9FZwAzZfVHM59FazFydfl0Xk5GNfdmbww2X5J3M291ZAxmZfNDa09FdVB3XJ9FMz9VZn52MsxGQoN2XsRjbhY2Xzl2XzFCa091cBt3ZhxmZ'
	}

msg = [ 'Hey admin! this is a test message.', 'This website is awesome!', 'I need to reset my password.', 'The UI is so nice.', 'How can I contact you admin!',
	'I need s0me h3lp!!!!!!!', 'I want to meet you at Sunday.', 'Today I hang out with my friends.', 'How old are you admin?', 'Help me my account has been stolen.']

alert = ['Unusual login alert from a device!', "You didn't backup your files for a long time!", f'Someone is trying to login your account IP={random.randint(10,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}', 
	 'Please backup files regularly.', 'Your personal info is updated!', f'There are {random.randint(1,2000)} new users today.', 
	 f'{random.randint(1,300)} users are banned today because of hate speech!', f'There are {random.randint(1,50000)} users in total!',
	 'Backup finished!', f'{random.randint(1,1000)} people like your post!'
]

level6_blacklist = ["ABORT", "ACTION", "ADD", "AFTER", "ALL", "ALTER", "ALWAYS", "ANALYZE", "AND", "AS", "ASC", "ATTACH", "AUTOINCREMENT", "BEFORE", "BEGIN", "BETWEEN", "CASCADE", "CASE", "CAST", "CHECK", "COLLATE", "COLUMN", "COMMIT", "CONFLICT", "CONSTRAINT", "CREATE", "CROSS", "CURRENT", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "DATABASE", "DEFAULT", "DEFERRABLE", "DEFERRED", "DELETE", "DESC", "DETACH", "DISTINCT", "DO", "DROP", "EACH", "ELSE", "END", "ESCAPE", "EXCEPT", "EXCLUDE", "EXCLUSIVE", "EXISTS", "EXPLAIN", "FAIL", "FILTER", "FIRST", "FOLLOWING", "FOR", "FOREIGN", "FROM", "FULL", "GENERATED", "GLOB", "GROUP", "GROUPS", "HAVING", "IF", "IGNORE", "IMMEDIATE", "IN", "INDEX", "INDEXED", "INITIALLY", "INNER", "INSERT", "INSTEAD", "INTERSECT", "INTO", "IS", "ISNULL", "JOIN", "KEY", "LAST", "LEFT", "LIKE", "LIMIT", "MATCH", "MATERIALIZED", "NATURAL", "NO", "NOT", "NOTHING", "NOTNULL", "NULL", "NULLS", "OF", "OFFSET", "ON", "OR", "ORDER", "OTHERS", "OUTER", "OVER", "PARTITION", "PLAN", "PRAGMA", "PRECEDING", "PRIMARY", "QUERY", "RAISE", "RANGE", "RECURSIVE", "REFERENCES", "REGEXP", "REINDEX", "RELEASE", "RENAME", "REPLACE", "RESTRICT", "RETURNING", "RIGHT", "ROLLBACK", "ROW", "ROWS", "SAVEPOINT", "SELECT", "SET", "TABLE", "TEMP", "TEMPORARY", "THEN", "TIES", "TO", "TRANSACTION", "TRIGGER", "UNBOUNDED", "UNION", "UNIQUE", "UPDATE", "USING", "VACUUM", "VALUES", "VIEW", "VIRTUAL", "WHEN", "WHERE", "WINDOW", "WITH", "WITHOUT","HEX","SUBSTR","level6"]

def connection(tbl_name):
	con = sqlite3.connect('database.db')
	cur = con.cursor()
	cur.execute(f"CREATE TABLE {tbl_name}(id integer PRIMARY KEY,username text,password text)")
	con.commit()
	
def insert(tbl_name, user_id, username, password):
	con = sqlite3.connect('database.db')
	cur = con.cursor()
	cur.execute(f"INSERT INTO {tbl_name} (id,username,password) VALUES ({user_id},'{username}',\"{password}\")")
	con.commit()
	
def drop(tbl_name):
	con = sqlite3.connect('database.db')
	cur = con.cursor()
	cur.execute(f"DROP TABLE {tbl_name}")
	con.commit()

def update_flag(tbl_name,password,user_id):
	con = sqlite3.connect('database.db')
	cur = con.cursor()
	try:
		result = cur.execute(f"UPDATE {tbl_name} SET password=? where id=?", (password,user_id,))
		con.commit()
		return True
	except:
		return False
	
def CheckCreds(tbl_name,username, password):
	con = sqlite3.connect('database.db')
	cur = con.cursor()
	try:
		result = cur.execute(f"SELECT * from {tbl_name} where username='{username}' and password='{password}'").fetchall()
	except:
		return False
	con.commit()
	cur.close()
	con.close()
	if result == []:
		return False
	else:
		return True


def get_flag(tbl_name,userid):
	con = sqlite3.connect('database.db')
	cur = con.cursor()
	flag = cur.execute(f"SELECT password FROM {tbl_name} where id={userid}").fetchall()
	con.commit()
	cur.close()
	con.close()
	return str(flag).strip("(['])")[:-2]
	
def filters(name,blacklist):
	for i in blacklist:
		regex = re.compile(i,re.IGNORECASE)
		name = regex.sub("",name)
	return name
		


@app.route('/')
def index():
	return render_template("index.html",msg = "",error='')



@app.route('/reset')
def remove():
	if request.method == 'GET':
		if os.path.isfile('database.db'):	
			os.remove('database.db')
		for i in range(1,7):
			tbl_name = f"level{i}"
			connection(tbl_name)
			insert(tbl_name,1,"admin",base64.b64decode(data[f'level{i}'][::-1]).decode('utf-8'))
		return "Success"

@app.route('/update',methods = ['GET','POST'])
def update():
	if request.method == 'GET':
		return render_template("update.html")
	else:
		level = request.values['level']
		flag_value = request.values['flag']
		levels = ['level1','level2','level3','level4','level5','level6']
		if len(flag_value) == 0:
			render_template("update.html", error = 'Flag value can\'t be empty!')
		if len(level) > 6 or level not in levels:
			return render_template("update.html",error = 'Please select the valid table!')
		if level == levels[2]:
			for i in flag_value:
				if i.isnumeric():
					message = "For challenge purpose, make sure your level3 flag don't contain [0-9] numbers!"
					return render_template("update.html", error = message)
				else:
					continue
		if update_flag(level,flag_value,1) == True:
			return render_template("update.html", msg = f"Updated {level} flag Successfully!")
		else:
			return render_template("update.html", error = "Error while updating flag")
		



@app.route('/submit',methods=['POST'])
def submit():
	if request.method == 'POST':
		submit_flag = request.values['flag']
		real_flag = []
		for i in range(1,7):
			real_flag.append(base64.b64decode(data[f'level{i}'][::-1]).decode('utf-8'))
		
		if submit_flag in submitted_flag:
			return render_template("index.html",msg='', error = 'You have already solved that challenge!')
				
		for index,value in enumerate(real_flag):
			if submit_flag == value:
				index = index+1
				submitted_flag.append(value)
				return render_template("index.html",msg = f"Congrats! you solved level{index}.",error='')
			else:
				continue
		if submit_flag not in real_flag:
			return render_template("index.html",msg='', error = "Sorry! your flag is incorrect! Try harder.")
			
				



@app.route('/level1',methods=['POST','GET'])
def level1():
	if request.method == 'POST':
		username = request.values['username']
		password = request.values['password']
		blacklist = ['level2','level3','level4','level5','level6','LIMIT','limit']
		for i in blacklist:	#ignore this
			if username.find(i) != -1:
				return render_template("level1.html",value="Please don't attack other tables!")
			elif password.find(i) != -1:
				return render_template("level1.html",value="Please don't attack other tables!")
			else:
				continue
		#challenge start from here!!
		if CheckCreds('level1',username,password) == True:
			flag = get_flag('level1',1)
			return render_template("admin.html",msg=msg[random.randint(0,len(msg)-1)],alert=alert[random.randint(0,len(alert)-1)],flag=flag)
		else:
			return render_template("level1.html",value="Username or passowrd incorrect!!")
	else:
		return render_template("level1.html")



@app.route('/level2',methods = ['GET','POST'])
def level2():
	if request.method == 'GET':
		return render_template("level2.html")
	if request.method == 'POST':
		username = request.values['username']
		password = request.values['password']
		blacklist = ['level3','level4','level1','level5','level6','LIMIT','limit']
		for i in blacklist:	#ignore this
			if username.find(i) != -1:
				return render_template("level2.html",value="Please don't attack other tables!")
			elif password.find(i) != -1:
				return render_template("level2.html",value="Please don't attack other tables!")
			else:
				continue
		#challenge start from here!!
		for i in username:
			if i.isnumeric():
				return render_template("level2.html",value="Contain unacceptable characters")
			else:
				continue
		creds = CheckCreds('level2',username,password) 
		if creds == True:
			flag = get_flag('level2',1)
			return render_template("admin.html",msg=msg[random.randint(0,len(msg)-1)],alert=alert[random.randint(0,len(alert)-1)],flag=flag)
		else:
			return render_template("level2.html",value="Username or password incorrect!!")
		

@app.route('/level3',methods=['GET','POST'])
def level3():
	if request.method == 'GET':
		return render_template("level3.html")
	if request.method == 'POST':
		username = request.values['username']
		password = request.values['password']
		blacklist = ['level1','level2','level4','level5','level6','LIMIT','limit']
		for i in blacklist:	#ignore this
			if username.find(i) != -1:
				return render_template("level3.html",value="Please don't attack other tables!")
			elif password.find(i) != -1:
				return render_template("level3.html",value="Please don't attack other tables!")
			else:
				continue
		#challenge start from here!!
		for i in username:
			if i.isnumeric():
				return render_template("level3.html",value="Contain unacceptable character!")
			else:
				continue
		for j in password:
			if j.isnumeric():
				return render_template("level3.html",value="Contain unacceptable character!")
			else:
				continue
		creds = CheckCreds('level3',username,password)
		if creds == True:
			flag = get_flag('level3',1)
			return render_template("admin.html",msg=msg[random.randint(0,len(msg)-1)],alert=alert[random.randint(0,len(alert)-1)],flag=flag)
		else:
			return render_template("level3.html",value="Username or password incorrect!!")
		
		

@app.route('/level4', methods=['GET','POST'])
def level4():
	if request.method == 'GET':
		return render_template("level4.html")
	if request.method == 'POST':
		username = request.values['username']
		password = request.values['password']
		blacklist = ['level1','level2','level3','level5','level6','LIMIT','limit']
		for i in blacklist:	#ignore this
			if username.find(i) != -1:
				return render_template("level4.html",value="Please don't attack other tables!")
			elif password.find(i) != -1:
				return render_template("level4.html",value="Please don't attack other tables!")
			else:
				continue
		#challenge start from here!!
		if CheckCreds('level4',username,password) == True:
			message = "You th!nk there will be flag in here??"
			return render_template("admin.html",msg=msg[random.randint(0,len(msg)-1)],alert=alert[random.randint(0,len(alert)-1)],flag=message)
		else:
			return render_template("level4.html",value="Username or passowrd incorrect!!")
		
		
		
@app.route('/level5', methods = ['GET','POST'])
def level5():
	if request.method == 'GET':
		return render_template("level5.html")
	if request.method == 'POST':
		username = request.values['username']
		password = request.values['password']
		blacklist = ['level1','level2','level3','level4','level6','LIMIT','limit']
		for i in blacklist:	#ignore this
			if username.find(i) != -1:
				return render_template("level5.html",value="Please don't attack other tables!")
			elif password.find(i) != -1:
				return render_template("level5.html",value="Please don't attack other tables!")
			else:
				continue
		#challenge start from here!!
		unacceptable = ["UNION","OR","AND","SELECT","FROM","WHERE","level5","ON"]
		username = filters(username, unacceptable)
		password = filters(password, unacceptable)
		if CheckCreds('level5', username,password) == True:
			message = "I told you there is no flag in here!!!!"
			return render_template("admin.html",msg=msg[random.randint(0,len(msg)-1)], alert = alert[random.randint(0,len(alert)-1)], flag = message)
		else:
			return render_template("level5.html", value = "Username or password incorrect!!")
		
		
		
		
@app.route('/level6', methods = ['GET','POST'])
def level6():
	if request.method == 'GET':
		return render_template("level6.html")
	if request.method == 'POST':
		username = request.values['username']
		password = request.values['password']
		blacklist = ['level1','level2','level3','level4','level5','LIMIT','limit']
		for i in blacklist:	#ignore this
			if username.find(i) != -1:
				return render_template("level6.html", value = "Please don't attack other tables!")
			elif password.find(i) != -1:
				return render_template("level6.html", value = "Please don't attack other tables!")
			else:
				continue
		
		#challenge start from here!!
		username = filters(username, level6_blacklist)
		password = filters(password, level6_blacklist)
		if CheckCreds('level6', username, password) == True:
			message = "The flag is not in h3r3333333333333333, buddy!!!!!"
			return render_template("admin.html", msg = msg[random.randint(0,len(msg)-1)], alert = alert[random.randint(0,len(alert)-1)], flag = message)
		else:
			return render_template("level6.html" , value = "Username or password incorrect!!")
			

