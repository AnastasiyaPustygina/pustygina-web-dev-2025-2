from flask import Flask, request, render_template, redirect, make_response, jsonify
import re

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask-приложение работает!"

@app.route("/url_params")
def url_params():
    return render_template("params.html", params=request.args)

@app.route("/headers")
def headers():
    return render_template("headers.html", headers=request.headers)

@app.route("/cookies")
def cookies():
    cookie_name = "my_cookie"
    cookie_value = request.cookies.get(cookie_name)

    if cookie_value:
        response = make_response(render_template("cookies.html", cookie_value=cookie_value))
        response.delete_cookie(cookie_name)
    else:
        response = make_response(render_template("cookies.html", cookie_value=None))
        response.set_cookie(cookie_name, "test_value", max_age=60)

    return response

@app.route("/form_params", methods=["POST", "GET"])
def form_params():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        if not name or not email:
            return "Bad Request", 400
        return "Form submitted successfully", 200
    return render_template("form.html")


def validate_phone_number(phone):
    if not re.match(r"^[\d\s().\-+]+$", phone):
        return "Недопустимый ввод. В номере телефона встречаются недопустимые символы.", False

    digits = re.sub(r"\D", "", phone)

    if len(digits) not in [10, 11]:
        return "Недопустимый ввод. Неверное количество цифр.", False

    if len(digits) == 11 and not (digits.startswith("8") or digits.startswith("7")):
        return "Недопустимый ввод. Неверное количество цифр.", False

    formatted = f"8-{digits[-10:-7]}-{digits[-7:-4]}-{digits[-4:-2]}-{digits[-2:]}"
    return formatted, True

@app.route("/validate_phone", methods=["POST"])
def phone_validation():
    error = None
    formatted_number = None

    if request.method == "POST":
        phone = request.form.get("phone", "")
        formatted_number, is_valid = validate_phone_number(phone)
        if not is_valid:
            error = formatted_number
            return error, 400
    return render_template("phone_validation.html", error=error, formatted_number=formatted_number)

@app.route("/redirect_example")
def redirect_example():
    return redirect("/")

@app.route("/api/data")
def api_data():
    return jsonify({"key": "value"})

@app.route("/set_cookie")
def set_cookie():
    resp = make_response("Cookie Set")
    resp.set_cookie("my_cookie", "cookie_value")
    return resp

@app.route("/delete_cookie")
def delete_cookie():
    resp = make_response("Cookie Deleted")
    resp.delete_cookie("my_cookie")
    return resp

@app.route("/json_post", methods=["POST"])
def json_post():
    data = request.get_json()
    return jsonify(data)
@app.errorhandler(405)
def method_not_allowed(error):
    return "Method Not Allowed", 405
if __name__ == "__main__":
    app.run(debug=True)
