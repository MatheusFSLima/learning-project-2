
from utils.json_handler import load_data
from services.user_service import (
    register_user,
    list_users,
    unblock_user,
    remove_user
)
from services.auth_service import login



def show_menu():
    print ('=== SISTEMA ===')
    print ('1 - Cadastrar usuário')
    print ('2 - Login')
    print ('3 - Listar usuários')
    print ('4 - Desbloquear usuários')
    print ('5 - Remover usuário')
    print ('0 - Sair do programa')

def main():
    data=load_data()
    while True:
        show_menu()
        option = input ('Digite a opção desejada: ').strip()
        if option == '1':
            register_user(data)
        elif option == '2':
            login(data)
        elif option == '3':
            list_users(data)
        elif option == '4':
            unblock_user(data)
        elif option == '5':
            remove_user(data)
        elif option == '0':
            break
        else:
            print ('Opção inválida.\n')



if __name__ == "__main__":
    main()