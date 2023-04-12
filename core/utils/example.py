def create_example_py_file():
    content = '''import sys

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
'''

    with open("example.py", "w", encoding="utf-8") as file:
        file.write(content)

if __name__ == "__main__":
    create_example_py_file()