from app import app
from flask import render_template, request, redirect, session

from app.forms import JustNickForm, SignInForm, SignUpForm, ConfirmForm, NewChatForm, SettingsForm, MessageForm
import app.database_functions as db_func



@app.route('/', methods = ['GET', 'POST'])
@app.route('/welcome', methods = ['GET', 'POST'])
def welcome():
    form = JustNickForm()

    if form.validate_on_submit():
        session['nickname'] = form.nickname.data
        # TODO redirect to signin if nickname is in db else signup

        return redirect('/signin')

    if 'nickname' in session:
        signed_up=True if session['nickname'] == 'sup' else False
        del session['nickname']
    else:
        signed_up = False
    return render_template('welcome_page.html', form=form, signed_up=signed_up)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()

    if form.validate_on_submit():
        # TODO login
        return redirect('/chats')

    if 'nickname' in session:
        return render_template('signin_page.html', form=form, nickname=session['nickname'])
    else:
        return redirect('/')


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        db_func.create_new_user(session['nickname'], form.password.data)
        session['nickname'] = 'sup'
        return redirect('/welcome')

    if 'nickname' in session:
        return render_template('signup_page.html', form=form, nickname=session['nickname'])
    else:
        return redirect('/')


@app.route('/chats')
def chats():
    user = 'Arseniy'
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


@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
    form = MessageForm()
    if form.validate_on_submit():
        print(f"Sended message: {form.message.data}")

    dialog_user = 'Emma'
    messages = [
        {
            'is_received': True,
            'text': 'Привет)',
        },
        {
            'is_received': False,
            'text': 'Привет))',
        },
    ]
    return render_template('chat_page.html', dialog_user=dialog_user, messages=reversed(messages), form=form)


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    form=ConfirmForm()
    if form.validate_on_submit():
        print(f"Confirm password: {request.form['confirm_password']}")
        return redirect('/chats')
    return render_template('confirm_page.html', form=form)


@app.route('/newchat')
def newchat():
    form = NewChatForm()
    query = request.args.get('query')
    if query == None:
        query = ''
    
    found_users = [
        {
            'nickname': 'Arseniy',
            'chat_id': '1234'
        },
        {
            'nickname': 'Nikita',
            'chat_id': '123456'
        }
    ]

    return render_template('newchat_page.html', query=query, found_users=found_users, form=form)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        print(f"New nickname: {form.new_nickname.data}")
        print(f"New password: {form.new_password.data}")
        print(f"Confirm new password: {form.confirm_new_password.data}")
        return redirect('/confirm')
    return render_template('settings_page.html', form=form)