'''
Mino Stoto 
3.12.23
CRN: 23199
CIS 226: Advanced Python Programming
Total time: around 3 hours

This program sets up a database for a user to input data to via a webapp. It begins by declaring the database under vegetables.db.
It declares a Vegetables class that houses the functions for the sqlite database, then sets the database up before any submissions 
can be made to it, which happens between the inputs in the html file and the functions within the Vegetables class. Once a user submits 
an update to the database the input information is checked for validity (that both fields had inputs, and that the quantity field held an integer). 
If both of the validity checks pass, the database is updated with the new information.

I had started writing this with similar intent to your demo, but hadn't done the tutorial yet. After doing the tutorial, I realized that you directly 
showed us all of the techniques I wanted to cover with my app, including the Vegetables class, the flash messages, and error checks. When all was said 
and done, I basically ended up using very very similar code to your demo. I am not certain there is even a better way to handle the flash messages than 
how you suggested. For the secret key I opted to generate it within the program itself by calling the method instead of creating a one-off key. I threw 
bootstrap on the html file for an enhanced visual experience. I tested it throughout its development by attempting to add vegetable/quantity pairs.

To use this program, access it via the web and simply input the data you want to store in the database. Enter a vegetable and a quantity for that
vegetable, then click the add button. The new entry will show up underneath, in a darkened table for visual feedback.
'''


import sqlite3
from flask import Flask, flash, render_template, request, redirect, url_for
import secrets

DB_PATH = 'vegetables.db'

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe() #secret key for cookies

#vegetable class, universally applicable
class Vegetables:
    def __init__(self, conn):
        self.conn = conn
        self.c = self.conn.cursor()
    def setup(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS vegetable (quantity INTEGER, name TEXT)")
        self.conn.commit()
    def get_all_veg(self):
        for row in self.c.execute("SELECT * FROM vegetable"):
            yield row
    def add_veg(self, name, quantity):
        self.c.execute("INSERT INTO vegetable VALUES (?, ?)", [quantity, name])

#sets up the database    
def db_setup():
    with sqlite3.connect(DB_PATH) as conn:
        v = Vegetables(conn)
        v.setup()

#sets the database up before any other request
app.before_first_request(db_setup)

#main page
@app.route('/', methods=['GET', 'POST'])
def main():
    veg = '' #variable for veggie name
    quantity = '' #variable for veggie quant
    valid = False #validity variable
    if request.method == 'POST': #if anything is submitted via the inputs
        veg = request.form.get('veg') #get the submitted veggie name
        quantity = request.form.get('quantity') #get the submitted quantity of the veggie
        valid = True
        if not veg or not quantity: #if neither name or quantity were entered
            flash('Please submit for both fields') #informative error message
            valid = False #invalid, will not post submission
        else:
            try:
                quantity = int(quantity) #checks that quantity is an integer
            except ValueError:
                valid = False #invalid, will not post submission

    with sqlite3.connect(DB_PATH) as conn:
        v = Vegetables(conn) #instantiates the class
        if valid: #checks to see if the form was entered correctly
            v.add_veg(veg, quantity) #then adds them to the database
            flash('{} {}(s) were added to the database'.format(quantity, veg)) #confirmation message
            return redirect(url_for('main')) #refreshes page after submission
        vegetables = v.get_all_veg() #refreshes the vegetable list
    #passes to html file
    return render_template(
        'base.html',
        title="Vegetable Database",
        vegetables=vegetables,
        veg=veg,
        quantity=quantity,
    )


if __name__ == "__main__": #you know
    app.run()