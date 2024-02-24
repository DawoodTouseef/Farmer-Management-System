from flask import Flask, render_template, request, redirect, url_for, session 
import sqlite3
import re 
from decimal import *

  
app = Flask(__name__) 

app.secret_key = 'your secret key'
DATABASE="farmer.db"
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Initialize the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
  
# routes  
# login route
@app.route('/')
@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = '' 
    if request.method == 'POST':
        
        # getting id and password
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = get_db()
        
        # getting farmer where id and password matches
        data=cursor.execute('SELECT * FROM farmer WHERE User_id = ? AND Password = ? ',(username,password))
        account = data.fetchone()

        if account:

            # if account found then log in successful
            session['loggedin'] = True
            session['id'] = account['User_id'] 
            msg = 'Logged in successfully!!!'
            if account['F_Firstname'] == '' and account['F_Lastname'] == '' or (account['F_Firstname'] is None and account['F_Lastname'] is None):
                
                # if firstname and lastname is none or empty and then complete profile
                msg = "complete your profile"
                return render_template("complete.html")
            
            # getting farmer info where id and password matches
            cursor = get_db()
            data=cursor.execute('SELECT * FROM farmer WHERE User_id = ? ', (session['id'],)) 
            info = data.fetchone()
            data = {'user_id': session['id'], 'msg': msg, 'info': info}

            # displaying farmer basic info 
            return render_template('index.html', **data)
        else:
            # if username/password not matching with our database or not present in database then displaying error 
            msg = 'Incorrect username / password!!!'
    return render_template('login.html', msg = msg) 

# logout route
@app.route('/logout') 
def logout():
    
    # removing data of current logged in farmer from sessions  
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 

# signup route
@app.route('/signup', methods =['GET', 'POST']) 
def signup(): 
    msg = ''
    if request.method == 'POST':

        # getting new id and new password
        user_id = request.form['username'] 
        password = request.form['password']
        cursor = get_db()

        # getting farmer where id and password matches
        data=cursor.execute('SELECT * FROM farmer WHERE User_id = ?', (user_id, )) 
        account = data.fetchall()

        if account:

            # if user already exists then displaying error
            msg = 'Account already exists!!!'
        else: 

            # if user don't exists then create new user
            cursor.execute('INSERT INTO farmer(User_id,Password) VALUES (?, ?)', (user_id, password))
            cursor.commit() 
            msg = 'You have successfully registered!!!'
            return render_template('login.html', msg=msg) 
    return render_template('signup.html', msg = msg)

# complete route
@app.route('/complete', methods =['GET', 'POST'])
def complete():
    msg = "Please first create user!!!" 
    if request.method == 'POST':

        # getting other info of new user and adding it in our database and going to home page
        first = request.form['first']
        last = request.form['last']
        gender = request.form['gender']
        address = request.form['address']
        contact = request.form['contact']
        user_id = session['id']
        cursor = get_db()
        cursor.execute('UPDATE farmer SET F_Firstname=?, F_Lastname=?, F_Gender=?, F_Address = ?, F_ContactNo=? WHERE User_id=?', (first, last, gender, address, contact, user_id))
        cursor.commit()
        data=cursor.execute('SELECT * FROM farmer WHERE User_id = ? ', (session['id'],))
        info=data.fetchone()
        msg="successfully completed profile!!!"
        data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('index.html', **data)

# from now 9 routes are used for displaying respected data and if no data found then display error
# 1 - home route - to main user page
@app.route('/home')
def home():
    msg = ""
    cursor = get_db()
    data=cursor.execute('SELECT * FROM farmer WHERE User_id = ? ', (session['id'],)) 
    info = data.fetchone()
    data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('index.html', **data)

# 2 - farm route - to display farm data
@app.route('/farm')
def farm():
    msg=""
    cursor = get_db()
    data=cursor.execute('SELECT Farm_Id,Farm_Acre,Farm_Location,Irrigation_Source FROM farm WHERE User_id = ? ', (session['id'],))
    info = data.fetchall()
    if len(info)==0:
        msg="Sorry, no data found!!!"
    data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('Farm/farm.html', **data)

