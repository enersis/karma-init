from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Config:
    baseConfigPath: str
    outputConfigPath: str
    configMapSelector: dict = field(default_factory=dict)
    namespace: Optional[str] = None
