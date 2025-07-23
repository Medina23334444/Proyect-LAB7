"""
app.py
-------------
Aplicación Flask mínima pero lista para producción/desarrollo.
Incluye:
  - Rutas / y /api/health
  - Manejo básico de errores (404 y 500)
  - Configuración basada en variables de entorno
"""
import os
import logging
from flask import Flask, jsonify, render_template, request


# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
class Config:
    """Configuración base (aplicable a todos los entornos)."""
    DEBUG = False
    TESTING = False
    APP_PORT = int(os.getenv("APP_PORT", 5000))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    # Podríamos agregar configuraciones extras específicas de producción
    pass


def create_app():
    """Factory pattern para crear la app con la configuración correcta."""
    env = os.getenv("FLASK_ENV", "development").lower()
    app = Flask(__name__)

    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        # Por defecto Development
        app.config.from_object(DevelopmentConfig)

    # Configurar logging simple
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

    # -------------------------------------------------------------------
    # Rutas
    # -------------------------------------------------------------------
    @app.route("/")
    def index():
        """Ruta principal que renderiza una página HTML."""
        return render_template("index.html", message="Bienvenido a mi-app-web 🚀")  # noqa: E501

    @app.route("/api/health")
    def health():
        """Ruta de salud que retorna JSON con el estado."""
        return jsonify({
            "status": "ok",
            "environment": os.getenv("FLASK_ENV", "development"),
            "time": os.getenv("TZ", "UTC")
        })

    # -------------------------------------------------------------------
    # Manejo básico de errores
    # -------------------------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({"error": "Recurso no encontrado", "code": 404}), 404
        return render_template("index.html", message="Página no encontrada (404)"), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception("Error interno del servidor: %s", error)
        if request.path.startswith('/api/'):
            return jsonify({"error": "Error interno", "code": 500}), 500
        return render_template("index.html", message="Error interno (500)"), 500

    return app


application = create_app()
if __name__ == "__main__":
    port = application.config.get("APP_PORT", 5000)
    application.run(host="0.0.0.0", port=port)