# 3 - crop_allocation route - to display all currently allocated crop data
@app.route('/crop_allocation')
def crop_allocation():
    msg=""
    cursor =get_db()
    data=cursor.execute('SELECT crop_id, Crop_Name,Crop_Quantity FROM crop_allocation WHERE User_id = ? ', (session['id'],))
    info = data.fetchall()
    if len(info)==0:
        msg="Sorry, no data found!!!"
    data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('crop_allocation/crop_allocation.html', **data)

# 4 - seed route - to display all seeds data 
@app.route('/seed')
def seed():
    msg=""
    cursor = get_db()
    data=cursor.execute('SELECT Seed_Id,Seed_Name,Quantity,Seed_Price,Crop_Name FROM seed WHERE User_id = ? ', (session['id'],))
    info = data.fetchall()
    if len(info)==0:
        msg="Sorry, no data found!!!"
    data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('seed/seed.html', **data)

# 5 - pesticide route - to display all pesticides data
@app.route('/pesticide')
def pesticide():
    msg=""
    cursor = get_db()
    data=cursor.execute('SELECT * FROM pesticide WHERE User_id = ? ', (session['id'],))
    info = data.fetchall()
    if len(info)==0:
        msg="Sorry, no data found!!!"
    data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('pesticide.html', **data)

# 6 - fertilizers route - to display all fertilizers data
@app.route('/fertilizer')
def fertilizer():
    msg=""
    cursor = get_db()
    data=cursor.execute('SELECT Fertilizer_Id,Fertilizer_Name ,Quantity ,Fertilizer_Price ,Crop_Name FROM fertilizer WHERE User_id = ? ', (session['id'],))
    info = data.fetchall()
    if len(info)==0:
        msg="Sorry, no data found!!!"
    data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('fertilizer/fertilizer.html', **data)

# 7 - labour route - to display all labours data
@app.route('/labour')
def labour():
    msg=""
    cursor = get_db()
    data=cursor.execute('SELECT * FROM labour WHERE User_id = ? ', (session['id'],))
    info = data.fetchall()
    if len(info)==0:
        msg="Sorry, no data found!!!"
    data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('labour.html', **data)

# 8 - warehouse route - to display all warehouses data where crops are stored
@app.route('/warehouse')
def warehouse():
    msg=""
    cursor = get_db()
    data=cursor.execute('SELECT * FROM warehouse WHERE User_id = ? ', (session['id'],))
    info = data.fetchall()
    if len(info)==0:
        msg="Sorry, no data found!!!"
    data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('warehouse.html', **data)

# 9 - crop_market route - to display all markets data where crops are sold
@app.route('/crop_market')
def crop_market():
    msg=""
    cursor = get_db()
    data=cursor.execute('SELECT * FROM crop_market WHERE User_id = ? ', (session['id'],))
    info = data.fetchall()
    if len(info)==0:
        msg="Sorry, no data found!!!"
    data = {'user_id': session['id'], 'msg': msg, 'info': info}
    return render_template('crop_market.html', **data)

# delete route - to delete any entry or account
@app.route("/delete", methods = ['GET', 'POST'])
def delete():
    msg = ''
    if request.method == "POST":

        # getting value that will be deleted
        name = list(request.form)[0]
        value = request.form[name]
        column, table = name.split('+')

        # deleting value from respected table
        sql = "DELETE FROM " + table + " WHERE " + column + " = '" + value + "'"
        cursor = get_db()
        cursor.execute(sql)
        cursor.commit()

        if (table != 'farmer'):
            return redirect(table)

        # only user is deleted not data
        msg = 'User Deleted!!!'
    return render_template('login.html', msg = msg)



