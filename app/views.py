from flask.helpers import url_for
from app import app
from flask import render_template, request, redirect, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

from app.forms import JustNickForm, SignInForm, SignUpForm, ConfirmForm, NewChatForm, SettingsForm, MessageForm
import app.database_functions as db_func
import app.models as models

from app.userlogin import UserLogin



@app.login_manager.user_loader
def load_user(user_id):
    return UserLogin(db_func.get_user_by_id(user_id))


@app.route('/', methods = ['GET', 'POST'])
@app.route('/welcome', methods = ['GET', 'POST'])
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('chats'))

    form = JustNickForm()

    if form.validate_on_submit():
        session['nickname'] = form.nickname.data
        user = db_func.get_user_by_nickname(form.nickname.data)
        if isinstance(user, models.User) :
            return redirect('/signin')
        elif user == -1:
            flash("Database error.", 'error')
        else:
            return redirect('/signup')

    return render_template('welcome_page.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('chats'))

    form = SignInForm()

    if form.validate_on_submit():
        user = db_func.get_user_by_nickname(session['nickname'])
        if user == -1:
            flash("Database error.", "error")
        elif user and check_password_hash(user.password, form.password.data):
            userlogin = UserLogin(user)
            login_user(userlogin, form.rememberme.data)
            return redirect('/chats')
        else:
            flash("Wrong password.", "error")

    if 'nickname' in session:
        return render_template('signin_page.html', form=form, nickname=session['nickname'])
    else:
        return redirect('/')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('chats'))
        
    form = SignUpForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        res_status = db_func.create_new_user(session['nickname'], password_hash)
        del session['nickname']
        flash('You are signed up! Now you can use our Messenger. ', 'success') if res_status == 0 else flash('An error has occurred during signing up. ', 'error')
        return redirect('/welcome')

    if 'nickname' in session:
        return render_template('signup_page.html', form=form, nickname=session['nickname'])
    else:
        return redirect(url_for('welcome'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out. ", 'success')
    return redirect(url_for('welcome'))


@app.route('/chats')
@login_required
def chats():
    user = current_user.get_user().nickname
    chats = [
        {
            'chat_user': 'Emma',
            'chat_id': '1234',
            'last_msg_date': 'today',
            'last_msg_time': '12:20',
            'has_new_msg': True
        },
        {
            'chat_user': 'Andrey',
            'chat_id': '12345',
            'last_msg_date': 'yesterday',
            'last_msg_time': '18:54',
            'has_new_msg': False
        },
    ]
    return render_template('chats_page.html', user=user, chats=chats)


@app.route('/chats/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    form = MessageForm()

    dialog_user = db_func.get_user_by_id(1) # temporarily
    '''dialog_user = db_func.get_user_by_id(user_id)

    if not dialog_user or dialog_user == -1:
        return redirect(url_for('chats'))

    chat = db_func.get_chat_by_users_id(current_user.get_id(), user_id)

    if not chat:
        chat = db_func.create_new_chat(current_user.get_user(), dialog_user)'''

    messages = [
        {
            'is_received': True,
            'text': 'Привет)',
        },
        {
            'is_received': False,
            'text': 'Привет))',
        },
        {
            'is_received': False,
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla viverra feugiat euismod. Cras tempor tempus lobortis. Aliquam viverra porttitor arcu, vel tristique velit egestas ac. Morbi pellentesque diam nulla, porttitor pellentesque mauris tempus ut. Mauris euismod risus nec tortor lacinia, et laoreet ante lobortis. ',
        },
    ]
    return render_template('chat_page.html', dialog_user=dialog_user, messages=reversed(messages), form=form)


@app.route('/confirm', methods=['GET', 'POST'])
@login_required
def confirm():
    form=ConfirmForm()
    if form.validate_on_submit():
        print(f"Confirm password: {request.form['confirm_password']}")
        return redirect('/chats')
    return render_template('confirm_page.html', form=form)


@app.route('/newchat')
@login_required
def newchat():
    user = current_user.get_user().nickname

    form = NewChatForm()

    return render_template('newchat_page.html', user=user, form=form)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        print(f"New nickname: {form.new_nickname.data}")
        print(f"New password: {form.new_password.data}")
        print(f"Confirm new password: {form.confirm_new_password.data}")
        return redirect('/confirm')
    return render_template('settings_page.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('welcome'))


@app.route('/api/usersearch')
@login_required
def api_usersearch():
    query = request.args.get('query')
    offset = request.args.get('offset', type=int)

    found_users = db_func.get_users_by_nickname_query(query, offset=offset, limit=100, order_by_nickname=True)
    found_users_json = []
    for user in found_users:
        found_users_json.append({
            'nickname': user.nickname,
            'id': user.id
            })

    return jsonify(found_users_json)