from flask import Flask, render_template, request, session, redirect
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
app = Flask(__name__)
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('mydb')
# now, we may invoke the query_db method
print("all the users", mysql.query_db("SELECT * FROM users;"))
app.secret_key = 'Thisissupersecret'
@app.route('/')
def index():
    if 'filtered_name' in session:
        search_query = "SELECT * FROM users WHERE name = %(name)s;"
        search_query_data = {
            "name":session['filtered_name']
        }
        filtered_users = mysql.query_db(search_query, search_query_data)
    else:
        search_query = "SELECT * FROM users;"
        filtered_users = mysql.query_db(search_query)
    return render_template('index.html', users = filtered_users)
    # If you don't want to worry about the search feature, comment lines 13 through 21 and uncomment line 23 and 24 below
    # all_users = mysql.query_db("SELECT * FROM users;")
    # return render_template('index.html', users = all_users)

@app.route('/users', methods=["POST"])
def create():
    query_string = "INSERT INTO users (name) VALUES (%(new_user_name)s);"
    query_data = {
        'new_user_name': request.form['name']
    }
    mysql.query_db(query_string, query_data)
    return redirect('/')

@app.route('/search', methods=["POST"])
def search():
    session['filtered_name'] = request.form['search_name']
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
