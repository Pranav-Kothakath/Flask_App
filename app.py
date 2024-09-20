from flask import Flask, redirect, render_template, request
# import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Procfile to let Horoku know that we are using gnuicon
# -------------------------------------------------------------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# initialize the database
db = SQLAlchemy(app)

#create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    #Create a function to return a string when we add something
    def __repr__(self):
        return f'<Friend {self.name}>'
    
subscribers = []

# -------------------------------------------------------------------------------------

@app.route('/')
def index():
    title = "Pranav's Portfolio"
    return render_template("index.html", title = title) 

# -------------------------------------------------------------------------------------


@app.route('/about')
def about():
    names = [1,2,3,4,5,6,7]
    return render_template("about.html", names = names)

# -------------------------------------------------------------------------------------

@app.route('/contacts')
def contacts():
    return render_template("contacts.html")

# --------------------------------------------------------------------------------------

@app.route('/form', methods = ['POST']) 
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")

    # message = "We have received your credatials. We'll reach out to you soon."
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # #server.login("pranav@gmail.com", os.getenv("PASSWORD"))
    # server.login("pranav@gmail.com", "PASSWORD")
    # server.sendmail("pranav@gmail.com", email, message)

    if not first_name or not last_name or not email:
        err_msg = 'All fields required.'
        return render_template("contacts.html", err_msg = err_msg, first_name=first_name, last_name=last_name, email=email)
    subscribers.append(f'{first_name} {last_name} | {email}')
    return render_template("form.html" , subscribers=subscribers)

# ------------------------------------------------------------------------------------

@app.route('/friends', methods=['POST', 'GET'])
def friends():
    if request.method == 'POST':
        friend_name = request.form['name'] 
        new_friend = Friends(name = friend_name)
        #push to db
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error while adding your friend..."
    else:
        friends = Friends.query.order_by(Friends.date)  
        return render_template("friends.html", friends=friends)
    
# ---------------------------------------------------------------------------------------    
    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == 'POST':
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "Problem occured while updating..."
    else:
        return render_template('update.html', friend_to_update=friend_to_update)

# ---------------------------------------------------------------------------------------

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "Error occured while deleting..."

# ---------------------------------------------------------------------------------------
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
