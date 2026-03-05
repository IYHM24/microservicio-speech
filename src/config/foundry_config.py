import os
from typing import Optional

import httpx

try:
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.projects import ProjectsClient
    _AZURE_SDK_AVAILABLE = True
except Exception:
    AzureKeyCredential = None  # type: ignore
    ProjectsClient = None  # type: ignore
    _AZURE_SDK_AVAILABLE = False


class FoundryConfig:
    """Configuración para Foundry usando el SDK de Azure (si está instalado).

    - Si `azure-ai-projects` está disponible, crea `self.sdk_client` como
      `ProjectsClient(endpoint, AzureKeyCredential(key))`.
    - Siempre crea `self.client` como `httpx.AsyncClient` para fallback.
    """

    def __init__(self):
        self.api_key: str = os.getenv("FOUNDRY_API_KEY", "")
        self.base_url: str = os.getenv("FOUNDRY_BASE_URL", "https://api.foundry.example")
        self.model: str = os.getenv("FOUNDRY_MODEL", "kimi-k2")
        self.timeout: int = int(os.getenv("FOUNDRY_TIMEOUT", "60"))
        self.max_retries: int = int(os.getenv("FOUNDRY_MAX_RETRIES", "3"))

        if not self.api_key:
            raise RuntimeError("FOUNDRY_API_KEY is not set")

        # SDK client (azure-ai-projects) if available
        self.sdk_client = None
        if _AZURE_SDK_AVAILABLE and AzureKeyCredential and ProjectsClient:
            try:
                self.sdk_client = ProjectsClient(self.base_url, AzureKeyCredential(self.api_key))
            except Exception:
                self.sdk_client = None

        # httpx client as fallback for raw REST requests
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)

        self.client: httpx.AsyncClient = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=httpx.Timeout(self.timeout),
            limits=limits,
        )

    async def aclose(self) -> None:
        if self.sdk_client:
            # SDK clients usually don't need explicit close; ignore if not implemented
            close = getattr(self.sdk_client, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass
        await self.client.aclose()
