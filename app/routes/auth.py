from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .. import db, bcrypt
from ..models import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and bcrypt.check_password_hash(usuario.password_hash, password):
            session["user_id"] = usuario.id
            session["user_nombre"] = usuario.nombre
            session["user_rol"] = usuario.rol
            return redirect(url_for("dashboard.index"))

        flash("Email o contraseña incorrectos.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
