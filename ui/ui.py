from utils.session import get_current_user
from services.auth_service import (login,
                                   logout,
                                   handle_failed_attempt
                                   )
from services.user_service import (register_user,
                                   get_user_by_username,
                                   list_users,
                                   unblock_user,
                                   remove_user
                                   )

    ###############################################################

def render_user_menu():
    print ('=== MENU DE USUÁRIO ===')
    print ('1 - Listar usuários')
    print ('2 - Desbloquear usuários')
    print ('3 - Remover usuário')
    print ('4 - Logout')
    print ('0 - Sair do programa')

    ###############################################################

def render_main_menu():
    print ('=== MENU DE LOGIN ===')
    print ('1 - Cadastrar usuário')
    print ('2 - Login')
    print ('0 - Sair do programa')

    ###############################################################

def render_header(data):
    user = get_current_user(data)
    current_user = 'Sem usuários logados' if not user else user['username']
    status = 'Logado' if user else 'Deslogado'
    print ('===============')
    print ('PAINEL DE CONTROLE')
    print (f'Usuário:   {current_user}')
    print (f'Status:    {status}')
    print ('===============')

    ###############################################################

def login_ui(data):

    username = input('Digite seu nome de usuário: ').strip().lower()

    if not data['users']:
        print ('Lista de usuários vazia.\n')
        return

    if not username.replace(' ','').isalpha():
        print ('Nome de usuário inválido. \n')
        return

    user = get_user_by_username(data, username)

    if user is None:
        print ('Usuário não cadastrado.\n')
        return

    elif user['blocked']:
        print ('Usuário bloqueado.\n')
        return

    while True:
        password = input('Digite sua senha: ').strip()
        result, attempts = login(data, username, password)

        if result == 'ALREADY_LOGGED':
            print('Login já realizado.\n')
            break

        elif result == 'SUCCESS':
            print('Login realizado com sucesso.\n')
            break

        elif result == 'BLOCKED':
            print(f'Usuário bloqueado por excesso de tentativas.')
            break

        elif result == 'INVALID_PASSWORD':
            print (f'Senha inválida. Tentativa {attempts} de 3.\n')
            continue




    ###############################################################

def logout_ui(data):
    option = input('Tem certeza que deseja sair? [S/N]').strip().lower()

    if option == 's':
        result = logout(data)
        if result == 'NO_USER_LOGGED':
            print ('Faça login primeiro.\n')
        elif result == 'SUCCESS':
            print ('Logout realizado com sucesso.\n')
    else:
        print ('Usuário continua logado.\n')

    ###############################################################

def register_user_ui(data):
    while True:
        username = input('Digite o nome de usuário: ').strip().lower()
        if not username.replace(' ', '').isalpha() or len(username) < 4:
            print ('Nome inválido, o nome deve conter somente letras e ser maior que 3 caracteres.\n')
            return
        user = get_user_by_username(data, username)
        if user:
            print ('Nome de usuário já cadastrado\n')
            return
        break
    attempts = 0
    while True:
        password = input('Digite sua senha: ').strip()
        result = register_user(data, username, password)

        if result == 'SUCCESS':
            print ('Usuário cadastrado com sucesso.\n')
            break
        elif result == 'INVALID_PASSWORD':
            print ('Senha inválida, a senha deve ser maior que 4 caracteres.\n')
            attempts += 1
            if attempts == 3:
                print ('Tente novamente mais tarde.\n')
                break
            continue
        elif result == 'TRY_AGAIN_LATER':
            print ('Tente novamente mais tarde.\n')
            break

    ###############################################################

def list_users_ui(data):
    result = list_users(data)
    if result == 'EMPTY_LIST':
        print ('Lista de usuários vazia.\n')
        return
    if result == 'USER_LIST':
        for i, user in enumerate(data['users'], start=1):
            status = 'ATIVO' if not user['blocked'] else 'BLOQUEADO'
            print(f"\n{i} - Usuário: {user['username']} | Status: {status}")

    ###############################################################

def unblock_user_ui(data):
    username = input('Digite o nome de usuário: ').strip().lower()
    result = unblock_user(data,username)
    if result == 'EMPTY_LIST':
        print ('Lista de usuários vazia.\n')
        return
    elif result == 'USER_NOT_FOUND':
        print ('Usuário não cadastrado.\n')
        return
    elif result == 'USER_NOT_BLOCKED':
        print ('Usuário não bloqueado.\n')
        return
    elif result == 'SUCCESS':
        print (f'Usuário {username} desbloqueado com sucesso.\n')

    ###############################################################

def handle_failed_attempt_ui(data,user):
    result = handle_failed_attempt(data,user)
    if result == 'WRONG_PASSWORD':
        print (f'Senha inválida. Tentativa {user["attempts"]} de 3.')
        return
    if result == 'BLOCKED':
        print ('Usuário bloqueado por tentativas')
        return

    ###############################################################

def remove_user_ui(data):

    if not data['users']:
        print('Lista de usuários vazia.\n')
        return

    username = input('Digite o nome de usuário: ').strip().lower()
    user = get_user_by_username(data, username)

    if user is None:
        print('Usuário não cadastrado.\n')
        return


    option = input(f"Tem certeza que deseja excluir PERMANENTEMENTE o usuário {user['username']}? (S/N)\n").lower()
    if option != 's':
        print ('Operação cancelada.\n')
        return

    result = remove_user(data, username)

    if result == 'SUCCESS':
        print('Usuário excluido com sucesso.\n')
