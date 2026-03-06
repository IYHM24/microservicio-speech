import json
from pathlib import Path


class Helpers:

    """ Obtener el Schema """
    @staticmethod
    def load_schema(schema_name: str) -> dict:
        base = Path(__file__).resolve().parent.parent  # points to src/
        schema_path = base / "contracts" / f"{schema_name}.schema.json"
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {schema_path}")
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    """ Cargar la prompt del sistema """
    @staticmethod
    def load_prompt(prompt_name: str) -> str:
        base = Path(__file__).resolve().parent.parent  # points to src/
        path = base / "prompts" / f"{prompt_name}.prompt.txt"
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")
        return path.read_text(encoding="utf-8")