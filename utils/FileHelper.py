import re
from typing import List, Optional

def find_file_path(pathList: List[str], fileNameRegExp: str) -> Optional[str] :
    # All file paths that match the given file name regular expression    
    fileMatches: List[str] = [path for path in pathList if re.search(fileNameRegExp, path, re.IGNORECASE)]
    
    # If file is not present in tar, None will be returned
    if len(fileMatches) == 0:
        return None
    else:
        # Assuming log file names that we search for are unique per tar, so return first match
        return fileMatches[0]


def write_to_json_file(json_string: str, file_name: str): 
    with open(file_name, 'w') as json_file:
        json_file.write(json_string)
        json_file.close()