from flask import session, render_template, flash, redirect, url_for, request
from app import db
from flask_login import current_user, login_required
from app.models import User, Game
from app.main import bp
from app.main.forms import EditProfileForm, CreateGameForm, SelectGameForm
from sqlalchemy import or_


teams = {'Cardinals': 1, 'Falcons': 2, 'Ravens': 3, 'Bills': 4, 'Panthers': 5,
         'Bears': 6, 'Bengals': 7, 'Browns': 8, 'Cowboys': 9, 'Broncos': 10,
         'Lions': 11, 'Packers': 12, 'Texans': 13, 'Colts': 14, 'Jaguars': 15,
         'Chiefs': 16, 'Chargers': 17, 'Rams': 18, 'Dolphins': 19,
         'Vikings': 20, 'Patriots': 21, 'Saints': 22, 'Giants': 23, 'Jets': 24,
         'Raiders': 25, 'Eagles': 26, 'Steelers': 27, '49ers': 28,
         'Seahawks': 29, 'Buccaneers': 30, 'Titans': 31, 'Redskins': 32}


def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form, user=current_user)


@bp.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    form = CreateGameForm()
    if form.validate_on_submit():
        away_id = form.away_id.data
        home_id = form.home_id.data
        try:
            away_id = teams[away_id]
            home_id = teams[home_id]
        except KeyError:
            flash('Invalid team name')
            return redirect(url_for('main.create_game'))
        game = Game(week=form.week.data, away_id=away_id,
                    away_value=form.away_value.data, home_id=home_id,
                    home_value=form.home_value.data)
        db.session.add(game)
        db.session.commit()
        flash('A new game has been created')
        return redirect(url_for('main.create_game'))
    return render_template('create_game.html', title='Create Game', form=form,
                           user=current_user)


@bp.route('/select_game', methods=['GET', 'POST'])
@login_required
def select_game():
    form = SelectGameForm()
    if form.validate_on_submit():
        return redirect(url_for('main.edit_game', week=form.week.data,
                                team=form.team.data))
    return render_template('select_game.html', user=current_user, form=form)


@bp.route('/edit_game/<week>/<team>', methods=['GET', 'POST'])
@login_required
def edit_game(week, team):
    form = CreateGameForm()
    try:
        id = teams[team]
    except KeyError:
        flash('Invalid team name')
        return redirect(url_for('main.select_game'))
    # try/except - 'Game does not exist'
    game = Game.query.filter_by(week=week).filter(or_(
        Game.home_id == id, Game.away_id == id)).first()
    home = getKeysByValue(teams, game.home_id)
    away = getKeysByValue(teams, game.away_id)
    form.week.data = game.week
    form.home_id.data = home[0]
    form.home_value.data = game.home_value
    form.away_id.data = away[0]
    form.away_value.data = game.away_value
    if form.validate_on_submit():
        away_id = form.away_id.data
        home_id = form.home_id.data
        winner_id = form.winner_id.data
        try:
            away_id = teams[away_id]
            home_id = teams[home_id]
            if len(winner_id) > 0:
                winner_id = teams[winner_id]
        except KeyError:
            flash('Invalid team name')
            return redirect(url_for('main.select_game'))

        game.week = form.week.data
        game.away_id = away_id
        game.away_value = form.away_value.data
        game.home_id = home_id
        game.home_value = form.home_value.data
        game.winner_id = winner_id
        db.session.add(game)
        db.session.commit()
        flash('Game successfully edited')
        return redirect(url_for('main.select_game'))
    return render_template('edit_game.html', user=current_user, form=form,
                           game=game)
