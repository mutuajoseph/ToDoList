from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

DB_URL = "postgresql://postgres:Jose.2018@127.0.0.1:5432/todo"

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='some-secret-string'

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

    # Create
    def create_user(self):
        db.session.add(self)
        db.session.commit()

        # Delete

    @classmethod
    def delete_by_id(cls, id):
        record = Todo.query.filter_by(id=id)

        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False

@app.before_first_request
def createTables():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        taskContent = request.form['content']
        newTask = Todo(content=taskContent)

        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'Error Message'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    task_to_delete = Todo.delete_by_id(id)
    if task_to_delete:
        
        return redirect(url_for('home'))
    else:
        
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)