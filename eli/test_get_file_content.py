from functions.get_file_content import get_file_content

def main():
    # Test case: Large file (lorem.txt)
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")

    # Test case: Small file (main.py)
    print("\nResult for main.py:")
    result = get_file_content("calculator", "main.py")
    print(result)

    # Test case: File in subdirectory (pkg/calculator.py)
    print("\nResult for pkg/calculator.py:")
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)

    # Test case: File outside working directory (/bin/cat)
    print("\nResult for /bin/cat:")
    result = get_file_content("calculator", "/bin/cat")
    print(result)

    # Test case: Non-existent file (pkg/does_not_exist.py)
    print("\nResult for pkg/does_not_exist.py:")
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)

if __name__ == "__main__":
    main()