from datetime import datetime

def add_log(data,username,action,status):
    log = {
        'user': username,
        'action': action,
        'status': status,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    data['logs'].append(log)



