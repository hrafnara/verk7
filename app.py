from flask import Flask, render_template as rend, session, request
import hashlib, binascii, os, pymysql,secrets
app = Flask(__name__)
app.secret_key = os.urandom(24)
connection = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1209023850', password='mypassword', database='1209023850_verk7', autocommit=True)
cursor = connection.cursor()
#alltaf gaman að fara overboard
app.secret_key = secrets.token_hex(255)

def authorize(user):
    pass
    #todo tengja við localhost, muna að breyta aftur

def verify_password(stored_password, provided_password):
    return provided_password == stored_password

def verify():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print("{0} {1} {2}".format(row[0], row[1], row[2]))
     
@app.route('/')
def index():
    if "user" not in session.keys():
        user = {"uname":None,"pass":None,"nafn":None}
    else:
        user = session["user"]
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    print(rows)
    return rend("index.html", user = user, rows = rows)

@app.route("/signup")
def signup():
    return rend("signup.html",code=None)

@app.route("/signup/create",methods=['POST'])
def addusr():
    r=request.form
    print(r)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    if request.form['name'] in map(lambda x: x[0], rows):
        pass
    cursor.execute("""INSERT INTO users (user, pass, nafn) VALUES
    (%s, %s, %s);""" % 
    (connection.escape(r['username']),
    connection.escape(r['password']),
    connection.escape(r['name'])))
    return rend("signup.html",code=0)

@app.route("/login")
def login_page():
    return rend("login.html",code = None)

@app.route("/login/process",methods=['POST'])
def login():
    r=request.form
    cursor.execute("""select * from users where user="%s";""" % r["username"])
    rows = cursor.fetchall()
    if rows!=():
        user = rows[0]
        if verify_password(user[1],r["password"]):
            session["user"] = {"username":user[0],"nafn":user[2],"pass":user[1]}
            print(session["user"])
        else: 
            return rend("login.html", code=1)
    else: 
        print(rows)
        return rend("login.html", code=1)
    return rend("login.html", code=0)

@app.route("/account")
def account():
    if "user" in session.keys():
        sql= "SELECT postur FROM posts WHERE user ="
        user = session["user"]
        prent = user['nafn']
        cursor.execute(sql+"'"+prent+"'")
        gogn =  cursor.fetchall()
        if session["user"]["username"] != None:
            return rend("account.html", user = session["user"], gogn = gogn)
    return index()
@app.route("/logout")
def logout():
    session["user"] ={"uname":None,"pass":None,"nafn":None}
    return index()


@app.route("/account/eida",methods=['POST'])
def eida():
    if "user" in session.keys():
        sql2= "SELECT postur FROM posts WHERE user ="
        user = session["user"]
        prent = user['nafn']
        cursor.execute(sql2+"'"+prent+"'")
        gogn =  cursor.fetchall()
        user = session["user"]
        prent = user['nafn']
        print(prent)
        print(user)
        sql = "DELETE FROM posts WHERE user ="
        print(sql+"'"+prent+"'")
        cursor.execute(sql+"'"+prent+"'")
        return rend("account.html", user = session["user"], gogn = gogn)
    else: return index()

@app.route("/index/create",methods=['POST'])
def addpost():
    r=request.form
    user2 = session["user"]
    num = 1
    name = (user2["nafn"])
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    if request.form['postur'] in map(lambda x: x[0], rows):
        pass
    cursor.execute("""INSERT INTO posts (user, postur, num) VALUES
    (%s, %s, %s);""" % 
    (connection.escape(name),
    connection.escape(r['postur']),
    connection.escape(num)))
    return rend("index.html", user = user2, rows =rows)


if __name__ == "__main__":
    app.run(debug=True)
