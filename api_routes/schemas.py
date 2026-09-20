"""Shared Pydantic schemas for ORBIT API v2 (optional modular routes)."""

from __future__ import annotations

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "orbit-toy"
    messages: List[ChatMessage]
    temperature: float = 0.8
    max_tokens: int = 128
    stream: bool = False
    top_p: float = 0.9
    stop: Optional[List[str]] = None


class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 64
    temperature: float = 0.8
    top_p: float = 0.9
    top_k: int = 0
    repetition_penalty: float = 1.1
    seed: Optional[int] = None


class EmbedRequest(BaseModel):
    input: str
    model: str = "orbit-hash"


class MemoryAddRequest(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None


class MemorySearchRequest(BaseModel):
    query: str
    top_k: int = 5


class RAGQueryRequest(BaseModel):
    question: str
    top_k: int = 5


class AgentRunRequest(BaseModel):
    message: str
    permission_level: str = "SAFE"
    max_iterations: int = 5
