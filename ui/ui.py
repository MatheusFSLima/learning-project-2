def get_current_user(data):
    if not data['session']['current_user']:
        return None
    else:
        user = data['session']['current_user']
        return user

def get_current_username(data):
    if not data['session']['current_user']:
        return None
    else:
        user = data['session']['current_user']
        return user.get('username')

def render_user_menu():
    print ('=== MENU DE USUÁRIO ===')
    print ('1 - Listar usuários')
    print ('2 - Desbloquear usuários')
    print ('3 - Remover usuário')
    print ('4 - Logout')
    print ('0 - Sair do programa')

def render_main_menu():
    print ('=== MENU DE LOGIN ===')
    print('1 - Cadastrar usuário')
    print('2 - Login')
    print('0 - Sair do programa')




def render_header(data):
    current_user = get_current_user(data)
    current_username = get_current_username(data)
    user = 'Sem usuários logados' if not current_user else current_username
    status = 'Logado' if current_user else 'Deslogado'
    print ('===============')
    print ('PAINEL DE CONTROLE')
    print (f'Usuário:   {user}')
    print (f'Status:    {status}')
    print ('===============')




