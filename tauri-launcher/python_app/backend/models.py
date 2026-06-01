from pydantic import BaseModel, Field


class ExegesisRequest(BaseModel):
    reference: str = Field(..., description="Ex: Joao 3:16")
    text: str = Field(..., description="Texto biblico base")
    model: str | None = Field(default=None, description="Modelo Ollama ou provider externo")
    language: str = Field(default="pt", description="Idioma de resposta")
    provider: str = Field(default="ollama", description="Provedor: ollama, chatgpt, deepseek, grok, openrouter, target_ai, nvidia, gemini")


class ExegesisResponse(BaseModel):
    model: str
    reference: str
    response: str


class GenerationRequest(BaseModel):
    kind: str = Field(..., description="Tipo de geracao: sermon, devotional, chat, questions, study")
    reference: str = Field(default="", description="Referencia biblica ou escopo")
    context: str = Field(..., description="Texto base para a geracao")
    request: str = Field(..., description="Instrucoes para o modelo")
    model: str | None = Field(default=None, description="Modelo Ollama ou provider externo")
    language: str = Field(default="pt", description="Idioma de resposta")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1800, ge=1, le=12000)
    timeout_sec: int = Field(default=180, ge=1, le=1200)
    provider: str = Field(default="ollama", description="Provedor: ollama, chatgpt, deepseek, grok, openrouter, target_ai, nvidia, gemini")


class GenerationResponse(BaseModel):
    kind: str
    model: str
    reference: str
    response: str


class ExportPdfRequest(BaseModel):
    title: str = Field(..., min_length=1)
    subtitle: str | None = None
    sections: list[dict[str, str]] = Field(default_factory=list)
    footer: str | None = None
