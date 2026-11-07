from drf_spectacular.extensions import OpenApiAuthenticationExtension



class APIKeyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "api.authentication.APIKeyAuthentication"
    name = "APIKeyAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: Api-Key <your_api_key>",
        }