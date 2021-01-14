from flask import Flask, render_template, request


app = Flask(__name__)



@app.route('/')
@app.route('/login')
def login():
    return render_template('login_page.html')

@app.route('/signup')
def signup():
    return render_template('signup_page.html')

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

@app.route('/chat/<int:chat_id>')
def chat(chat_id):
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
    return render_template('chat_page.html', dialog_user=dialog_user, messages=reversed(messages))

@app.route('/confirm')
def confirm():
    return render_template('confirm_page.html')

@app.route('/newchat')
def newchat():
    query = request.args.get('q')
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

    return render_template('newchat_page.html', query=query, found_users=found_users)

@app.route('/settings')
def settings():
    return render_template('settings_page.html')

'''
@app.route('/<string:filename>')
def index1(filename):
    return render_template(filename)
'''



if __name__ == "__main__":
    app.run(debug=True)