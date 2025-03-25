import sys
from flask import Flask, render_template, abort
from faker import Faker


app = Flask(__name__)
fake = Faker("ru_RU")

def create_files() -> None:  # zapolnenie failov
    with open("./files/humans.txt", 'w', encoding="utf-8") as humans_f:
        for _ in range(10):
            print(*fake.name().split(), sep=',', file=humans_f)

    with open("./files/names.txt", 'w', encoding="utf-8") as names_f:
        for _ in range(10):
            print(fake.first_name(), sep=',', file=names_f)

    with open("./files/users.txt", 'w', encoding="utf-8") as users_f:
        for _ in range(10):
            print(*fake.simple_profile().values(), sep=';', file=users_f)

def load_users():
    users = []
    with open("./files/users.txt", encoding="utf-8") as f:
        for line in f:
            login, full_name, gender, address, email, birth_date = line.strip().split(';')
            users.append({
                'login': login,
                'full_name': full_name,
                'gender': gender,
                'address': address,
                'email': email,
                'birth_date': birth_date
            })
    return users

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/names")
def get_names():
    names = list()
    with open("./files/names.txt", encoding="utf-8") as f:
        for raw_line in f:
            names.append(raw_line.strip())
        
    return render_template("names.html", people_names=names, check=555)

@app.route("/table")
def table():
    
    users = load_users()
    entities = []
    
    with open("./files/humans.txt", encoding="utf-8") as f:
        for i, raw_line in enumerate(f):
            data = raw_line.strip().split(',')
            
            if len(data) == 3:
                
                login = users[i]['login'] if i < len(users) else f"{data[1].lower()}_{data[0].lower()}"
                
                entities.append({
                    'login': login,
                    'last_name': data[0],
                    'name': data[1],
                    'surname': data[2],
                    'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
                    'phone': fake.phone_number()
                })
    
    return render_template("table.html", entities=entities, check=555)

@app.route("/users")
def users_list():
    entities = []
    with open("./files/users.txt", encoding="utf-8") as f:
        for raw_line in f:
            data = raw_line.strip().split(';')
            
            
            if len(data) >= 6:
                entities.append({
                    'login': data[0],
                    'name': data[1],
                    'gender': data[2],
                    'address': data[3],
                    'email': data[4],
                    'birth_date': data[5]
                })
    
    return render_template("users_list.html", users=entities, check=555)

@app.route("/users/<login>")
def user_profile(login):
    users = load_users()
    user = next((user for user in users if user['login'] == login), None)
    if user:
        return render_template("user_item.html", user=user)
    return "Пользователь не найден", 404

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--files":
        create_files()
    app.run(debug=True)