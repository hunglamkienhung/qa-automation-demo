from datetime import datetime
from API.Common.Open_File import *

def write_file_txt(filepath: str, message: str,file_extension: str ):
    with open_file_txt(filepath + datetime.now().strftime("%Y-%m-%d") + '.' + file_extension) as file:
        file.write(f"\n🔄 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}] {message}\n")

