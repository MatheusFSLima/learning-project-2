from services.log_service import add_log
from datetime import datetime
from utils.json_handler import save_data


def get_user_by_username(data,username):
    for user in data['users']:
        if user['username'] == username:
            return user
    return None



def register_user(data):
    username = input('Digite o nome de usuário: ').strip().title()
    if not username.replace(' ', '').isalpha() or len(username) < 4:
        print('Nome inválido, o nome deve conter somente letras e ser maior que 3 caracteres.\n')
        return
    user = get_user_by_username(data,username)
    if user:
        print ('Nome de usuário já cadastrado\n')
        return

    while user['attempts'] < 3:
        password = input('Digite sua senha: ')
        if password.strip() == '' or len(password) < 4:
            add_log(data, username, 'REGISTER', 'FAIL')
            print ('Senha inválida, a senha deve ser maior que 4 caracteres.\n')
            user['attempts'] += 1
            if user['attempts'] == 3:
                print('Tente novamente mais tarde.\n')
                return
            continue
        user = {
            'username':username,
            'password':password,
            'attempts': 0,
            'blocked': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data['users'].append(user)
        add_log(data,username,'REGISTER','SUCCESS')
        save_data(data)
        print ('Usuário cadastrado com sucesso.\n')
        break


def list_users(data):
    if not data['users']:
        print ('Lista de usuários vazia.\n')
        return
    for i,user in enumerate(data['users'],start=1):
        status = 'ATIVO' if not user['blocked'] else 'BLOQUEADO'
        print (f"{i} - Usuário: {user['username']} | Status: {status}\n")


def unblock_user(data):
    if not data['users']:
        print ('Lista de usuários vazia.\n')
        return
    username = input('Digite o nome de usuário: ').strip().title()
    user = get_user_by_username(data, username)
    if user is None:
        print ('Usuário não cadastrado.\n')
        return
    if not user['blocked']:
        print ('Usuário não bloqueado.\n')
        return

    user['blocked'] = False
    add_log(data,username,'UNBLOCK','SUCCESS')
    save_data(data)
    print (f'Usuário {username} desbloqueado com sucesso.\n')


def remove_user(data):
    if not data['users']:
        print('Lista de usuários vazia.\n')
        return
    username = input('Digite o nome de usuário: ').strip().title()
    user = get_user_by_username(data,username)
    if user is None:
        print ('Usuário não cadastrado.\n')
        return
    option = input (f"Tem certeza que deseja excluir PERMANENTEMENTE o usuário {user['username']}? (S/N)\n").lower()
    if option == 'n':
        return
    if option == 's':
        data['users'].remove(user)
        add_log(data,username,'REMOVE','SUCCESS')
        save_data(data)
        print ('Usuário excluido com sucesso.\n')

    else:
        print ('Opção inválida.\n')



