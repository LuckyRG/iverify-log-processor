from dataclasses import dataclass
from typing import Optional

@dataclass
class DBLogEvent:
    ID: int
    timestamp: Optional[float]
    BundleID: Optional[str]
    CoalitionID: Optional[int]
    PID: Optional[int]
    ProcessName: Optional[str]