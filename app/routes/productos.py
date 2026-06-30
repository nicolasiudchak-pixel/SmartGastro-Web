from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .. import db
from ..models import Producto

productos_bp = Blueprint("productos", __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@productos_bp.route("/")
@login_required
def index():
    productos = Producto.query.all()
    return render_template("productos/index.html", productos=productos)


@productos_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio = request.form.get("precio", 0)
        stock = request.form.get("stock", 0)
        categoria = request.form.get("categoria", "General").strip()

        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return render_template("productos/form.html", producto=None)

        producto = Producto(
            nombre=nombre,
            precio=float(precio),
            stock=int(stock),
            categoria=categoria,
        )
        try:
            db.session.add(producto)
            db.session.commit()
            flash(f"Producto '{nombre}' creado correctamente.", "success")
            return redirect(url_for("productos.index"))
        except Exception as e:
            db.session.rollback()
            flash("Error al guardar el producto.", "danger")

    return render_template("productos/form.html", producto=None)


@productos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    producto = Producto.query.get_or_404(id)

    if request.method == "POST":
        producto.nombre = request.form.get("nombre", "").strip()
        producto.precio = float(request.form.get("precio", 0))
        producto.stock = int(request.form.get("stock", 0))
        producto.categoria = request.form.get("categoria", "General").strip()

        try:
            db.session.commit()
            flash("Producto actualizado.", "success")
            return redirect(url_for("productos.index"))
        except Exception:
            db.session.rollback()
            flash("Error al actualizar el producto.", "danger")

    return render_template("productos/form.html", producto=producto)


@productos_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    try:
        db.session.delete(producto)
        db.session.commit()
        flash("Producto eliminado.", "success")
    except Exception:
        db.session.rollback()
        flash("No se pudo eliminar el producto (puede tener ventas asociadas).", "danger")
    return redirect(url_for("productos.index"))
