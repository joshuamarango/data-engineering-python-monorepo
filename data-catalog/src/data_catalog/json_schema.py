from pydantic.json_schema import GenerateJsonSchema


class GlueSchemaGenerator(GenerateJsonSchema):
    def generate(self, schema, description: str, mode='validation'):
        json_schema = super().generate(schema, mode=mode)
        json_schema['$schema'] = "https://json-schema.org/draft-07/schema",
        json_schema["$id"] = f"https://schema.data-catalog.acme.com/{json_schema['title']}.schema.json"
        json_schema["description"] = description
        return json_schema