from pydantic import BaseModel


class TranslatedBaseModel(BaseModel):
    def model_dump(self, language: str | None = None, *args, **kwargs):
        dump = super().model_dump(*args, **kwargs)
        result = {}
        return self.extract_translation(dump, language, result)

    def extract_translation(
        self,
        obj: dict | list,
        language: str | None,
        result: dict = {},
    ) -> dict:
        for field_name, value in obj.items():
            if field_name == "translations":
                # Handle translations
                translations = obj.get(field_name, [])
                translation = next(
                    (t for t in translations if t["language_code"] == language),
                    None,
                )
                if translation:
                    # Update result with translation fields
                    for translation_field, translation_value in translation.items():
                        result[translation_field] = translation_value
            elif isinstance(value, dict):
                # Recursive call for nested dictionaries
                result[field_name] = self.extract_translation(value, language, {})
            elif isinstance(value, list):
                # Recursive call for nested lists
                result[field_name] = [
                    self.extract_translation(obj, language, {}) for obj in value
                ]
            else:
                result[field_name] = value
        return result
