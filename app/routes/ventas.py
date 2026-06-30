from flask import Blueprint, render_template, session, redirect, url_for
from ..models import Venta, Cliente, Producto

ventas_bp = Blueprint("ventas", __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


@ventas_bp.route("/")
@login_required
def index():
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template("ventas/index.html", ventas=ventas)


@ventas_bp.route("/nueva")
@login_required
def nueva():
    clientes = Cliente.query.all()
    productos = Producto.query.filter(Producto.stock > 0).all()
    return render_template("ventas/nueva.html", clientes=clientes, productos=productos)
