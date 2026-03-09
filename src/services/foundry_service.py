from typing import Any, Dict, Optional
from src.config.foundry_config import FoundryConfig


class FoundryService(FoundryConfig):
    
    """Servicio para interactuar con Foundry.

    Hereda `FoundryConfig` para reutilizar `self.sdk_client` o `self.client`.
    """

    """ Constructor de la clase """
    def __init__(self):
        super().__init__()

    """ Función genérica para llamar al modelo `kimi-k2` usando SDK o REST según disponibilidad. """
    async def call_model(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Llama al modelo `kimi-k2` usando el SDK si está disponible, si no usa REST.

        El payload y la ruta deben ajustarse según la API real de Foundry/Azure Foundry.
        """
        options = options or {}

        # Primer intento: usar el SDK client si existe
        if getattr(self, "sdk_client", None):
            sdk = self.sdk_client
            # probar nombres de método comunes en SDKs para invocar modelos
            for method_name in ("invoke", "invoke_model", "begin_invoke", "invoke_model_async"):
                method = getattr(sdk, method_name, None)
                if callable(method):
                    try:
                        result = method(model=self.model, input=prompt, **options)
                        # si devuelve un poller
                        if hasattr(result, "result"):
                            result = result.result()
                        return result
                    except TypeError:
                        # mismatched signature; intentar con otro esquema
                        try:
                            result = method(prompt, **options)
                            if hasattr(result, "result"):
                                result = result.result()
                            return result
                        except Exception:
                            continue
                    except Exception:
                        # fall back al REST below
                        break

        # Fallback: usar REST vía httpx
        payload = {"model": self.model, "input": prompt, **options}
        url = f"/v1/models/{self.model}/invoke"
        resp = await self.client.post(url, json=payload)
        resp.raise_for_status()
        try:
            return resp.json()
        except Exception:
            return {"status": resp.status_code, "text": resp.text}

    """ Función para transcribir audio usando el modelo `kimi-k2` vía SDK o REST. """
    async def transcribe(self, audio_bytes: bytes, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Transcribe audio usando REST o SDK si lo soporta.

        Ajustar según la API real de Foundry.
        """
        options = options or {}
        # Intentar SDK primero
        if getattr(self, "sdk_client", None):
            sdk = self.sdk_client
            method = getattr(sdk, "transcribe", None) or getattr(sdk, "transcriptions", None)
            if callable(method):
                try:
                    result = method(audio_bytes, model=self.model, **options)
                    if hasattr(result, "result"):
                        result = result.result()
                    return result
                except Exception:
                    pass

        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"model": self.model, **options}
        url = "/v1/audio/transcriptions"
        resp = await self.client.post(url, data=data, files=files)
        resp.raise_for_status()
        try:
            return resp.json()
        except Exception:
            return {"status": resp.status_code, "text": resp.text}

    """ Función de health check que intenta usar SDK si disponible, sino REST """
    async def health_check(self) -> bool:
        # Preferir SDK health method si disponible
        if getattr(self, "sdk_client", None):
            method = getattr(self.sdk_client, "health_check", None) or getattr(self.sdk_client, "get_health", None)
            if callable(method):
                try:
                    res = method()
                    if hasattr(res, "result"):
                        res = res.result()
                    return getattr(res, "status", 200) == 200
                except Exception:
                    pass
        try:
            resp = await self.client.get("/v1/health")
            return resp.status_code == 200
        except Exception:
            return False

