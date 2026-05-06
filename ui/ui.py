from utils.session import get_current_user
from services.auth_service import (login,
                                   logout,
                                   validate_username_for_register,
                                   validate_username_for_login,
                                   validate_remove_user,
                                   validate_password_for_register,
                                   normalize_username,
                                   )
from services.user_service import (register_user,
                                   list_users,
                                   unblock_user,
                                   remove_user
                                   )
from constants import (USER_NOT_FOUND,
                       SUCCESS,
                       NO_USER_LOGGED,
                       INVALID_USERNAME,
                       USERNAME_ALREADY_EXISTS,
                       BLOCKED,
                       INVALID_PASSWORD,
                       EMPTY_LIST,
                       TRY_AGAIN_LATER,
                       USER_LIST,
                       USER_NOT_BLOCKED,
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

    username = input('Digite seu nome de usuário: ')
    username = normalize_username(username)
    result,_ = validate_username_for_login(data,username)
    action = {
        BLOCKED: lambda: print('Usuário bloqueado.\n'),
        INVALID_USERNAME: lambda: print ('Nome inválido, o nome deve conter somente letras e ser maior que 3 caracteres.\n'),
        EMPTY_LIST: lambda: print ('Lista de usuários vazia.\n'),
        USER_NOT_FOUND: lambda: print ('Usuário não cadastrado.\n'),
    }
    if result in action:
        action[result]()
        return


    while True:
        password = input('Digite sua senha: ').strip()
        result, attempts = login(data, username, password)

        if result == SUCCESS:
            print('Login realizado com sucesso.\n')
            break

        elif result == BLOCKED:
            print('Usuário bloqueado por excesso de tentativas.')
            break

        elif result == INVALID_PASSWORD:
            print (f'Senha inválida. Tentativa {attempts} de 3.\n')
            continue




    ###############################################################

def logout_ui(data):
    option = input('Tem certeza que deseja sair? [S/N]').strip().lower()

    if option == 's':
        result = logout(data)
        if result == NO_USER_LOGGED:
            print ('Faça login primeiro.\n')
            return

        elif result == SUCCESS:
            print ('Logout realizado com sucesso.\n')
            return
    else:
        print ('Usuário continua logado.\n')
        return

    ###############################################################

def register_user_ui(data):

    username = input('Digite o nome de usuário: ')
    username = normalize_username(username)
    result,_ = validate_username_for_register(data,username)
    actions = {
        USERNAME_ALREADY_EXISTS: lambda: print ('Nome de usuário já cadastrado\n'),
        INVALID_USERNAME: lambda: print ('Nome inválido, o nome deve conter somente letras e ser maior que 3 caracteres.\n'),

    }
    if result in actions:
        actions[result]()
        return

    password = input('Digite sua senha: ').strip()
    result,_ = validate_password_for_register(password)
    if result == INVALID_PASSWORD:
        print ('Senha inválida, a senha deve ser maior ou igual a 4 caracteres.\n')
        return

    result,_ = register_user(data, username, password)
    actions = {
        SUCCESS: lambda: print ('Usuário cadastrado com sucesso.\n'),
        TRY_AGAIN_LATER: lambda: print ('Tente novamente mais tarde.\n'),

    }
    if result in actions:
        actions[result]()

    ###############################################################

def list_users_ui(data):
    result,users = list_users(data)
    if result == EMPTY_LIST:
        print ('Lista de usuários vazia.\n')
        return
    if result == USER_LIST:
        for i, user in enumerate(users, start=1):
            status = 'ATIVO' if not user['blocked'] else 'BLOQUEADO'
            print(f"\n{i} - Usuário: {user['username']} | Status: {status}")

    ###############################################################

def unblock_user_ui(data):
    username = input('Digite o nome de usuário: ').strip().lower()
    result,_ = unblock_user(data,username)

    actions = {
        EMPTY_LIST: lambda: print ('Lista de usuários vazia.\n'),
        USER_NOT_FOUND: lambda: print ('Usuário não cadastrado.\n'),
        USER_NOT_BLOCKED: lambda: print ('Usuário não bloqueado.\n'),
        SUCCESS: lambda: print (f'Usuário {username} desbloqueado com sucesso.\n')
    }

    if result in actions:
        actions[result]()

    ###############################################################

def remove_user_ui(data):

    username = input('Digite o nome de usuário: ').strip().lower()
    result,_ = validate_remove_user(data,username)
    actions = {
        EMPTY_LIST: lambda: print ('Lista de usuários vazia.\n'),
        USER_NOT_FOUND: lambda: print ('Usuário não cadastrado.\n')
    }

    if result in actions:
        actions[result]()
        return

    option = input(f"Tem certeza que deseja excluir o usuário PERMANENTEMENTE? (S/N)\n").lower()
    if option not in ['s','sim']:
        print ('Operação cancelada.\n')
        return

    result,_ = remove_user(data, username)

    if result == SUCCESS:
        print('Usuário excluido com sucesso.\n')
        return
