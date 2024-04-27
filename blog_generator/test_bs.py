# import re

# error_message = "[WinError 183] Cannot create a file when that file already exists: 'E:\\Code\\backend_freecode\\ai-blog-article-generator\\media\\SOLID Principles Do You Really Understand Them.mp4' -> 'E:\\Code\\backend_freecode\\ai-blog-article-generator\\media\\SOLID Principles Do You Really Understand Them.mp3'"
# pattern = r"(\S+)\\S+"
# match = re.search(pattern, error_message)

# if match:
#     print(match.group(1))


import re


error_message = "[WinError 183] Cannot create a file when that file already exists: 'E:\\Code\\backend_freecode\\ai-blog-article-generator\\media\\SOLID Principles Do You Really Understand Them.mp4' -> 'E:\\Code\\backend_freecode\\ai-blog-article-generator\\media\\SOLID Principles Do You Really Understand Them.mp3'"

match = re.search(r"-> '.+\.mp3)'", error_message)
if match:
    print(match.group(0))
    extracted_path = match.group(1)
    print(extracted_path)
