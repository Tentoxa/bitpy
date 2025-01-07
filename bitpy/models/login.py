from dataclasses import dataclass
from typing import Optional

@dataclass
class BitgetCredentials:
    api_key: Optional[str] = None
    secret_key: Optional[str] = None
    api_passphrase: Optional[str] = None