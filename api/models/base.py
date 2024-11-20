class BaseModel:
    schema = {}

    @classmethod
    def validate(cls, data):
        """Valida que los datos cumplan con el esquema del modelo."""
        if not data or not isinstance(data, dict):
            return False
        for key, value_type in cls.schema.items():
            if key not in data or not isinstance(data[key], value_type):
                return False
        return True

    def to_json(self):
        """Convierte un objeto de modelo a formato JSON."""
        return {key: getattr(self, f"_{key}") for key in self.schema}