# update route - to get old data for update
@app.route("/update_farm", methods = ['GET', 'POST'])
def update_farm():
    msg = ''
    if request.method == 'POST':

        # getting all old values to update them with new values
        name = list(request.form.to_dict())[0]
        column_id = request.form[name]
        column, table = name.split('+')
        sql = "SELECT  Farm_Acre,Farm_Location,Irrigation_Source FROM " + table + " WHERE " + column + " = '" + column_id + "'"
        cursor = get_db()
        data=cursor.execute(sql)
        info = [dict(row) for row in data.fetchall()]

        data = {'info':info[0], 'user_id': session['id'], 'table': table, 'id': column_id, 'column':column}
        return render_template('Farm/update_farm.html', **data)
    return render_template('login.html', msg = msg)


# update route - to get old data for update
@app.route("/update_fertilizer", methods = ['GET', 'POST'])
def update_fertilizer():
    msg = ''
    if request.method == 'POST':

        # getting all old values to update them with new values
        name = list(request.form.to_dict())[0]
        column_id = request.form[name]
        column, table = name.split('+')
        sql = "SELECT Fertilizer_Name,Quantity,Fertilizer_Price,Crop_Name FROM " + table + " WHERE " + column + " = '" + column_id + "'"
        cursor = get_db()
        data=cursor.execute(sql)
        info=[dict(row) for row in data.fetchall()]
        data = {'info':info[0], 'user_id': session['id'], 'table': table, 'id': column_id, 'column':column}
        return render_template('fertilizer/update_fertilizer.html', **data)
    return render_template('login.html', msg = msg)

@app.route("/update_crop_allocation", methods = ['GET', 'POST'])
def update_crop_allocation():
    msg = ''
    if request.method == 'POST':

        # getting all old values to update them with new values
        name = list(request.form.to_dict())[0]
        column_id = request.form[name]
        column, table = name.split('+')
        sql = "SELECT  Crop_Name,Crop_Quantity  FROM " + table + " WHERE " + column + " = '" + column_id + "'"
        cursor = get_db()
        data=cursor.execute(sql)
        info = [dict(row) for row in data.fetchall()]
        data = {'info':info[0], 'user_id': session['id'], 'table': table, 'id': column_id, 'column':column}
        return render_template('crop_allocation/update_crop_allocation.html', **data)
    return render_template('login.html', msg = msg)


# update route - to get old data for update
@app.route("/update_seed", methods = ['GET', 'POST'])
def update_seed():
    msg = ''
    if request.method == 'POST':

        # getting all old values to update them with new values
        name = list(request.form.to_dict())[0]
        column_id = request.form[name]
        column, table = name.split('+')
        sql = "SELECT  Seed_Name,Quantity,Seed_Price,Crop_Name FROM " + table + " WHERE " + column + " = '" + column_id + "'"
        cursor = get_db()
        data=cursor.execute(sql)
        info = [dict(row) for row in data.fetchall()]
        data = {'info':info[0], 'user_id': session['id'], 'table': table, 'id': column_id, 'column':column}
        return render_template('Farm/update_farm.html', **data)
    return render_template('login.html', msg = msg)
# update_confirm - to update with new data
@app.route("/update_confirm", methods = ["GET", "post"])
def update_confirm():
    msg = ""
    if request.method == "POST":
        # getting new data to update
        name = request.form.to_dict()
        table, column = list(name.keys())[-1].split('+')
        column_id = list(name.values())[-1]
        info = dict(list(name.items())[:-1])

        q1 = "UPDATE " + table
        q2 = " SET "
        for key, value in info.items():
            
            # to solve conversion error
            try:
                temp = float(value)
                if int(temp) / temp == 1 or temp / int(temp) > 1:
                    pass
            except ValueError:
                value = "'" + value + "'"
            q2 = q2 + key +" = " + value + ", "
        q2 = q2[:-2]
        q3 = " WHERE " + column + " = '" + column_id + "'"
        sql = q1 + q2 + q3
        # update old data with new data
        cursor = get_db()
        cursor.execute(sql)
        cursor.commit()
        return redirect(table)
    return render_template("login.html", msg = msg) 

