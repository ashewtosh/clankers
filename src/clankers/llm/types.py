from dataclasses import dataclass, field
from typing import Any
from clankers.core.types import Message

@dataclass(frozen=True, slots=True)
class LLMRequest:
    messages: tuple[Message, ...]
    model: str
    temperature: float = 0.0
    max_tokens: int | None = None

@dataclass(frozen=True, slots=True)
class LLMResponse:
    content: str
    model: str
    raw: dict[str, Any] = field(default_factory=dict)