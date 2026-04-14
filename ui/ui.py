def get_current_user(data):
    if not data['session']['current_user']:
        return None
    else:
        user = data['session']['current_user']
        return user

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




def render_header(current_user):
    user = current_user['username'] if current_user else 'Nenhum usuário logado'
    status = 'Logado' if current_user else 'Deslogado'
    print ('===============')
    print ('PAINEL DE CONTROLE')
    print (f'Usuário:   {user}')
    print (f'Status:    {status}')
    print ('===============')




