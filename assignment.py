from flask import Flask,request,render_template,url_for,redirect,make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


users = {
    'Vivek':'123vivek',
    'Manas':'123manas',
    'Payas':'123payas'
}


@auth.verify_password                                             #authentication
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

#DATABASE MODEL
class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    task_detail = db.Column(db.String(200), nullable = False)
    time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"Task: {self.task_id} created by {self.name}"


#ADD TASK POST REQUEST
@app.route('/',methods = ['POST','GET'])
def test():
    if(request.method == 'POST'):
        request_name = request.form['task_name']
        request_details = request.form['details']
        new = Todo(task_detail = request_details, name = request_name)

        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/')
        
        except:
            return f"Something is wrong!"
    
    else:
        return render_template('index.html', tasks = Todo.query.all())


#DELETE TASK
@app.route('/delete/<int:task_id>')
@auth.login_required
def del_func(task_id):
    _id = Todo.query.get_or_404(task_id)

    try:
        db.session.delete(_id)
        db.session.commit()
        return redirect('/')
    
    except:
        return f"There some problem with the deletion."


#UPDATE TASK
@app.route('/update/<int:task_id>',methods = ['POST','GET'])
@auth.login_required
def update(task_id):
    Task = Todo.query.get_or_404(task_id)
    if request.method == 'POST':
        Task.task_detail = request.form['details']
        Task.name = request.form['task_name']

        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return f"There's some error with the updation!"
    else:
        return render_template('update.html',task = Task)



if __name__ == '__main__':
    app.run(debug=True)