# python
import os, sys
# print("CWD:", os.getcwd())
# print("ROOT CONTENTS:", os.listdir("."))
# print("FUNCTIONS CONTENTS:", os.listdir("functions") if os.path.isdir("functions") else "functions dir not found")
# sys.path.insert(0, os.path.abspath("."))

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

if __name__ == "__main__":
    # below are tests for get_file_content - uncomment if you want to verify 
    # print("Result for current directory:")
    # print(get_files_info("calculator", "."))
    # print("\nResult for 'pkg' directory:")
    # print(get_files_info("calculator", "pkg"))
    # print("\nResult for 'bin' directory:")
    # print(get_files_info("calculator", "/bin"))
    # print("\nResult for '../' directory:")
    # print(get_files_info("calculator", "../"))

    # below are tests for get_file_content - uncomment if you want to verify 
    # print(get_file_content("calculator", "main.py"))
    # print(get_file_content("calculator", "pkg/calculator.py"))
    # print(get_file_content("calculator", "/bin/cat"))
    # print(get_file_content("calculator", "pkg/does_not_exist.py"))

    # below are tests for write_file_content
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))