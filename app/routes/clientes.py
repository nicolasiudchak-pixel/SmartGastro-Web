from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .. import db
from ..models import Cliente

clientes_bp = Blueprint("clientes", __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@clientes_bp.route("/")
@login_required
def index():
    clientes = Cliente.query.all()
    return render_template("clientes/index.html", clientes=clientes)


@clientes_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        email = request.form.get("email", "").strip()

        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return render_template("clientes/form.html", cliente=None)

        cliente = Cliente(nombre=nombre, telefono=telefono, email=email)
        try:
            db.session.add(cliente)
            db.session.commit()
            flash(f"Cliente '{nombre}' registrado.", "success")
            return redirect(url_for("clientes.index"))
        except Exception:
            db.session.rollback()
            flash("Error al guardar el cliente.", "danger")

    return render_template("clientes/form.html", cliente=None)


@clientes_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == "POST":
        cliente.nombre = request.form.get("nombre", "").strip()
        cliente.telefono = request.form.get("telefono", "").strip()
        cliente.email = request.form.get("email", "").strip()

        try:
            db.session.commit()
            flash("Cliente actualizado.", "success")
            return redirect(url_for("clientes.index"))
        except Exception:
            db.session.rollback()
            flash("Error al actualizar el cliente.", "danger")

    return render_template("clientes/form.html", cliente=cliente)


@clientes_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash("Cliente eliminado.", "success")
    except Exception:
        db.session.rollback()
        flash("No se pudo eliminar el cliente (puede tener ventas asociadas).", "danger")
    return redirect(url_for("clientes.index"))
