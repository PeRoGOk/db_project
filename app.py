from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Функція підключення до бази
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# --------- Головна сторінка з таблицею ----------
@app.route("/")
def index():
    conn = get_db()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("index.html", products=rows)


# --------- Додавання ----------
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]

    conn = get_db()
    conn.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
                 (name, price, description))
    conn.commit()
    conn.close()
    return redirect("/")


# --------- Видалення ----------
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


# ---------- Сторінка редагування ----------
@app.route("/edit/<int:id>")
def edit(id):
    conn = get_db()
    row = conn.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", p=row)


# ---------- Оновлення ----------
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]

    conn = get_db()
    conn.execute("""
        UPDATE products 
        SET name=?, price=?, description=? 
        WHERE id=?
    """, (name, price, description, id))
    conn.commit()
    conn.close()
    return redirect("/")


# ---------- Створення таблиці при запуску ----------
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# ---------- Обробка 500 ----------
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
