def get_current_user(data):
    return data['session']['current_user']

def set_current_user(data,user):
    data['session']['current_user'] = user

def clear_session(data):
    data['session']['current_user'] = None