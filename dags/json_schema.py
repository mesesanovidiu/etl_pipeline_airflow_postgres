json_std_schema = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "object",
                        "properties": {
                            "first": {"type": "string"},
                            "last": {"type": "string"}
                        },
                        "required": ["first", "last"]
                    },
                    "location": {
                        "type": "object",
                        "properties": {
                            "country": {"type": "string"}
                        },
                        "required": ["country"]
                    },
                    "login": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "password": {"type": "string"}
                        },
                        "required": ["username", "password"]
                    },
                    "email": {"type": "string"}
                },
                "required": ["name", "location", "login", "email"]
            }
        }
    },
    "required": ["results"]
}
