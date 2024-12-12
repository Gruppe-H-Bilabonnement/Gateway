from flasgger import Swagger

def init_swagger(app):
    """Initialize Swagger with base configurations."""
    swagger_config = {
        "headers": [],
        "specs": [{"endpoint": "apispec", "route": "/apispec.json"}],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/v1/docs",
    }
    template = {
        "swagger": "2.0",
        "info": {
            "title": "API Gateway",
            "description": "API Gateway for Bilabonnement.dk",
            "version": "1.0.0",
        },
        "paths": {},
        "tags": [],
    }
    return Swagger(app, config=swagger_config, template=template)