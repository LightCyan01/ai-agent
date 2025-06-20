from functions.get_files_info import get_files_info, get_file_content, write_file

print("result for lorem.txt")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

print("result for morelorem.txt")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print("results for tmp/temp.txt")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))