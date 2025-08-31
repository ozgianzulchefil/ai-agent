# python
import os, sys
# print("CWD:", os.getcwd())
# print("ROOT CONTENTS:", os.listdir("."))
# print("FUNCTIONS CONTENTS:", os.listdir("functions") if os.path.isdir("functions") else "functions dir not found")
# sys.path.insert(0, os.path.abspath("."))

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

if __name__ == "__main__":
    # below are tests for get_file_content
    # print("Result for current directory:")
    # print(get_files_info("calculator", "."))
    # print("\nResult for 'pkg' directory:")
    # print(get_files_info("calculator", "pkg"))
    # print("\nResult for 'bin' directory:")
    # print(get_files_info("calculator", "/bin"))
    # print("\nResult for '../' directory:")
    # print(get_files_info("calculator", "../"))

    # below are tests for get_file_content
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))