# SmartGastro Web

Sistema de gestión para foodtrucks — Segunda Entrega  
Materia: Análisis y Metodología de Sistemas · Da Vinci  
Integrantes: Nicolas Iudchak

---

## Descripción

SmartGastro es una aplicación web que permite a los dueños de foodtrucks gestionar su inventario, clientes y ventas, con alerta climática en tiempo real para evitar pérdidas de mercadería por lluvia.

## Tecnologías

- Python 3 + Flask
- SQLAlchemy (SQLite)
- Flask-Bcrypt (hashing de contraseñas)
- Sesiones Flask (autenticación)
- OpenWeatherMap API (clima)
- Jinja2 + CSS (frontend)
- fetch() async para registro de ventas

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPO>
cd SmartGastro-Web
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiar el archivo de ejemplo y completar los valores:

```bash
cp .env.example .env
```

Editar `.env`:

```
SECRET_KEY=una-clave-secreta-larga-y-aleatoria
DATABASE_URL=sqlite:///smartgastro.db
WEATHER_API_KEY=tu_api_key_de_openweathermap
WEATHER_CITY=Buenos Aires
```

> La API key de clima es gratuita en [openweathermap.org](https://openweathermap.org/api)

### 4. Ejecutar la aplicación

```bash
python run.py
```

Abrir en el navegador: `http://127.0.0.1:5000`

---

## Credenciales de prueba

| Campo | Valor |
|-------|-------|
| Email | admin@smartgastro.com |
| Contraseña | admin123 |

El usuario admin se crea automáticamente al iniciar la aplicación por primera vez.

---

## Funcionalidades

- Login/Logout con sesión protegida
- Dashboard con alerta de lluvia en tiempo real
- CRUD completo de Productos (inventario)
- CRUD completo de Clientes
- Registro de Ventas asíncrono (fetch + API REST interna)
- Historial de ventas con detalle por producto
