from flask import Blueprint, request, jsonify, session
from .. import db
from ..models import Venta, DetalleVenta, Producto, Cliente

api_bp = Blueprint("api", __name__)


def login_required_api(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "No autorizado"}), 401
        return f(*args, **kwargs)
    return decorated


@api_bp.route("/ventas", methods=["POST"])
@login_required_api
def crear_venta():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    cliente_id = data.get("cliente_id")
    items = data.get("items", [])

    if not cliente_id or not items:
        return jsonify({"error": "Faltan datos: cliente_id e items son requeridos"}), 400

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    total = 0.0
    detalles = []

    for item in items:
        producto = Producto.query.get(item.get("producto_id"))
        cantidad = int(item.get("cantidad", 0))

        if not producto:
            return jsonify({"error": f"Producto {item.get('producto_id')} no encontrado"}), 404
        if cantidad <= 0:
            return jsonify({"error": "La cantidad debe ser mayor a 0"}), 400
        if producto.stock < cantidad:
            return jsonify({"error": f"Stock insuficiente para '{producto.nombre}' (disponible: {producto.stock})"}), 400

        subtotal = producto.precio * cantidad
        total += subtotal
        detalles.append(DetalleVenta(
            producto_id=producto.id,
            cantidad=cantidad,
            precio_unitario=producto.precio,
        ))
        producto.stock -= cantidad

    venta = Venta(
        cliente_id=cliente_id,
        usuario_id=session["user_id"],
        total=round(total, 2),
    )

    try:
        db.session.add(venta)
        db.session.flush()
        for d in detalles:
            d.venta_id = venta.id
            db.session.add(d)
        db.session.commit()
        return jsonify({
            "ok": True,
            "venta_id": venta.id,
            "total": venta.total,
            "mensaje": f"Venta #{venta.id} registrada por ${venta.total:.2f}",
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno al registrar la venta"}), 500


@api_bp.route("/productos", methods=["GET"])
@login_required_api
def listar_productos():
    productos = Producto.query.filter(Producto.stock > 0).all()
    return jsonify([
        {"id": p.id, "nombre": p.nombre, "precio": p.precio, "stock": p.stock}
        for p in productos
    ])
