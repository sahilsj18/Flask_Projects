# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, User, Tournament
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    coach = db.Column(db.String(100))
    played = db.Column(db.Integer, default=0)
    won = db.Column(db.Integer, default=0)  
    drawn = db.Column(db.Integer, default=0)
    lost = db.Column(db.Integer, default=0)
    goals_for = db.Column(db.Integer, default=0)
    goals_against = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer)
    position = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    goals = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team1_score = db.Column(db.Integer, default=0)
    team2_score = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(100))
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    team1 = db.relationship('Team', foreign_keys=[team1_id], backref='home_matches')
    team2 = db.relationship('Team', foreign_keys=[team2_id], backref='away_matches')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  
        flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def user_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/teams')
def teams():
    teams = Team.query.all()
    return render_template('teams.html')


@app.route('/teams/add', methods=['GET', 'POST'])
def add_team():

    if request.method == 'POST':
        name = request.form.get('name')
        coach = request.form.get('coach')
        
        if name:
            new_team = Team(name=name, coach=coach)
            db.session.add(new_team)
            db.session.commit()
            return redirect(url_for('teams'))
    
    return render_template('add_team.html')


@app.route('/fixtures')
def fixtures():
    matches = Match.query.all()
    return render_template('fixtures.html', matches=matches)

@app.route('/fixtures/add', methods=['GET', 'POST'])
def add_fixture():
    if request.method == 'POST':
        # Retrieve form data
        team1_id = request.form.get('team1_id')
        team2_id = request.form.get('team2_id')
        date = request.form.get('date') 
        venue = request.form.get('venue')
        
        
        match_date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        
        # Create a new Match object
        new_match = Match(
            team1_id=team1_id,
            team2_id=team2_id,
            date=match_date,
            venue=venue,
            is_completed=False
        )
        
        # Save to the database
        db.session.add(new_match)
        db.session.commit()
        
        return redirect(url_for('fixtures'))
    
    # Fetch teams for the dropdowns
    teams = Team.query.all()
    return render_template('add_fixture.html', teams=teams)

@app.route('/fixtures/update_score/<int:match_id>', methods=['GET', 'POST'])
def update_score(match_id):
    match = Match.query.get_or_404(match_id)
    if request.method == 'POST':
        match.team1_score = request.form.get('team1_score', type=int)
        match.team2_score = request.form.get('team2_score', type=int)
        match.is_completed = True
        db.session.commit()
        return redirect(url_for('fixtures'))
    
    return render_template('update_score.html', match=match)

@app.route('/results')
def results():
    completed_matches = Match.query.filter_by(is_completed=True).all()
    return render_template('results.html', matches=completed_matches)

@app.route('/standings')
def standings():
    teams = Team.query.order_by(Team.points.desc()).all()
    return render_template('standing.html', teams=teams)



# Create the database tables
def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()  # Initialize database tables
    app.run(debug=True)