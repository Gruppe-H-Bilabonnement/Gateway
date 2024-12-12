from flasgger import Swagger

def init_swagger(app):
    swagger_config = {
        "headers": [],
        "specs": [{
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # Include all routes
            "model_filter": lambda tag: True,  # Include all tags
        }],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/v1/docs"
    }

    template = {
        "swagger": "2.0",
        "info": {
            "title": "API Gateway",
            "description": "API Gateway for managing rental cars",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "JWT": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        }
    }

    return Swagger(app, config=swagger_config, template=template)