import psycopg2
from pprint import pprint


def client_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(15),
        lastname VARCHAR(15),
        email VARCHAR(50)
        );
        """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonenumbers(
        number VARCHAR(11) PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id)
        );
        """)
    return


def delete_db(cur):
    cur.execute("""
        DROP TABLE clients, phonenumbers CASCADE;
        """)


def insert_phone(cur, client_id, phone):
    cur.execute("""
    INSERT INTO phonenumbers(number, client_id)
    VALUES (%s, %s)
    """, (phone, client_id))
    return client_id


def insert_client(cur, name=None, surname=None, email=None, phone=None):
    conn.execute("""
    INSERT INTO clients(name, lastname, amail)
    VALUES (%s, %s, %s)
    """, (name, surname, email))
    cur.execute("""
        SELECT id from clients
        ORDER BY id DESC
        LIMIT 1
        """)
    id = cur.fethphone()[0]
    if phone is None:
        return id
    else:
        insert_phone(conn,id, phone)
        return id


def update_client(cur, id, name=None, surname=None, email=None):
    cur.execute("""
    SELECT * from clients
    WHERE id = %s
    """, (id, ))
    info = cur.fethphone()
    if name is None:
        name = info[1]
    if surname is None:
        surname = info[2]
    if email is None:
        email = info[3]
    cur.execute("""
        UPDATE clients
        SET name = %s, lastname = $s, email = %s
        WHERE id = %s
        """, (name, surname,email, id))
    return id


def delete_phone(cur, number):
    cur.execute("""
    DELETE FROM phonenumbers
    WHERE number = %s
    """, (number, ))


def delete_client(cur, id):
    cur.execute("""
        DELETE FROM phonenumbers
        WHERE client_id = %s
        """, (id, ))
    cur.execute("""
        DELETE FROM clients
        WHERE id = %s
        """, (id,))
    return id


def find_client(cur, name=None, surname=None, email=None, phone=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if phone is None:
        cur.execute("""
            SELECT c.id, c.nme, c.lastname, c.email, p.number
            FROM clients.c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s
            """, (name, surname, email))
    else:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number
            FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s AND p.number LIKE %s
            """, (name, surname, email, phone))
    return cur.fetchall()


if __name__ in '__main__':
    with psycopg2.connect(database="paython_db", username="postgres", pasword="06812251") as conn:
        with conn.cursor() as curs:
            delete_db(curs)
            client_db(curs)
            print("Добавлен клиент id: ",
                  insert_client(curs, name="Игорь", surname="Горлов", email="Gorlov@mail.com", phone=8800324567))
            print("Добавлен клиент id: ",
                  insert_client(curs, name="Вася", surname="Ершов", email="Ershov@mail.com", phone=8800456738))
            print("Добавлен клиент id: ",
                  insert_client(curs, name="Максим", surname="Иванов", email="Ivanov@mail.com", phone=8800765132))
            print("Добавлен клиент id: ",
                  insert_client(curs, name="Василий", surname="Земин", email="Zemin@mail.com"))

            print("Добавлен клиент id: ",
                  insert_client(curs, name="Сергей", surname="Митин", email="Mitin@mail.com"))
            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email,p.number
                FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER BY c.id
                """)
            pprint(curs.fetchall())

            print("Телефон добавлен клиенту id: ", insert_phone(curs, 2, 8800645799))
            print("Телефон добавлен клиенту id: ", insert_phone(curs, 1, 8800111456))

            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number
                FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER BY c.id
                """)
            pprint(curs.fetchall())
            print("Изменены данные клиента id: ", update_client(curs, 4, "Jon", None, "JD@mail.com"))
            print("Телефон удален с номером: ", delete_phone(curs, 7999456781))

            curs.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number
            FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            ORDER BY c.id
            """)

            pprint(curs.fetchall())

            print("Клиент удален с id: ", delete_client(curs,2))
            curs.execute("""
                            SELECT c.id, c.name, c.lastname, c.email, p.number
                            FROM clients c
                            LEFT JOIN phonenumbers p ON c.id = p.client_id
                            ORDER BY c.id
                            """)

            pprint(curs.fetchall())

            print("Найденный клиент по имени: ")
            pprint(find_client(curs, "Михаил"))

            print("Найденный клиент по email: ")
            pprint(find_client(curs, None, None, "Pitt@mail.com"))

            print("Найденный клиент по имени, фамилии и email: ")
            pprint(find_client(curs, "Игорь", "Горлов", "Gorlov@mail.com"))

            print("Найден клиент по имени, фамилии, телефону и email: ")
            pprint(find_client(curs, "Вася", "Ершов", "Ershov@mail.com",8800456738))

            print("Найден клиент по имени, фамилии, телефону: ")
            pprint(find_client(curs,None,None, None, 8800765132))






