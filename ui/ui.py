from utils.session import get_current_user
from services.auth_service import (login,
                                   logout,
                                   )
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
    user = get_current_user(data)
    current_user = 'Sem usuários logados' if not user else user['username']
    status = 'Logado' if user else 'Deslogado'
    print ('===============')
    print ('PAINEL DE CONTROLE')
    print (f'Usuário:   {current_user}')
    print (f'Status:    {status}')
    print ('===============')

def login_ui(data):
    username = input('Digite seu nome de usuário: ').strip().title()
    while True:
        password = input('Digite sua senha: ').strip()
        result = login(data, username, password)

        if result == 'SUCCESS':
            print ('Login realizado com sucesso.\n')
            break
        elif result == 'ALREADY_LOGGED':
            print ('Login já realizado.\n')
            break
        elif result == 'INVALID_USERNAME':
            print ('Nome de usuário inválido. \n')
            break
        elif result == 'USER_NOT_FOUND':
            print ('Usuário não cadastrado.\n')
            break
        elif result == 'BLOCKED':
            print ('Usuário bloqueado.\n')
            break
        elif result == 'EMPTY_LIST':
            print('Lista de usuários vazia.\n')
            break
        elif result == 'INVALID_PASSWORD':
            continue

def logout_ui(data):
    option = input('Tem certeza que deseja sair? [S/N]').strip().lower()

    if option == 's':
        result = logout(data)
        if result == 'NO_USER_LOGGED':
            print('Faça login primeiro.\n')
        elif result == 'SUCCESS':
            print('Logout realizado com sucesso.\n')
    else:
        print('Usuário continua logado.\n')




