from functions.get_files_info import get_files_info

def main():
    # Test cases
    print("Result for current directory:")
    print(get_files_info("calculator", "."))  # Expected: Directory contents for "."

    print("\nResult for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))  # Expected: Directory contents for "pkg"

    print("\nResult for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))  # Expected: Error (outside working directory)

    print("\nResult for '../' directory:")
    print(get_files_info("calculator", "../"))  # Expected: Error (outside working directory)

if __name__ == "__main__":
    main()