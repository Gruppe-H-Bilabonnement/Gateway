from flasgger import Swagger

def init_swagger(app, paths, tags):
    """Initialize Swagger with base configurations."""
    swagger_config = {
        "headers": [],
        "specs": [{"endpoint": "apispec", "route": "/apispec.json"}],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/v1/docs",  # URL where Swagger UI is hosted
    }
    template = {
        "swagger": "2.0",
        "info": {
            "title": "API Gateway",
            "description": "API Gateway for Bilabonnement.dk",
            "version": "1.0.0",
        },
        "paths": paths,
        "tags": tags,
    }
    return Swagger(app, config=swagger_config, template=template)

def update_swagger(swagger_instance, paths, tags):
    """Update existing Swagger instance with new paths and tags."""
    swagger_instance.template['paths'] = paths
    swagger_instance.template['tags'] = tags
    return swagger_instance