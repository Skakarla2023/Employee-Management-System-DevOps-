import os
from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
DATABASE = os.environ.get("DATABASE_PATH", os.path.join(app.root_path, "data", "employees.db"))

os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
init_db(DATABASE)

@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    db = get_db(DATABASE)
    if search:
        employees = db.execute(
            """SELECT * FROM employees
               WHERE name LIKE ? OR email LIKE ? OR department LIKE ?
               ORDER BY id DESC""",
            (f"%{search}%", f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
        employees = db.execute("SELECT * FROM employees ORDER BY id DESC").fetchall()
    db.close()
    return render_template("index.html", employees=employees, search=search)

@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        data = employee_form_data()
        if not data["name"] or not data["email"]:
            flash("Name and email are required.", "error")
            return render_template("add_employee.html", employee=data)
        db = get_db(DATABASE)
        db.execute(
            """INSERT INTO employees (name, email, department, designation, salary)
               VALUES (?, ?, ?, ?, ?)""",
            (data["name"], data["email"], data["department"],
             data["designation"], data["salary"])
        )
        db.commit()
        db.close()
        flash("Employee added successfully.", "success")
        return redirect(url_for("index"))
    return render_template("add_employee.html", employee={})

@app.route("/edit/<int:employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):
    db = get_db(DATABASE)
    employee = db.execute("SELECT * FROM employees WHERE id = ?", (employee_id,)).fetchone()
    if employee is None:
        db.close()
        flash("Employee not found.", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        data = employee_form_data()
        if not data["name"] or not data["email"]:
            flash("Name and email are required.", "error")
            db.close()
            return render_template("edit_employee.html", employee=data, employee_id=employee_id)
        db.execute(
            """UPDATE employees
               SET name=?, email=?, department=?, designation=?, salary=?
               WHERE id=?""",
            (data["name"], data["email"], data["department"],
             data["designation"], data["salary"], employee_id)
        )
        db.commit()
        db.close()
        flash("Employee updated successfully.", "success")
        return redirect(url_for("index"))
    db.close()
    return render_template("edit_employee.html", employee=employee, employee_id=employee_id)

@app.route("/delete/<int:employee_id>", methods=["POST"])
def delete_employee(employee_id):
    db = get_db(DATABASE)
    db.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    db.commit()
    db.close()
    flash("Employee deleted.", "success")
    return redirect(url_for("index"))

def employee_form_data():
    salary_text = request.form.get("salary", "0").strip()
    try:
        salary = max(float(salary_text or 0), 0)
    except ValueError:
        salary = 0
    return {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "department": request.form.get("department", "").strip(),
        "designation": request.form.get("designation", "").strip(),
        "salary": salary,
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
