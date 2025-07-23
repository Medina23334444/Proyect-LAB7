# mi-app-web

Proyecto de ejemplo en **Python/Flask** empaquetado con **Docker** y **Docker Compose**.

## Estructura

```text
mi-app-web/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── templates/
│   └── index.html
└── README.md
```

## Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/) (si usas Docker Desktop ya viene incluido)

## Modo Desarrollo

1. Clona o descarga este repositorio (o extrae el ZIP).
2. Desde la carpeta del proyecto, ejecuta:

   ```bash
   docker compose up --build
   ```

3. Accede a la app en: **http://localhost:8080**

- En desarrollo se monta el directorio actual (`./`) como volumen (hot-reload con `flask run`).
- Variable `FLASK_ENV=development` por defecto.

## Modo Producción

Simplemente establece la variable `FLASK_ENV=production` para usar gunicorn (servidor WSGI):

```bash
FLASK_ENV=production docker compose up --build -d
```

- El contenedor expondrá el puerto interno 5000 y se mapeará al 8080 del host.
- Gunicorn arrancará con el número de workers definido en `WORKERS`.

## Variables de Entorno

| Variable   | Descripción                           | Valor por defecto |
|------------|---------------------------------------|-------------------|
| FLASK_ENV  | Entorno de ejecución (development/production) | development       |
| APP_PORT   | Puerto interno en el contenedor       | 5000              |
| WORKERS    | Workers de gunicorn (production)      | 2                 |

Puedes definirlas en un archivo `.env` o pasarlas inline:

```bash
FLASK_ENV=production WORKERS=4 docker compose up --build
```

## Endpoints

- `/` : Página HTML de bienvenida.
- `/api/health` : JSON con el estado de la aplicación.

## Tests rápidos

```bash
curl http://localhost:8080/api/health
```

Debe devolver algo como:

```json
{
  "status": "ok",
  "environment": "development",
  "time": "UTC"
}
```

---

© 2025 mi-app-web