# add route - to get table, column names to add
@app.route("/add_farm", methods=['GET', 'POST'])
def add_farm():
    msg = ''
    if request.method == 'POST':
        # getting table name
        table = request.form.get('table')

        # fetching column names using PRAGMA table_info
        cursor = get_db()
        data=cursor.execute("PRAGMA table_info({})".format(table))
        columns = data.fetchall()
        column_names = [column[1] for column in columns if column[1] not in ['User_id']]
        if not  column_names:
            column_names=["Farm_Acre","Farm_Location","Irrigation_Source"]
        if not table:
            table="farm"
        data = {"columns": column_names, "table": table, "user_id": session['id']}
        return render_template('Farm/add_farm.html', **data)

    return render_template('login.html', msg=msg)

@app.route("/add_seed", methods=['GET', 'POST'])
def add_seed():
    msg = ''
    if request.method == 'POST':
        # getting table name
        table = request.form.get('table')

        # fetching column names using PRAGMA table_info
        cursor = get_db()
        data=cursor.execute("PRAGMA table_info({})".format(table))
        columns = data.fetchall()
        column_names = [column[1] for column in columns if column[1] not in ['User_id']]
        if not  column_names:
            column_names=["Seed_Name","Quantity","Seed_Price","Crop_Name"]
        if not table:
            table="seed"
        data = {"columns": column_names, "table": table, "user_id": session['id']}
        return render_template('seed/add_seed.html', **data)

    return render_template('login.html', msg=msg)
@app.route("/add_fertilizer", methods=['GET', 'POST'])
def add_fertilizer():
    msg = ''
    if request.method == 'POST':
        # getting table name
        table = request.form.get('table')

        # fetching column names using PRAGMA table_info
        cursor = get_db()
        data=cursor.execute("PRAGMA table_info({})".format(table))
        columns = data.fetchall()
        column_names = [column[1] for column in columns if column[1] not in ['User_id']]
        if not  column_names:
            column_names=["Fertilizer_Name","Quantity","Fertilizer_Price","Crop_Name"]
        if not table:
            table="fertilizer"
        data = {"columns": column_names, "table": table, "user_id": session['id']}
        return render_template('fertilizer/add_fertilizer.html', **data)

    return render_template('login.html', msg=msg)

@app.route("/add_crop_allocation", methods=['GET', 'POST'])
def add_crop_allocation():
    msg = ''
    if request.method == 'POST':
        # getting table name
        table = request.form.get('table')

        # fetching column names using PRAGMA table_info
        cursor = get_db()
        data=cursor.execute("PRAGMA table_info({})".format(table))
        columns = data.fetchall()
        column_names = [column[1] for column in columns if column[1] not in ['User_id']]
        if not  column_names:
            column_names=["Crop_Name","Crop_Quantity"]
        if not table:
            table="crop_allocation"
        data = {"columns": column_names, "table": table, "user_id": session['id']}
        return render_template('crop_allocation/add_crop_allocation.html', **data)

    return render_template('login.html', msg=msg)

# add_confirm - to add new data
@app.route("/add_confirm", methods = ['GET', 'POST'])
def add_confirm():
    msg = ''
    if request.method == 'POST':

        # getting new data
        name = request.form.to_dict()
        table = list(name.keys())[-1]
        temp = list(name.items())[:-1]
        columns = dict(temp)

        q1 = "INSERT INTO " + table + "("
        q2 = " VALUES ("
        for key, value in columns.items():

            # to solve conversion error
            try:
                temp = float(value)
                if int(temp)/temp == 1 or temp/int(temp) > 1:
                    pass
            except ValueError:
                value = "'" + value + "'"
            q1 = q1 + key + ", "
            q2 = q2 + value + ", "
        q1 = q1 + "User_id )"
        q2 = q2 + "'" + session['id'] + "' )"

        # add new data in our database
        sql = q1 + q2
        cursor = get_db()
        cursor.execute(sql)
        cursor.commit()
        return redirect(table)
    return render_template('login.html', msg = msg)

# to calulate sum
def calculate_total(d):
    total = 0
    for v in d:
        total += list(v.values())[0]
    return(total)

