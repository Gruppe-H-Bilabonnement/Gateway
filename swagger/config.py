from flasgger import Swagger
import requests

def fetch_and_merge_swagger_docs(microservices):
    merged_definitions = {
        "swagger": "2.0",
        "info": {
            "title": "Centralized API Gateway Documentation",
            "description": "Consolidated documentation of all microservices",
            "version": "1.0.0"
        },
        "paths": {},
        "definitions": {}
    }

    for service, url in microservices.items():
        try:
            response = requests.get(f"{url}/api/v1/docs", timeout=5)
            if response.status_code == 200:
                service_doc = response.json()
                # Merge paths
                for path, details in service_doc.get('paths', {}).items():
                    merged_definitions['paths'][f"/{service}{path}"] = details
                # Merge definitions
                for definition, details in service_doc.get('definitions', {}).items():
                    merged_definitions['definitions'][definition] = details
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch Swagger documentation from {service}: {e}")

    return merged_definitions

def init_swagger(app, microservices):
    merged_swagger = fetch_and_merge_swagger_docs(microservices)
    swagger_config = {
        "headers": [],
        "specs": [{
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/v1/docs"
    }
    return Swagger(app, config=swagger_config, template=merged_swagger)
