import json
import os

DB_FILE = 'database.json'

class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class UserManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self._ensure_db()

    def _ensure_db(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def _load_data(self):
        with open(self.db_file, 'r') as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=4)

    def create_user(self, user):
        data = self._load_data()
        if any(u['id'] == user.id for u in data):
            print(f" Ya existe un usuario con ID {user.id}")
            return
        data.append(user.to_dict())
        self._save_data(data)
        print(f" Usuario '{user.name}' creado.")

    def read_users(self):
        data = self._load_data()
        if not data:
            print(" No hay usuarios.")
            return
        for u in data:
            print(f" {u['id']} |  {u['name']} |  {u['email']}")

    def update_user(self, user_id, new_name=None, new_email=None):
        data = self._load_data()
        for u in data:
            if u['id'] == user_id:
                if new_name:
                    u['name'] = new_name
                if new_email:
                    u['email'] = new_email
                self._save_data(data)
                print(f" Usuario {user_id} actualizado.")
                return
        print(f" Usuario con ID {user_id} no encontrado.")

    def delete_user(self, user_id):
        data = self._load_data()
        new_data = [u for u in data if u['id'] != user_id]
        if len(new_data) == len(data):
            print(f" Usuario con ID {user_id} no encontrado.")
        else:
            self._save_data(new_data)
            print(f"🗑️ Usuario {user_id} eliminado.")


def menu():
    manager = UserManager(DB_FILE)
    while True:
        print("\n--- MENÚ CRUD ---")
        print("1. Crear usuario")
        print("2. Ver usuarios")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. Salir")

        choice = input("Elige una opción: ")

        if choice == '1':
            try:
                user_id = int(input("ID: "))
                name = input("Nombre: ")
                email = input("Email: ")
                user = User(user_id, name, email)
                manager.create_user(user)
            except ValueError:
                print(" ID debe ser numérico.")
        elif choice == '2':
            manager.read_users()
        elif choice == '3':
            try:
                user_id = int(input("ID del usuario a actualizar: "))
                name = input("Nuevo nombre (Enter para omitir): ")
                email = input("Nuevo email (Enter para omitir): ")
                manager.update_user(user_id, name or None, email or None)
            except ValueError:
                print(" ID inválido.")
        elif choice == '4':
            try:
                user_id = int(input("ID del usuario a eliminar: "))
                manager.delete_user(user_id)
            except ValueError:
                print(" ID inválido.")
        elif choice == '5':
            print(" Saliendo del programa.")
            break
        else:
            print(" Opción no válida.")

if __name__ == "__main__":
    menu()