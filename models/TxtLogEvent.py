from dataclasses import dataclass
from typing import Optional

@dataclass
class TxtLogEvent:
    USER: str             
    UID: int
    PRSNA: str
    PID: int
    PPID: int        
    F: Optional[str]   
    CPU: Optional[float]   
    MEM: Optional[float]   
    PRI: Optional[int]   
    NI: Optional[int]      
    VSZ: Optional[int]     
    RSS: Optional[int]   
    WCHAN: Optional[str]     
    TT: Optional[str]    
    STAT: Optional[str]   
    STARTED: Optional[str]       
    TIME: Optional[str]   
    COMMAND: Optional[str]