def get_current_user(data):
    session = data.get('session', {})
    return session.get('current_user')

def set_current_user(data,user):
    data['session']['current_user'] = user

def clear_session(data):
    data['session']['current_user'] = None