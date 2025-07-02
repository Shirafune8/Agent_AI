import os
import unittest
from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file

# class Test_get_files_info(unittest.TestCase):
#     # Test 1: Run get_files_info("calculator", ".")
#     def test_calculator_period(self):
#         result = get_files_info("calculator", ".")
#         self.assertIsInstance(result, str)
#         print("Test 1: get_files_info('calculator', '.')")
#         print(result)
#         print()

#     # Test 2: Run get_files_info("calculator", "pkg")
#     def test_calculator_pkg(self):
#         pkg_path = os.path.join("calculator", "pkg")
#         os.makedirs(pkg_path, exist_ok=True)
#         result = get_files_info("calculator", "pkg")
#         self.assertIsInstance(result, str)
#         print("Test 2: get_files_info('calculator', 'pkg')")
#         print(result)
#         print()

#     # Test 3: Run get_files_info("calculator", "/bin")
#     def test_calculator_bin(self):
#         result = get_files_info("calculator", "/bin")
#         self.assertTrue(result.startswith("Error:"))
#         print("Test 3: get_files_info('calculator', '/bin')")
#         print(result)
#         print()

#     # Test 4: Run get_files_info("calculator", "../")
#     def test_calculator_twodots(self):
#         result = get_files_info("calculator", "../")
#         self.assertTrue(result.startswith("Error:"))
#         print("Test 4: get_files_info('calculator', '../')")
#         print(result)
#         print()

# class Test_get_file_content(unittest.TestCase):
    # Test 1: Run get_files_info("calculator", "lorem.txt")
    # def test_truncation(self):
    #     working_dir = os.path.abspath("calculator")
    #     test_file_path = os.path.join(working_dir, "lorem.txt")
    #     # Ensure the working directory exists
    #     os.makedirs(working_dir, exist_ok=True)

    #     result = get_file_content(working_dir, test_file_path)
    #     trunc_msg = f'\n[...File "{test_file_path}" truncated at 10000 characters]'
    #     expected_length = 10000 + len(trunc_msg)
    #     self.assertEqual(len(result), expected_length)
    #     self.assertTrue(result.endswith(trunc_msg))
    #     print("Test 1: get_file_content with truncated file")
    #     print(result[:100])
    #     print(result[-len(trunc_msg):])

    # Test real #1: Run get_files_info("calculator", "main.py")
    # def test_get_main_content(self):
    #     working_dir = os.path.abspath("calculator")
    #     test_file_path = os.path.join(working_dir, "main.py")
    #     result = get_file_content(working_dir, test_file_path)
    #     self.assertTrue("calculator = Calculator()" in result)
    #     # self.assertEqual(result, test_file_path)
    #     print("Test real 1: Valid file content")
    #     print(result)

    # # Test 2: Test valid file in a subdirectory
    # def test_get_pkgcalc_content(self):
    #     working_dir = os.path.abspath("calculator")
    #     pkg_dir = os.path.join(working_dir, "pkg")
    #     test_file_path = os.path.join(pkg_dir, "calculator.py")
    #     result = get_file_content(working_dir, test_file_path)
    #     self.assertTrue("class Calculator:" in result)
    #     print("Test 2: get_file_content('calculator', 'pkg/calculator.py')")
    #     print(result)

    # # Test 3: Test if file outside the working directory returns an error.
    # def test_get_file_bin_content(self):
    #     working_dir = os.path.abspath("calculator")
    #     result = get_file_content(working_dir, "/bin/cat")
    #     self.assertTrue(result.startswith("Error:"))
    #     print("Test 3: get_file_content('calculator', '/bin/cat')")
    #     print(result)

class Test_write_file(unittest.TestCase):
    # Test 1: Valid file within the working directory
    def test_valid_file_write(self):
        working_dir = os.path.abspath("calculator")
        test_file_path = os.path.join(working_dir, "lorem.txt")
        content = "wait, this isn't lorem ipsum"

        os.makedirs(working_dir, exist_ok=True)
        result = write_file(working_dir, test_file_path, content)
        self.assertEqual(result, f'Successfully wrote to "{test_file_path}" ({len(content)} characters written)')
        
        with open(test_file_path, "r") as file:
            self.assertEqual(file.read(), content)

        print("Test 1: write_file('calculator', 'lorem.txt')")
        print(result)

    # Test 2: Valid file in a subdirectory
    def test_valid_file_subdirectory(self):
        working_dir = os.path.abspath("calculator")
        sub_dir = os.path.join(working_dir, "pkg")
        test_file_path = os.path.join(sub_dir, "morelorem.txt")
        content = "lorem ipsum dolor sit amet"

        result = write_file(working_dir, test_file_path, content)
        self.assertEqual(result, f'Successfully wrote to "{test_file_path}" ({len(content)} characters written)')
        
        with open(test_file_path, "r") as file:
            self.assertEqual(file.read(), content)

        print("Test 2: write_file_subdir('calculator', 'morelorem.txt')")
        print(result)

    # Test 3: File outside working directory
    def test_file_outside_working_directory(self):
        working_dir = os.path.abspath("calculator")
        content = "this should not be allowed"

        result = write_file(working_dir, "/tmp/temp.txt", content)
        self.assertTrue(result.startswith("Error:"))
        self.assertIn(f'Cannot write to "{os.path.abspath("/tmp/temp.txt")}"', result)
        
        print("Test 3: write_file('calculator', 'temp.txt')")
        print(result)


if __name__ == "__main__":
    unittest.main()