from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="Kiss and Tell API",
        version="1.0.0",
        description="API for anonymous confession app",
        routes=app.routes,
    )
    schema["components"] = schema.get("components", {})
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in schema.get("paths", {}).values():
        for op in path.values():
            if "security" not in op:
                op["security"] = []
    app.openapi_schema = schema
    return app.openapi_schema
