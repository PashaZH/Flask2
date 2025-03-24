import sys
from flask import Flask, render_template
from faker import Faker


app = Flask(__name__)
fake = Faker("ru_RU")

def create_files() -> None:  # zapolnenie files
    with open("./files/humans.txt", 'w', encoding="utf-8") as humans_f:
        for _ in range(10):
            print(*fake.name().split(), sep=',', file=humans_f)

    with open("./files/names.txt", 'w', encoding="utf-8") as names_f:
        for _ in range(10):
            print(fake.first_name(), sep=',', file=names_f)

    with open("./files/users.txt", 'w', encoding="utf-8") as users_f:
        for _ in range(10):
            print(*fake.simple_profile().values(), sep=';', file=users_f)


@app.route("/")

def hello():
    return render_template("index.html")

@app.route("/names")
def get_names():
    names = list()
    with open("./files/names.txt", encoding="utf-8") as f:
        for raw_line in f:
            names.append(raw_line.strip())
        return "<br>".join(names)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--files":
        create_files()
    app.run(debug=True)


