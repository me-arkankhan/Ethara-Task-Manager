from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ethara_ai_secret_9988'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ethara_main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='Member')
    tasks = db.relationship('Task', backref='assignee_details', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(20), default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')
        role = request.form.get('role')

        print("registering:", uname)

        if User.query.filter_by(username=uname).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        hashed = generate_password_hash(pwd)
        new_u = User(username=uname, password_hash=hashed, role=role)
        
        try:
            db.session.add(new_u)
            db.session.commit()
            print("saved to db")
            flash('Account created successfully. Please sign in to continue.', 'success')
            return redirect(url_for('login'))
        except Exception as err:
            print("db error:", err)
            flash('An unexpected server error occurred. Please try again.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usr = request.form.get('username')
        pas = request.form.get('password')
        
        u = User.query.filter_by(username=usr).first()

        if not u:
            print("user mila hi nahi")
            flash("We couldn't find an account with this username. Please register to get started.", 'danger')
        elif not check_password_hash(u.password_hash, pas):
            print("password galat hai")
            flash("Incorrect password. Please try again.", 'danger')
        else:
            login_user(u)
            print("logged in:", usr)
            return redirect(url_for('dashboard'))
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Admin':
        members = User.query.filter_by(role='Member').all()
        all_t = Task.query.all()
        
        t_count = len(all_t)
        c_count = sum(1 for x in all_t if x.status == 'Complete')
        p_count = t_count - c_count
        
        return render_template('dashboard.html', members=members, tasks=all_t, 
                               stats={'total': t_count, 'completed': c_count, 'pending': p_count})
    else:
        my_t = Task.query.filter_by(user_id=current_user.id).all()
        
        t_count = len(my_t)
        c_count = sum(1 for x in my_t if x.status == 'Complete')
        p_count = t_count - c_count
        
        return render_template('dashboard.html', tasks=my_t, 
                               stats={'total': t_count, 'completed': c_count, 'pending': p_count})

@app.route('/api/add_task', methods=['POST'])
@login_required
def api_add_task():
    if current_user.role != 'Admin':
        return jsonify({"status": "error", "message": "Unauthorized access. Admin privileges required."}), 403

    d = request.get_json()
    title = d.get('title')
    prio = d.get('priority', 'Medium')
    uid = d.get('assigned_to')

    if not title or not uid:
        return jsonify({"status": "error", "message": "Please fill in all required fields."}), 400

    t = Task(title=title, priority=prio, user_id=uid)
    
    try:
        db.session.add(t)
        db.session.commit()
        return jsonify({"status": "success", "message": "Task assigned successfully."}), 201
    except Exception as e:
        print("task add error:", e)
        return jsonify({"status": "error", "message": "Internal server error."}), 500

@app.route('/api/complete_task/<int:task_id>', methods=['POST'])
@login_required
def api_complete_task(task_id):
    t = Task.query.get(task_id)
    
    if not t:
        return jsonify({"status": "error", "message": "Task not found."}), 404
        
    if t.user_id != current_user.id and current_user.role != 'Admin':
        return jsonify({"status": "error", "message": "Unauthorized. You can only update your own tasks."}), 403

    t.status = 'Complete'
    db.session.commit()
    return jsonify({"status": "success", "message": "Task marked as complete."}), 200

@app.route('/api/delete_task/<int:task_id>', methods=['DELETE'])
@login_required
def api_delete_task(task_id):
    if current_user.role != 'Admin':
        return jsonify({"status": "error", "message": "Unauthorized. Admin privileges required."}), 403
        
    t = Task.query.get(task_id)
    if not t:
        return jsonify({"status": "error", "message": "Task not found or already deleted."}), 404
        
    db.session.delete(t)
    db.session.commit()
    return jsonify({"status": "success", "message": "Task deleted successfully."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)