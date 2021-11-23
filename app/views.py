from flask.helpers import url_for
from app import app
from flask import render_template, request, redirect, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

from app.forms import JustNickForm, SignInForm, SignUpForm, ConfirmForm, NewChatForm, SettingsForm, MessageForm
import app.messenger_functions as msgr
import app.models as models

from app.userlogin import UserLogin

from app import socketio
from flask_socketio import emit, join_room, send



@app.login_manager.user_loader
def load_user(user_id):
    return UserLogin(msgr.get_user_by_id(user_id))


@app.route('/', methods = ['GET', 'POST'])
@app.route('/welcome', methods = ['GET', 'POST'])
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('chats'))

    form = JustNickForm()

    if form.validate_on_submit():
        user = msgr.get_user_by_nickname(form.nickname.data)
        if isinstance(user, models.User) :
            if not user.active:
                flash('Account deleted.', category='error')
            else:
                session['nickname'] = user.nickname
                return redirect('/signin')
        elif user == -1:
            flash("Database error.", 'error')
        else:
            session['nickname'] = form.nickname.data
            return redirect('/signup')

    return render_template('welcome_page.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('chats'))

    form = SignInForm()

    if form.validate_on_submit():
        user = msgr.get_user_by_nickname(session['nickname'])
        if user == -1:
            flash("Database error.", "error")
        elif user and not user.active:
            flash("Account deleted.", "error")
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
        res_status = msgr.create_new_user(session['nickname'], password_hash)
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
    c_user = current_user.get_user()

    chats = msgr.get_user_chats(c_user)
    
    chats = [] if chats == -1 else chats

    return render_template('chats_page.html', user=c_user.nickname, chats=chats)


@app.route('/chats/<int:chat_id>')
@login_required
def chat(chat_id:int):
    form = MessageForm()

    chat = msgr.get_chat_by_id(chat_id)
    if not chat or chat == -1 or current_user.get_user() not in chat.users:
        return redirect(url_for('chats'))

    chat_users = chat.users.all()
    chat_users.remove(current_user.get_user())

    chat_name = msgr.make_chat_name(current_user.get_user(), chat)

    return render_template('chat_page.html', chat_name=chat_name, form=form)


@app.route('/chats/u<int:user_id>')
@login_required
def chat_2users(user_id:int):
    form = MessageForm()

    current_user_dbobject = current_user.get_user()
    opponent_user_dbobject = msgr.get_user_by_id(user_id)
    if not opponent_user_dbobject or opponent_user_dbobject == -1:
        return redirect(url_for('chats'))

    chat = msgr.get_chat_by_users(current_user_dbobject, opponent_user_dbobject)
    if not chat or chat == -1:
        chat = msgr.create_new_chat(current_user.get_user(), msgr.get_user_by_id(user_id))

    chat_name = opponent_user_dbobject.nickname

    return render_template('chat_page.html', chat_name=chat_name, form=form)


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
        if not check_password_hash(current_user.get_user().password, form.current_password.data):
            flash('Wrong current password. ', category='confirm_password_error')

        elif form.delete_user.data:
            print(msgr.delete_user(current_user.get_user()))
            print("Delete user")
            logout_user()
            flash('User deleted', category='success')
            return redirect(url_for('welcome'))
        else:
            if form.new_nickname.data:
                msgr.change_user_nickname(current_user.get_user(), form.new_nickname.data)
                print("Change nickanme")
                flash("Nickname successfully changed.", category='data_changed')
            if form.new_password.data:
                msgr.change_user_password(current_user.get_user(), generate_password_hash(form.new_password.data))
                print("Change password")
                flash("Password successfully changed.", category='data_changed')
        
    return render_template('settings_page.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('welcome'))

@app.errorhandler(AttributeError)
def page_not_found(e):
    if not current_user.get_user():
        logout_user()
        return redirect(url_for('welcome'))


@app.route('/api/usersearch')
@login_required
def api_usersearch():
    query = request.args.get('query')
    offset = request.args.get('offset', type=int)

    found_users = msgr.get_users_by_nickname_query(query, offset=offset, limit=100, order_by_nickname=True)
    found_users_json = []
    for user in found_users:
        found_users_json.append({
            'nickname': user.nickname,
            'chat_id': 'u' + str(user.id)
            })

    return jsonify(found_users_json)


@app.route('/api/get_chats')
@login_required
def api_get_messages():
    offset = request.args.get('offset', type=int)

    chats = msgr.get_user_chats(current_user.get_user(), offset=offset, limit=100)

    return jsonify(chats)


@app.route('/api/get_messages')
@login_required
def api_get_chats():
    chat_id = request.args.get('chat_id')
    offset = request.args.get('offset', type=int)

    if chat_id[0] == 'u':
        chat = msgr.get_chat_by_users(current_user.get_user(), msgr.get_user_by_id(chat_id[1:]))
    else:
        chat = msgr.get_chat_by_id(chat_id)

    messages = msgr.get_messages_by_chat(chat, offset=offset, limit=100)
    messages_dicts = [{'is_received': (True if str(message.from_id) != current_user.get_id() else False), 'text': message.text} for message in messages]

    return jsonify(messages_dicts)


@socketio.on('join')
def connect(data):
    if data['chat_id'][0] == 'u':
        chat = msgr.get_chat_by_users(current_user.get_user(), msgr.get_user_by_id(data['chat_id'][1:]))
    else:
        chat = msgr.get_chat_by_id(data['chat_id'])

    if current_user.get_user() in chat.users.all():
        join_room('chat' + str(chat.id))
        emit('current_user_id', {'current_user_id': current_user.get_id()})


@socketio.on('listen_all_chats')
def listen_all_chats():
    join_room('all_chats' + current_user.get_id())


@socketio.on('message')
def message_sent(message):
    chat_id = message['chat_id']
    message_text = message['text']
    print(chat_id, message_text)

    if chat_id[0] == 'u':
        chat = msgr.get_chat_by_users(current_user.get_user(), msgr.get_user_by_id(chat_id[1:]))
    else:
        chat = msgr.get_chat_by_id(chat_id)

    del chat_id

    new_message = msgr.create_new_message(int(current_user.get_id()), chat.id, text=message_text)

    if new_message != -1:
        send({'sender_id': current_user.get_id(), 'text': message_text}, to='chat'+str(chat.id))
        for user in chat.users.all():
            send({
                'chat_name': msgr.make_chat_name(user, chat),
                'chat_id': chat.id,
                'has_new_msg': True,
                **msgr.get_message_data(new_message)
            }, to='all_chats'+str(user.id))