# profit_loss_overall route - to caluculate overall profit-loss
@app.route('/profit_loss_overall', methods=['GET', 'post'])
def profit_loss_overall():
    msg=''

    # getting selling prices of every crop and all expences and calculating its sum
    sql1 = "SELECT selling_price FROM crop_market WHERE User_id = '" + session['id'] + "' "
    cursor = get_db()
    data=cursor.execute(sql1)
    total_sp = data.fetchall()
    total_sp = calculate_total(total_sp)
    
    q1 = "SELECT seed_price FROM seed WHERE User_id = '" + session['id'] + "' "  
    cursor = get_db()
    data=cursor.execute(q1)
    exp1 = data.fetchall()
    exp1 = calculate_total(exp1)
    
    q2 = "SELECT pesticide_price FROM pesticide WHERE User_id = '" + session['id'] + "' "
    cursor = get_db()
    data=cursor.execute(q2)
    exp2 = data.fetchall()
    exp2 = calculate_total(exp2)

    q3 = "SELECT fertilizer_price FROM fertilizer WHERE User_id = '" + session['id'] + "' "
    cursor = get_db()
    data=cursor.execute(q3)
    exp3 = data.fetchall()
    exp3 = calculate_total(exp3)

    q4 = "SELECT salary FROM labour WHERE User_id = '" + session['id'] + "' "
    cursor = get_db()
    data=cursor.execute(q4)
    exp4 = data.fetchall()
    exp4 = calculate_total(exp4)

    total_exp = exp1 + exp2 + exp3 + exp4
    values = [exp1, exp2, exp3, exp4]
    data = {'user_id': session['id'], 'msg': msg, 'values': values, 'total_exp': total_exp, 'sp': total_sp, 'color': 'primary'}

    if (total_sp - total_exp) > 0:
        data['color'] = 'success'
    elif (total_sp - total_exp) < 0:
        data['color'] = 'danger'

    return render_template('profit.html', **data)

# cropwise route - give crop name to calculate profit-loss
@app.route('/cropwise', methods = ['GET', 'post'])
def cropwise():
    return render_template("cropwise.html", user_id = session['id'])

# profit_loss_cropwise - to calculate cropwise profit-loss 
@app.route('/profit_loss_cropwise', methods = ['GET', 'post'])
def profit_loss_cropwise():
    msg = ''
    if request.method == 'POST':
        crop_name = request.form['crop_name']

        # getting selling prices of every crop and all expences and calculating its sum
        sql1 = "SELECT selling_price FROM crop_market WHERE User_id = '" + session['id'] + "' " + " AND crop_name = '" + crop_name + "' "
        cursor = get_db()
        data=cursor.execute(sql1)
        sp = data.fetchall()
        sp = calculate_total(sp)

        q1 = "SELECT seed_price FROM seed WHERE User_id = '" + session['id'] + "' " + " AND crop_name = '" + crop_name + "' " 
        cursor = get_db()
        data=cursor.execute(q1)
        exp1 = data.fetchall()
        exp1 = calculate_total(exp1)
        
        
        q2 = "SELECT pesticide_price FROM pesticide WHERE User_id = '" + session['id'] + "' " + " AND crop_name = '" + crop_name + "' "
        cursor = get_db()
        data=cursor.execute(q2)
        exp2 = data.fetchall()
        exp2 = calculate_total(exp2)
        

        q3 = "SELECT fertilizer_price FROM fertilizer WHERE User_id = '" + session['id'] + "' " + " AND crop_name = '" + crop_name + "' "
        cursor = get_db()
        data=cursor.execute(q3)
        exp3 = data.fetchall()
        exp3 = calculate_total(exp3)
        
        total_exp = exp1 + exp2 + exp3
        values = [exp1, exp2, exp3]
        data = {'user_id': session['id'], 'msg': msg, 'values': values, 'total_exp': total_exp, 'sp': sp, 'color': 'primary'}

        if (sp - total_exp) > 0:
            data['color'] = 'success'
        elif (sp - total_exp) < 0:
            data['color'] = 'danger'
        return render_template('profit.html', **data)
    return render_template('login.html', msg = msg)



if __name__=="__main__":
    init_db()
    app.run(debug=True)