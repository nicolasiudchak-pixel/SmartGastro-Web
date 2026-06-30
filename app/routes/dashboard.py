from flask import Blueprint, render_template, session, redirect, url_for, current_app
import requests
from ..models import Producto, Venta, Cliente

dashboard_bp = Blueprint("dashboard", __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def obtener_clima():
    api_key = current_app.config.get("WEATHER_API_KEY", "")
    city = current_app.config.get("WEATHER_CITY", "Buenos Aires")
    if not api_key:
        return None

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            "ciudad": data["name"],
            "descripcion": data["weather"][0]["description"].capitalize(),
            "temperatura": round(data["main"]["temp"], 1),
            "lluvia": any(
                w["main"].lower() in ("rain", "drizzle", "thunderstorm")
                for w in data["weather"]
            ),
            "icono": data["weather"][0]["icon"],
        }
    except Exception:
        return None


@dashboard_bp.route("/")
@login_required
def index():
    clima = obtener_clima()
    total_productos = Producto.query.count()
    productos_bajo_stock = Producto.query.filter(Producto.stock < 5).count()
    total_clientes = Cliente.query.count()
    total_ventas = Venta.query.count()
    ventas_recientes = Venta.query.order_by(Venta.fecha.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        clima=clima,
        total_productos=total_productos,
        productos_bajo_stock=productos_bajo_stock,
        total_clientes=total_clientes,
        total_ventas=total_ventas,
        ventas_recientes=ventas_recientes,
    )
