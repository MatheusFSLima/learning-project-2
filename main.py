
from utils.json_handler import load_data,clear_data
from services.user_service import (
    register_user,
    list_users,
    unblock_user,
    remove_user
)
from services.auth_service import login,logout
from ui.ui import (render_user_menu,
                   render_header,
                   render_main_menu,
                   get_current_user,
                   login_ui,
                   logout_ui,
                   register_user_ui,
                   list_users_ui,
                   unblock_user_ui,
                   remove_user_ui
                   )



def main():
    data=load_data()
    while True:
        current_user = get_current_user(data)
        render_header(data)

        if current_user:
            render_user_menu()
            option = input('Digite a opção desejada: ').strip()

            if option == '1':
                list_users_ui(data)
            elif option == '2':
                unblock_user_ui(data)
            elif option == '3':
                remove_user_ui(data)
            elif option == '4':
                logout_ui(data)
            elif option == '0':
                break
            else:
                print('Opção inválida.\n')

        else:
            render_main_menu()
            option = input('Digite a opção desejada: ').strip()
            if option == '1':
                register_user_ui(data)
            elif option == '2':
                login_ui(data)
            elif option == '0':
                break
            else:
                print('Opção inválida.\n')






if __name__ == "__main__":
    main()