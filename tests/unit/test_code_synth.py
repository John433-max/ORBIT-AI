from code_synth import synthesize_and_verify, synthesize_python, verify_source, TEMPLATES


def test_add_multiply_subtract():
    assert "return a + b" in synthesize_python("write a python function that adds two numbers")
    assert "def multiply" in synthesize_python("implement a python function that multiplies two numbers")
    assert "return a - b" in synthesize_python("write a python function that subtracts two numbers")


def test_max_reverse_factorial():
    assert "def maximum" in synthesize_python("write a function that returns the maximum of two numbers")
    assert "[::-1]" in synthesize_python("implement a python function to reverse a string")
    assert "def reverse_list" in synthesize_python("write a python function that reverses a list")
    assert "def factorial" in synthesize_python("write a python function for factorial")


def test_divide_average_abs_power():
    assert "def divide" in synthesize_python("write a python function that divides two numbers")
    assert "return a / b" in synthesize_python("implement a python function that divides two numbers")
    assert "def average" in synthesize_python("write a python function that averages two numbers")
    assert "def absolute" in synthesize_python("write a python function for the absolute value")
    assert "def power" in synthesize_python("write a python function that raises a number to a power")


def test_sort_palindrome_even():
    assert "return sorted(items)" in synthesize_python(
        "write a python function that sorts a list"
    )
    assert "def is_palindrome" in synthesize_python(
        "implement a python function that checks if a string is a palindrome"
    )
    assert "n % 2 == 0" in synthesize_python(
        "write a python function that checks if a number is even"
    )


def test_gcd_fib_vowels_unique():
    assert "while b:" in synthesize_python("write a python function that computes the gcd of two numbers")
    assert "def fibonacci" in synthesize_python("implement a python function for the nth fibonacci number")
    assert "aeiou" in synthesize_python("write a python function that counts vowels in a string")
    assert "seen" in synthesize_python("write a python function that returns unique items from a list")


def test_p34_identical_target_xor_consistent_dest_kth():
    assert "def num_identical_pairs" in synthesize_python(
        "write a python function that number of identical pairs"
    )
    assert "def create_target_array" in synthesize_python(
        "write a python function that create target array"
    )
    assert "def xor_operation" in synthesize_python(
        "write a python function that xor operation in an array"
    )
    assert "def count_consistent_strings" in synthesize_python(
        "write a python function that count the number of consistent strings"
    )
    assert "def unique_ints_sum_zero" in synthesize_python(
        "write a python function that n unique integers sum to zero"
    )
    assert "def max_score_after_splitting" in synthesize_python(
        "write a python function that maximum score after splitting a string"
    )
    for prompt in (
        "write a python function that number of identical pairs",
        "write a python function that create target array",
        "write a python function that xor operation in an array",
        "write a python function that count the number of consistent strings",
        "write a python function that n unique integers sum to zero",
        "write a python function that maximum score after splitting a string",
    ):
        bundle = synthesize_and_verify(prompt)
        assert bundle["verified"] is True, (prompt, bundle)


def test_p35_items_product_triplets_center_odds_special():
    assert "def count_items_matching" in synthesize_python(
        "write a python function that count the items matching a rule"
    )
    assert "def max_product_difference" in synthesize_python(
        "write a python function that maximum product difference between two pairs"
    )
    assert "def count_good_triplets" in synthesize_python(
        "write a python function that count the good triplets"
    )
    assert "def find_center" in synthesize_python(
        "write a python function that find the center of a star graph"
    )
    assert "def three_consecutive_odds" in synthesize_python(
        "write a python function that three consecutive odd numbers"
    )
    assert "def special_array" in synthesize_python(
        "write a python function that special array with x elements greater than or equal x"
    )
    for prompt in (
        "write a python function that count the items matching a rule",
        "write a python function that maximum product difference between two pairs",
        "write a python function that count the good triplets",
        "write a python function that find the center of a star graph",
        "write a python function that three consecutive odd numbers",
        "write a python function that special array with x elements greater than or equal x",
    ):
        bundle = synthesize_and_verify(prompt)
        assert bundle["verified"] is True, (prompt, bundle)


def test_p36_shuffle_power_kth_goal_busy_points():
    assert "def shuffle_string" in synthesize_python(
        "write a python function that shuffle a string given indices"
    )
    assert "def max_power" in synthesize_python(
        "write a python function that max power of a string"
    )
    assert "def count_good_rectangles" in synthesize_python(
        "write a python function that count good rectangles"
    )
    assert "def interpret" in synthesize_python(
        "write a python function that goal parser interpretation"
    )
    assert "def busy_student" in synthesize_python(
        "write a python function that students doing homework at a given time"
    )
    assert "def min_time_to_visit_all_points" in synthesize_python(
        "write a python function that min time to visit all points"
    )
    for prompt in (
        "write a python function that shuffle a string given indices",
        "write a python function that max power of a string",
        "write a python function that count good rectangles",
        "write a python function that goal parser interpretation",
        "write a python function that students doing homework at a given time",
        "write a python function that min time to visit all points",
    ):
        bundle = synthesize_and_verify(prompt)
        assert bundle["verified"] is True, (prompt, bundle)


def test_p38_perm_concat_ops_sign_truncate_matches():
    cases = {
        "write a python function that build array from permutation": "def build_array_from_permutation",
        "write a python function that concatenation of array": "def concatenation_of_array",
        "write a python function that final value of variable after performing operations": "def final_value_after_operations",
        "write a python function that sign of the product of an array": "def sign_of_product",
        "write a python function that truncate a sentence": "def truncate_sentence",
        "write a python function that count of matches in a tournament": "def count_matches",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def shuffle_string" not in synthesize_python(
        "write a python function that concatenation of array"
    )
    assert "def build_array_from_permutation" not in synthesize_python(
        "write a python function that shuffle a string given indices"
    )


def test_all_templates_verify():
    assert TEMPLATES
    for tmpl in TEMPLATES:
        check = verify_source(tmpl.source, tmpl.examples)
        assert check["ok"], (tmpl.name, check)


def test_synthesize_and_verify_add():
    bundle = synthesize_and_verify("write a python function that adds two numbers")
    assert bundle["verified"] is True
    assert bundle["checked"] >= 2
    assert "return a + b" in bundle["source"]


def test_odd_and_sum_list():
    assert "n % 2 != 0" in synthesize_python(
        "write a python function that checks if a number is odd"
    )
    assert "def sum_list" in synthesize_python(
        "write a python function that sums a list of numbers"
    )
    odd = synthesize_and_verify("write a python function that checks if a number is odd")
    assert odd["verified"] is True
    sl = synthesize_and_verify("write a python function that sums a list")
    assert sl["verified"] is True


def test_lcm_flatten_words_clamp_prime():
    assert "def lcm" in synthesize_python(
        "write a python function that computes the lcm of two numbers"
    )
    assert "out.extend" in synthesize_python(
        "write a python function that flattens a nested list"
    )
    assert "split()" in synthesize_python(
        "write a python function that counts words in a string"
    )
    assert "def clamp" in synthesize_python(
        "write a python function that clamps a number to a range"
    )
    assert "def is_prime" in synthesize_python(
        "write a python function that checks if a number is prime"
    )
    for q in (
        "write a python function that computes the lcm of two numbers",
        "write a python function that flattens a nested list",
        "write a python function that counts words in a string",
        "write a python function that clamps a number to a range",
        "write a python function that checks if a number is prime",
    ):
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_median_title_count_leap_fizz_bsearch_transpose():
    cases = {
        "write a python function that computes the median of a list": "def median",
        "write a python function that title cases a string": "def title_case",
        "write a python function that counts occurrences of a value in a list": "def count_occurrences",
        "write a python function that checks if a year is a leap year": "def is_leap_year",
        "write a python function for fizzbuzz": "def fizzbuzz",
        "write a python function that binary searches a sorted list": "def binary_search",
        "write a python function that transposes a matrix": "def transpose",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_two_sum_anagram_dot_reverse_list():
    cases = {
        "write a python function that solves two sum": "def two_sum",
        "write a python function that checks if two strings are anagrams": "def is_anagram",
        "write a python function that computes the dot product of two lists": "def dot_product",
        "write a python function that reverses a list": "def reverse_list",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    sl = synthesize_python("write a python function that sums a list of numbers")
    assert "def sum_list" in sl
    rs = synthesize_python("implement a python function to reverse a string")
    assert "def reverse_string" in rs


def test_merge_intersect_rotate_hamming_caesar_majority():
    cases = {
        "write a python function that merges two sorted lists": "def merge_sorted",
        "write a python function that returns the intersection of two lists": "def intersection",
        "write a python function that rotates a list": "def rotate_list",
        "write a python function that computes hamming distance": "def hamming_distance",
        "write a python function that applies a caesar shift": "def caesar_shift",
        "write a python function that finds the majority element": "def majority_element",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    # collisions
    assert "def sort_list" not in synthesize_python(
        "write a python function that merges two sorted lists"
    )
    assert "def reverse_list" not in synthesize_python(
        "write a python function that rotates a list"
    )


def test_parens_lcp_sorted_chunk_union_diff():
    cases = {
        "write a python function that checks balanced parentheses": "def valid_parentheses",
        "write a python function that finds the longest common prefix": "def longest_common_prefix",
        "write a python function that checks if a list is sorted": "def is_sorted",
        "write a python function that chunks a list": "def chunk_list",
        "write a python function that returns the union of two lists": "def list_union",
        "write a python function that returns the difference of two lists": "def list_difference",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def sort_list" not in synthesize_python(
        "write a python function that checks if a list is sorted"
    )
    assert "def intersection" not in synthesize_python(
        "write a python function that returns the union of two lists"
    )
    assert "def subtract" not in synthesize_python(
        "write a python function that returns the difference of two lists"
    )


def test_running_dup_missing_pow2_lastword_plusone():
    cases = {
        "write a python function that computes the running sum of a list": "def running_sum",
        "write a python function that checks if a list contains duplicates": "def contains_duplicate",
        "write a python function that finds the missing number": "def missing_number",
        "write a python function that checks if a number is a power of two": "def is_power_of_two",
        "write a python function that returns the length of the last word": "def length_of_last_word",
        "write a python function that plus one a digit list": "def plus_one",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def sum_list" not in synthesize_python(
        "write a python function that computes the running sum of a list"
    )
    assert "def power" not in synthesize_python(
        "write a python function that checks if a number is a power of two"
    )
    assert "def unique" not in synthesize_python(
        "write a python function that checks if a list contains duplicates"
    )


def test_kadane_stairs_single_zeroes_roman_firstuniq():
    cases = {
        "write a python function that computes the maximum subarray sum": "def max_subarray",
        "write a python function that climbs stairs": "def climb_stairs",
        "write a python function that finds the single number": "def single_number",
        "write a python function that moves zeroes to the end": "def move_zeroes",
        "write a python function that converts a roman numeral": "def roman_to_int",
        "write a python function that finds the first unique character": "def first_unique_char",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def unique" not in synthesize_python(
        "write a python function that finds the first unique character"
    )
    assert "def sum_list" not in synthesize_python(
        "write a python function that computes the maximum subarray sum"
    )


def test_stock_robber_jump_dedup_product_peak():
    cases = {
        "write a python function that computes max profit on a stock": "def max_profit",
        "write a python function for the house robber": "def house_robber",
        "write a python function for the jump game": "def can_jump",
        "write a python function that removes duplicates from a sorted list": "def remove_duplicates",
        "write a python function that computes the product except self": "def product_except_self",
        "write a python function that finds a peak element": "def find_peak",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def unique" not in synthesize_python(
        "write a python function that removes duplicates from a sorted list"
    )
    assert "def max_subarray" not in synthesize_python(
        "write a python function that computes max profit on a stock"
    )


def test_coin_lis_path_word_rotated():
    cases = {
        "write a python function that computes coin change": "def coin_change",
        "write a python function for the longest increasing subsequence": "def lis",
        "write a python function that computes the minimum path sum": "def min_path_sum",
        "write a python function that counts unique paths on a grid": "def unique_paths",
        "write a python function that solves word break": "def word_break",
        "write a python function that searches a rotated sorted array": "def search_rotated",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def unique(" not in synthesize_python(
        "write a python function that counts unique paths on a grid"
    )
    assert "def binary_search" not in synthesize_python(
        "write a python function that searches a rotated sorted array"
    )
    assert "def sum_list" not in synthesize_python(
        "write a python function that computes the minimum path sum"
    )


def test_threesum_edit_course_combo_group_merge():
    cases = {
        "write a python function that solves three sum": "def three_sum",
        "write a python function that computes edit distance": "def edit_distance",
        "write a python function for the course schedule": "def course_schedule",
        "write a python function that computes combination sum": "def combination_sum",
        "write a python function that groups anagrams": "def group_anagrams",
        "write a python function that merges overlapping intervals": "def merge_intervals",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def two_sum" not in synthesize_python(
        "write a python function that solves three sum"
    )
    assert "def is_anagram" not in synthesize_python(
        "write a python function that groups anagrams"
    )
    assert "def coin_change" not in synthesize_python(
        "write a python function that computes combination sum"
    )
    assert "def sum_list" not in synthesize_python(
        "write a python function that solves three sum"
    )


def test_subseq_happy_binary_words_strstr_parens():
    cases = {
        "write a python function that checks if a string is a subsequence of another": "def is_subsequence",
        "write a python function that checks a happy number": "def happy_number",
        "write a python function that adds two binary strings": "def add_binary",
        "write a python function that reverses the order of words in a string": "def reverse_words",
        "write a python function that finds the index of the first occurrence of a needle": "def str_str",
        "write a python function that generates valid parentheses": "def generate_parentheses",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def reverse_string" not in synthesize_python(
        "write a python function that reverses the order of words in a string"
    )
    assert "def valid_parentheses" not in synthesize_python(
        "write a python function that generates valid parentheses"
    )
    assert "def is_palindrome" not in synthesize_python(
        "write a python function that checks if a string is a subsequence of another"
    )


def test_ugly_cycle_pascal_spiral_zeroes_longpal():
    cases = {
        "implement a function that computes the nth ugly number": "def ugly_number",
        "write a function to detect a cycle in a linked list": "def has_cycle",
        "write a python function that builds pascal's triangle": "def pascal_triangle",
        "write a python function that returns a matrix in spiral order": "def spiral_order",
        "write a python function that sets matrix zeroes": "def set_zeroes",
        "write a python function for the longest palindrome that can be built": "def longest_palindrome",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def is_palindrome" not in synthesize_python(
        "write a python function for the longest palindrome that can be built"
    )


def test_decode_trap_nextperm_consec_rotateimg_minwin():
    cases = {
        "write a python function that computes decode ways": "def decode_ways",
        "write a python function that traps rain water": "def trap_rain_water",
        "write a python function that finds the next permutation": "def next_permutation",
        "write a python function for the longest consecutive sequence": "def longest_consecutive",
        "write a python function that rotates an image 90 degrees clockwise": "def rotate_image",
        "write a python function for the minimum window substring": "def min_window",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def rotate_list" not in synthesize_python(
        "write a python function that rotates an image 90 degrees clockwise"
    )
    assert "def longest_palindrome" not in synthesize_python(
        "write a python function for the longest consecutive sequence"
    )
    assert "def can_jump" not in synthesize_python(
        "write a python function that traps rain water"
    )


def test_jump2_paths2_wordsearch_islands_partition_square():
    cases = {
        "write a python function for jump game II minimum jumps": "def jump_game_ii",
        "write a python function for unique paths II with obstacles": "def unique_paths_ii",
        "write a python function for word search on a board": "def word_search",
        "write a python function that counts the number of islands": "def num_islands",
        "write a python function that can partition equal subset sum": "def can_partition",
        "write a python function for the maximal square of ones": "def maximal_square",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def can_jump" not in synthesize_python(
        "write a python function for jump game II minimum jumps"
    )
    assert "def unique_paths(" not in synthesize_python(
        "write a python function for unique paths II with obstacles"
    )
    assert "def word_break" not in synthesize_python(
        "write a python function for word search on a board"
    )


def test_robber2_coin2_invert_level_depth_diameter():
    cases = {
        "write a python function for house robber II circular houses": "def house_robber_ii",
        "write a python function for coin change II number of combinations": "def coin_change_ii",
        "write a python function that inverts a binary tree": "def invert_binary_tree",
        "write a python function for level-order traversal of a binary tree": "def level_order",
        "write a python function for the maximum depth of a binary tree": "def max_depth",
        "write a python function for the diameter of a binary tree": "def diameter_of_binary_tree",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def house_robber_ii" not in synthesize_python(
        "write a python function for the house robber"
    )
    assert "def coin_change_ii" not in synthesize_python(
        "write a python function that computes coin change"
    )


def test_schedule2_same_symmetric_path_bst_lca():
    cases = {
        "write a python function for course schedule II topological order": "def course_schedule_ii",
        "write a python function that checks if two trees are the same tree": "def is_same_tree",
        "write a python function for a symmetric binary tree": "def is_symmetric",
        "write a python function for path sum root-to-leaf": "def path_sum",
        "write a python function that validates a binary search tree": "def is_valid_bst",
        "write a python function for the lowest common ancestor": "def lowest_common_ancestor",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def course_schedule_ii" not in synthesize_python(
        "write a python function that can finish all courses"
    )
    assert "def course_schedule(" not in synthesize_python(
        "write a python function for course schedule II topological order"
    )


def test_linked_list_templates():
    cases = {
        "write a python function that reverses a linked list": "def reverse_linked_list",
        "write a python function that merges two sorted linked lists": "def merge_two_lists",
        "write a python function for the middle of a linked list": "def middle_node",
        "write a python function that removes nth node from the end": "def remove_nth_from_end",
        "write a python function that swaps nodes in pairs": "def swap_pairs",
        "write a python function that deletes duplicates from a sorted linked list": "def delete_duplicates",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def reverse_linked_list" not in synthesize_python(
        "write a python function that reverses a list"
    )
    assert "def merge_two_lists" not in synthesize_python(
        "write a python function that merges two sorted lists"
    )


def test_linked_list_cycle229():
    cases = {
        "write a python function that adds two numbers stored as reversed linked lists": "def add_two_numbers",
        "write a python function that checks if a linked list is a palindrome": "def palindrome_linked_list",
        "write a python function for the odd even linked list": "def odd_even_list",
        "write a python function for the intersection node of two linked lists": "def get_intersection_node",
        "write a python function that rotates a linked list to the right": "def rotate_right",
        "write a python function that partitions a linked list": "def partition_list",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def add(" not in synthesize_python(
        "write a python function that adds two numbers stored as reversed linked lists"
    )
    assert "def is_palindrome" not in synthesize_python(
        "write a python function that checks if a linked list is a palindrome"
    )
    assert "def rotate_list" not in synthesize_python(
        "write a python function that rotates a linked list to the right"
    )
    assert "def can_partition" not in synthesize_python(
        "write a python function that partitions a linked list"
    )
    assert "def intersection(" not in synthesize_python(
        "write a python function for the intersection node of two linked lists"
    )


def test_linked_list_cycle231():
    cases = {
        "write a python function that reverses a linked list between left and right positions": "def reverse_between",
        "write a python function that removes linked list elements equal to a value": "def remove_elements",
        "write a python function that reorders a linked list": "def reorder_list",
        "write a python function that sorts a linked list": "def sort_linked_list",
        "write a python function that deletes a node in a linked list given only that node": "def delete_node",
        "write a python function that insertion sorts a linked list": "def insertion_sort_list",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def reverse_linked_list" not in synthesize_python(
        "write a python function that reverses a linked list between left and right positions"
    )
    assert "def sort_list(" not in synthesize_python(
        "write a python function that sorts a linked list"
    )
    assert "def delete_duplicates" not in synthesize_python(
        "write a python function that deletes a node in a linked list given only that node"
    )
    assert "def remove_nth_from_end" not in synthesize_python(
        "write a python function that removes linked list elements equal to a value"
    )


def test_linked_list_cycle233():
    cases = {
        "write a python function that copies a linked list with random pointer": "def copy_random_list",
        "write a python function that flattens a multilevel doubly linked list": "def flatten_multilevel",
        "write a python function that deletes all nodes that have duplicates from a sorted linked list": "def delete_duplicates_ii",
        "write a python function that reverses nodes in k group": "def reverse_k_group",
        "write a python function that splits a linked list into parts": "def split_list_to_parts",
        "write a python function that plus-one a linked list": "def plus_one_linked_list",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def flatten(" not in synthesize_python(
        "write a python function that flattens a multilevel doubly linked list"
    )
    assert "def delete_duplicates(" not in synthesize_python(
        "write a python function that deletes all nodes that have duplicates from a sorted linked list"
    )
    assert "def plus_one(" not in synthesize_python(
        "write a python function that plus-one a linked list"
    )
    assert "def flatten_multilevel" not in synthesize_python(
        "write a python function that flattens a nested list"
    )


def test_cycle234_graph_heap_string():
    cases = {
        "write a python function that clones a graph": "def clone_graph",
        "write a python function for top k frequent elements": "def top_k_frequent",
        "write a python function that finds the kth largest element": "def find_kth_largest",
        "write a python function for longest substring without repeating characters": "def length_of_longest_substring",
        "write a python function for daily temperatures": "def daily_temperatures",
        "write a python function that merges k sorted linked lists": "def merge_k_lists",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def merge_two_lists" not in synthesize_python(
        "write a python function that merges k sorted linked lists"
    )
    assert "def merge_k_lists" not in synthesize_python(
        "write a python function that merges two sorted linked lists"
    )
    assert "def longest_palindrome" not in synthesize_python(
        "write a python function for longest substring without repeating characters"
    )


def test_cycle235_grid_graph():
    cases = {
        "write a python function that computes rotting oranges": "def rotting_oranges",
        "write a python function for pacific atlantic water flow": "def pacific_atlantic",
        "write a python function that flood fills an image": "def flood_fill",
        "write a python function for the 01 matrix nearest zero": "def update_matrix",
        "write a python function that counts the number of provinces": "def num_provinces",
        "write a python function that captures surrounded regions": "def surrounded_regions",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def num_islands" not in synthesize_python(
        "write a python function that flood fills an image"
    )
    assert "def flood_fill" not in synthesize_python(
        "write a python function that counts the number of islands"
    )


def test_cycle236_tree_bst():
    cases = {
        "write a python function for the minimum depth of a binary tree": "def min_depth",
        "write a python function that finds the kth smallest element in a bst": "def kth_smallest",
        "write a python function for binary tree right side view": "def right_side_view",
        "write a python function that converts a sorted array to a height-balanced bst": "def sorted_array_to_bst",
        "write a python function for binary tree zigzag level order traversal": "def zigzag_level_order",
        "write a python function for the range sum of bst": "def range_sum_bst",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def max_depth" not in synthesize_python(
        "write a python function for the minimum depth of a binary tree"
    )
    assert "def kth_smallest" not in synthesize_python(
        "write a python function that finds the kth largest element"
    )
    assert "def level_order" not in synthesize_python(
        "write a python function for binary tree zigzag level order traversal"
    )


def test_cycle237_backtrack_paths():
    cases = {
        "write a python function that returns all subsets of a list": "def subsets",
        "write a python function that generates all permutations of a list": "def permute",
        "write a python function for letter combinations of a phone number": "def letter_combinations",
        "write a python function for combination sum ii": "def combination_sum_ii",
        "write a python function for path sum ii": "def path_sum_ii",
        "write a python function for binary tree paths": "def binary_tree_paths",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def combination_sum_ii" not in synthesize_python(
        "write a python function for combination sum"
    )
    assert "def combination_sum(" not in synthesize_python(
        "write a python function for combination sum ii"
    )
    assert "def path_sum_ii" not in synthesize_python(
        "write a python function for path sum"
    )
    assert "def path_sum(" not in synthesize_python(
        "write a python function for path sum ii"
    )
    assert "def permute" not in synthesize_python(
        "write a python function for next permutation"
    )
    assert "def binary_tree_paths" not in synthesize_python(
        "write a python function for all root-to-leaf paths that sum"
    )


def test_cycle238_tree_walks_and_matrix():
    cases = {
        "write a python function for inorder traversal of a binary tree": "def inorder_traversal",
        "write a python function for preorder traversal of a binary tree": "def preorder_traversal",
        "write a python function for postorder traversal of a binary tree": "def postorder_traversal",
        "write a python function for the maximum path sum of a binary tree": "def max_path_sum",
        "write a python function that flattens a binary tree to a linked list": "def flatten_binary_tree",
        "write a python function that searches a 2d matrix": "def search_matrix",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def path_sum(" not in synthesize_python(
        "write a python function for the maximum path sum of a binary tree"
    )
    assert "def max_path_sum" not in synthesize_python(
        "write a python function for path sum"
    )
    assert "def flatten(" not in synthesize_python(
        "write a python function that flattens a binary tree to a linked list"
    )
    assert "def flatten_binary_tree" not in synthesize_python(
        "write a python function that flattens a nested list"
    )
    assert "def search_rotated" not in synthesize_python(
        "write a python function that searches a 2d matrix"
    )
    assert "def search_matrix" not in synthesize_python(
        "write a python function that searches in a rotated sorted array"
    )


def test_cycle239_stack_decode_rpn():
    cases = {
        "write a python function that implements a min stack": "def min_stack",
        "write a python function that decodes a string": "def decode_string",
        "write a python function for the next greater element": "def next_greater_element",
        "write a python function that evaluates reverse polish notation": "def eval_rpn",
        "write a python function for asteroid collision": "def asteroid_collision",
        "write a python function that implements a queue using stacks": "def queue_using_stacks",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def minimum(" not in synthesize_python(
        "write a python function that implements a min stack"
    )
    assert "def decode_ways" not in synthesize_python(
        "write a python function that decodes a string"
    )
    assert "def decode_string" not in synthesize_python(
        "write a python function that counts decode ways"
    )
    assert "def daily_temperatures" not in synthesize_python(
        "write a python function for the next greater element"
    )


def test_cycle240_heap_templates():
    cases = {
        "write a python function for last stone weight": "def last_stone_weight",
        "write a python function for a task scheduler": "def task_scheduler",
        "write a python function that reorganizes a string so no two adjacent characters are the same": "def reorganize_string",
        "write a python function for the sliding window maximum": "def sliding_window_maximum",
        "write a python function for k closest points to the origin": "def k_closest",
        "write a python function that finds the median from a data stream": "def median_finder",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def median(" not in synthesize_python(
        "write a python function that finds the median from a data stream"
    )
    assert "def median_finder" not in synthesize_python(
        "write a python function for the median of a list"
    )
    assert "def min_window" not in synthesize_python(
        "write a python function for the sliding window maximum"
    )
    assert "def sliding_window_maximum" not in synthesize_python(
        "write a python function for the minimum window substring"
    )


def test_container_sort_colors_dup_gas_lru_trie():
    cases = {
        "write a python function for container with most water": "def container_with_most_water",
        "write a python function that sort colors using the dutch flag": "def sort_colors",
        "write a python function that finds the duplicate number": "def find_duplicate",
        "write a python function for the gas station circuit": "def can_complete_circuit",
        "write a python function that implements an lru cache": "def lru_cache",
        "write a python function that implements a trie": "def implement_trie",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def sort_list" not in synthesize_python(
        "write a python function that sort colors using the dutch flag"
    )
    assert "def contains_duplicate" not in synthesize_python(
        "write a python function that finds the duplicate number"
    )
    assert "def median_finder" not in synthesize_python(
        "write a python function that implements an lru cache"
    )


def test_cycle241_graph_schedule_templates():
    cases = {
        "write a python function for network delay time": "def network_delay_time",
        "write a python function for meeting rooms ii": "def meeting_rooms_ii",
        "write a python function for cheapest flights with k stops": "def cheapest_flights",
        "write a python function for word ladder": "def word_ladder",
        "write a python function that counts connected components": "def count_components",
        "write a python function that reconstructs an itinerary": "def find_itinerary",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def word_search" not in synthesize_python(
        "write a python function for word ladder"
    )
    assert "def num_provinces" not in synthesize_python(
        "write a python function that counts connected components"
    )
    assert "def merge_intervals" not in synthesize_python(
        "write a python function for meeting rooms ii"
    )


def test_cycle242_unionfind_topo_templates():
    cases = {
        "write a python function for alien dictionary": "def alien_dictionary",
        "write a python function that merges accounts": "def accounts_merge",
        "write a python function for redundant connection": "def redundant_connection",
        "write a python function that checks if a graph is a valid tree": "def valid_tree",
        "write a python function for minimum height trees": "def min_height_trees",
        "write a python function for critical connections": "def critical_connections",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def course_schedule" not in synthesize_python(
        "write a python function for alien dictionary"
    )
    assert "def count_components" not in synthesize_python(
        "write a python function that checks if a graph is a valid tree"
    )
    assert "def is_valid_bst" not in synthesize_python(
        "write a python function that checks if a graph is a valid tree"
    )


def test_cycle244_tree_graph_templates():
    cases = {
        "write a python function that builds a binary tree from preorder and inorder": "def build_tree",
        "write a python function for house robber iii": "def house_robber_iii",
        "write a python function for the longest increasing path in a matrix": "def longest_increasing_path",
        "write a python function for word break ii": "def word_break_ii",
        "write a python function that connects points with minimum cost": "def min_cost_connect_points",
        "write a python function that counts unique binary search trees": "def num_trees",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def house_robber_iii" not in synthesize_python(
        "write a python function for house robber"
    )
    assert "def house_robber_iii" not in synthesize_python(
        "write a python function for house robber ii"
    )
    assert "def word_break_ii" not in synthesize_python(
        "write a python function for word break"
    )
    assert "def binary_search" not in synthesize_python(
        "write a python function that counts unique binary search trees"
    )
    assert "def lis" not in synthesize_python(
        "write a python function for the longest increasing path in a matrix"
    )


def test_cycle245_hard_dp_stack_templates():
    cases = {
        "write a python function for the median of two sorted arrays": "def find_median_sorted_arrays",
        "write a python function for the largest rectangle in a histogram": "def largest_rectangle_histogram",
        "write a python function for maximal rectangle": "def maximal_rectangle",
        "write a python function that distributes candy by ratings": "def candy",
        "write a python function for longest valid parentheses": "def longest_valid_parentheses",
        "write a python function for interleaving string": "def is_interleave",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def find_median_sorted_arrays" not in synthesize_python(
        "write a python function for median finder"
    )
    assert "def valid_parentheses" not in synthesize_python(
        "write a python function for longest valid parentheses"
    )
    assert "def largest_rectangle_histogram" not in synthesize_python(
        "write a python function for maximal rectangle"
    )
    assert "def container_with_most_water" not in synthesize_python(
        "write a python function for the largest rectangle in a histogram"
    )


def test_cycle246_hard_search_dp_templates():
    cases = {
        "write a python function that bursts balloons for max coins": "def burst_balloons",
        "write a python function for word search ii": "def word_search_ii",
        "write a python function for palindrome partitioning": "def palindrome_partition",
        "write a python function that serializes a binary tree": "def serialize_tree",
        "write a python function for counts of smaller numbers after self": "def count_smaller",
        "write a python function for buy and sell stock with cooldown": "def max_profit_cooldown",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src)
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def word_search_ii" not in synthesize_python(
        "write a python function for word search"
    )
    assert "def max_profit_cooldown" not in synthesize_python(
        "write a python function for best time to buy and sell stock"
    )
    assert "def word_search(" not in synthesize_python(
        "write a python function for word search ii"
    )


def test_cycle249_four_sum_closest_min_squares_bits_subsets_ii():
    cases = {
        "write a python function for four sum": "def four_sum",
        "write a python function for 3sum closest": "def three_sum_closest",
        "write a python function that finds the minimum in a rotated sorted array": "def find_min_rotated",
        "write a python function for perfect squares": "def perfect_squares",
        "write a python function for counting bits": "def count_bits",
        "write a python function for subsets with duplicates": "def subsets_ii",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:80])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def three_sum(" in synthesize_python(
        "write a python function for three sum"
    )
    assert "def three_sum_closest" not in synthesize_python(
        "write a python function for three sum"
    )
    assert "def search_rotated" in synthesize_python(
        "write a python function that searches in a rotated sorted array"
    )
    assert "def find_min_rotated" in synthesize_python(
        "write a python function that finds the minimum in a rotated sorted array"
    )


def test_cycle250_wildcard_regex_lcs_product_target():
    cases = {
        "write a python function for wildcard matching": "def wildcard_matching",
        "write a python function for regular expression matching": "def regex_matching",
        "write a python function for distinct subsequences": "def distinct_subsequences",
        "write a python function for longest common subsequence": "def longest_common_subsequence",
        "write a python function for maximum product subarray": "def max_product_subarray",
        "write a python function for target sum": "def target_sum",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:80])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def lis(" in synthesize_python(
        "write a python function for longest increasing subsequence"
    )
    assert "def longest_common_subsequence" not in synthesize_python(
        "write a python function for longest increasing subsequence"
    )
    assert "def wildcard_matching" not in synthesize_python(
        "write a python function for regular expression matching"
    )


def test_cycle251_subarray_anagrams_queens_calc():
    cases = {
        "write a python function for subarray sum equals k": "def subarray_sum",
        "write a python function for longest repeating character replacement": "def character_replacement",
        "write a python function that finds all anagrams in a string": "def find_all_anagrams",
        "write a python function for first missing positive": "def first_missing_positive",
        "write a python function for n queens": "def n_queens",
        "write a python function for basic calculator ii": "def basic_calculator_ii",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:120])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def is_anagram" not in synthesize_python(
        "write a python function that finds all anagrams in a string"
    )
    assert "def missing_number" not in synthesize_python(
        "write a python function for first missing positive"
    )
    assert "def max_subarray" not in synthesize_python(
        "write a python function for subarray sum equals k"
    )
    assert "def group_anagrams" not in synthesize_python(
        "write a python function that finds all anagrams in a string"
    )


def test_cycle252_lfu_window_burst_wordsearch_median():
    cases = {
        "write a python function for lfu cache": "def lfu_cache",
        "write a python function for sliding window maximum": "def sliding_window_maximum",
        "write a python function to burst balloons": "def burst_balloons",
        "write a python function for word search ii": "def word_search_ii",
        "write a python function that finds median from data stream": "def median_finder",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:160])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def lru_cache" not in synthesize_python(
        "write a python function for lfu cache"
    )
    assert "def word_search_ii" not in synthesize_python(
        "write a python function for word search"
    )
    assert "def word_search(" in synthesize_python(
        "write a python function for word search"
    )


def test_cycle253_design_stream_templates():
    cases = {
        "write a python function for time based key value store": "def time_based_kv",
        "write a python function for insert delete getrandom": "def insert_delete_getrandom",
        "write a python function for moving average from data stream": "def moving_average",
        "write a python function for logger rate limiter": "def logger_rate_limiter",
        "write a python function that designs a hashmap": "def design_hashmap",
        "write a python function for range sum query": "def range_sum_query",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:160])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def average" not in synthesize_python(
        "write a python function for moving average from data stream"
    )
    assert "def range_sum_bst" not in synthesize_python(
        "write a python function for range sum query"
    )
    assert "def median_finder" not in synthesize_python(
        "write a python function for time based key value store"
    )


def test_cycle254_unique_names_and_design():
    from collections import Counter
    from code_synth import get_templates

    names = [t.name for t in get_templates()]
    dups = [n for n, c in Counter(names).items() if c > 1]
    assert dups == [], dups
    cases = {
        "write a python function for snapshot array": "def snapshot_array",
        "write a python function that designs a circular queue": "def circular_queue",
        "write a python function to encode and decode tinyurl": "def encode_decode_tinyurl",
        "write a python function that implements a stack using queues": "def stack_using_queues",
        "write a python function for a parking system": "def parking_system",
        "write a python function that designs a twitter": "def design_twitter",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:180])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def queue_using_stacks" not in synthesize_python(
        "write a python function that implements a stack using queues"
    )
    assert "def circular_queue" not in synthesize_python(
        "write a python function that implements a queue using stacks"
    )


def test_cycle255_browser_underground_stream_design():
    from collections import Counter
    from code_synth import get_templates

    names = [t.name for t in get_templates()]
    dups = [n for n, c in Counter(names).items() if c > 1]
    assert dups == [], dups
    cases = {
        "write a python function for browser history": "def browser_history",
        "write a python function that designs an underground system": "def underground_system",
        "write a python function for product of last k numbers": "def product_of_numbers",
        "write a python function for number of recent calls": "def recent_counter",
        "write a python function for a peeking iterator": "def peeking_iterator",
        "write a python function for stock price fluctuation": "def stock_price",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:180])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def product_except_self" not in synthesize_python(
        "write a python function for product of last k numbers"
    )
    assert "def max_profit" not in synthesize_python(
        "write a python function for stock price fluctuation"
    )
    assert "def stock_price" not in synthesize_python(
        "write a python function for best time to buy and sell stock"
    )


def test_cycle258_array_island_dp():
    from collections import Counter
    from code_synth import get_templates

    names = [t.name for t in get_templates()]
    dups = [n for n, c in Counter(names).items() if c > 1]
    assert dups == [], dups
    cases = {
        "write a python function that finds all duplicates in an array": "def find_all_duplicates",
        "write a python function that finds all numbers disappeared in an array": "def find_disappeared",
        "write a python function for island perimeter": "def island_perimeter",
        "write a python function for next greater element ii circular": "def next_greater_ii",
        "write a python function to delete and earn points": "def delete_and_earn",
        "write a python function for longest palindromic subsequence": "def longest_palindromic_subsequence",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:180])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def find_all_duplicates" not in synthesize_python(
        "write a python function that finds the duplicate number"
    )
    assert "def next_greater_ii" not in synthesize_python(
        "write a python function for next greater element"
    )
    assert "def island_perimeter" not in synthesize_python(
        "write a python function for number of islands"
    )
    assert "def longest_palindromic_subsequence" not in synthesize_python(
        "write a python function for longest palindrome"
    )


def test_cycle260_easy_string_dp():
    cases = {
        "write a python function for min cost climbing stairs": "def min_cost_climbing_stairs",
        "write a python function for search insert position": "def search_insert",
        "write a python function for isomorphic strings": "def isomorphic_strings",
        "implement a function to check if two strings are isomorphic": "def isomorphic_strings",
        "write a python function for word pattern": "def word_pattern",
        "write a python function to reverse an integer": "def reverse_integer",
        "write a python function that add strings representing integers": "def add_strings",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:180])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def min_cost_climbing_stairs" not in synthesize_python(
        "write a python function that climbs stairs"
    )
    assert "def reverse_integer" not in synthesize_python(
        "write a python function to reverse a string"
    )
    assert "def add_strings" not in synthesize_python(
        "write a python function that adds two numbers"
    )


def test_cycle261_string_math_helpers():
    cases = {
        "write a python function that reverses vowels in a string": "def reverse_vowels",
        "write a python function that counts primes less than n": "def count_primes",
        "write a python function that converts an integer to roman": "def integer_to_roman",
        "write a python function for valid palindrome ii delete one character": "def valid_palindrome_ii",
        "write a python function to detect capital use in a word": "def detect_capital",
        "write a python function for integer square root": "def my_sqrt",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def reverse_vowels" not in synthesize_python(
        "write a python function to reverse a string"
    )
    assert "def count_primes" not in synthesize_python(
        "write a python function that checks if a number is prime"
    )
    assert "def integer_to_roman" not in synthesize_python(
        "write a python function that converts a roman numeral"
    )
    assert "def valid_palindrome_ii" not in synthesize_python(
        "write a python function that checks if a string is a palindrome"
    )


def test_cycle262_sudoku_life_pow():
    cases = {
        "write a python function that validates a sudoku board": "def valid_sudoku",
        "write a python function for game of life next board": "def game_of_life",
        "write a python function for count and say": "def count_and_say",
        "write a python function for majority element ii": "def majority_element_ii",
        "write a python function for pow x n with negative exponents": "def my_pow",
        "write a python function that removes duplicates from sorted array ii keep at most two": "def remove_duplicates_ii",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def majority_element_ii" not in synthesize_python(
        "write a python function for majority element boyer moore"
    )
    assert "def remove_duplicates_ii" not in synthesize_python(
        "write a python function that removes duplicates from a sorted list"
    )
    assert "def my_pow" not in synthesize_python(
        "write a python function that raises a number to a power"
    )


def test_cycle263_bits_mountain_ranges():
    cases = {
        "write a python function for single number ii where others appear three times": "def single_number_ii",
        "write a python function for hamming weight number of 1 bits": "def hamming_weight",
        "write a python function that reverse bits of an integer": "def reverse_bits",
        "write a python function that checks if a number is a power of four": "def is_power_of_four",
        "write a python function that checks a valid mountain array": "def valid_mountain_array",
        "write a python function that returns summary ranges": "def summary_ranges",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def single_number_ii" not in synthesize_python(
        "write a python function that finds the single number"
    )
    assert "def hamming_weight" not in synthesize_python(
        "write a python function for hamming distance of two strings"
    )
    assert "def is_power_of_four" not in synthesize_python(
        "write a python function that checks if a number is a power of two"
    )


def test_cycle264_ranges_nim_hex_square():
    cases = {
        "write a python function that returns missing ranges": "def missing_ranges",
        "write a python function for third maximum distinct": "def third_max",
        "write a python function that add digits digital root": "def add_digits",
        "write a python function that checks if a number is a perfect square": "def is_perfect_square",
        "write a python function that can win nim game": "def can_win_nim",
        "write a python function that converts an integer to hexadecimal to_hex": "def to_hex",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def is_perfect_square" not in synthesize_python(
        "write a python function for perfect squares"
    )
    assert "def missing_ranges" not in synthesize_python(
        "write a python function that returns summary ranges"
    )
    assert "def add_digits" not in synthesize_python(
        "write a python function that adds two numbers"
    )


def test_cycle265_license_excel_happy():
    cases = {
        "write a python function that reformats a license key": "def license_key_formatting",
        "write a python function that finds the number complement": "def find_complement",
        "write a python function that returns excel column title": "def convert_to_title",
        "write a python function that returns excel column number": "def title_to_number",
        "write a python function that arrange coins into a staircase": "def arrange_coins",
        "write a python function that lists self-dividing numbers": "def self_dividing_numbers",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def convert_to_title" not in synthesize_python(
        "write a python function that title cases a string"
    )
    assert "def find_complement" not in synthesize_python(
        "write a python function for two's complement hex"
    )
    assert "def arrange_coins" not in synthesize_python(
        "write a python function that counts coins"
    )


def test_cycle266_lemonade_jewels_morse_judge():
    cases = {
        "write a python function that lemonade change": "def lemonade_change",
        "write a python function that robot returns to the origin": "def judge_circle",
        "write a python function that counts jewels in stones": "def num_jewels_in_stones",
        "write a python function that unique morse representations": "def unique_morse_representations",
        "write a python function that finds the town judge": "def find_judge",
        "write a python function for peak index in a mountain array": "def peak_index_in_mountain_array",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def peak_index_in_mountain_array" not in synthesize_python(
        "write a python function that checks a valid mountain array"
    )
    assert "def valid_mountain_array" not in synthesize_python(
        "write a python function for peak index in a mountain array"
    )
    assert "def find_judge" not in synthesize_python(
        "write a python function that first bad version"
    )


def test_p10_unique_email_parity_flip():
    cases = {
        "write a python function that counts unique email addresses": "def unique_email_addresses",
        "write a python function to convert a string to lowercase": "def to_lower_case",
        "write a python function that sort array by parity": "def sort_array_by_parity",
        "write a python function that height checker": "def height_checker",
        "write a python function for shortest distance to character": "def shortest_to_char",
        "write a python function that flip and invert image": "def flip_and_invert_image",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def sort_array_by_parity" not in synthesize_python(
        "write a python function that sorts a list"
    )
    assert "def sort_list" not in synthesize_python(
        "write a python function that sort array by parity"
    )


def test_p11_squares_parity_ii_monotonic_goat():
    cases = {
        "write a python function for squares of a sorted array": "def sorted_squares",
        "write a python function that sort array by parity ii": "def sort_array_by_parity_ii",
        "write a python function that checks if an array is monotonic": "def is_monotonic",
        "write a python function that backspace string compare": "def backspace_compare",
        "write a python function that converts a sentence to goat latin": "def to_goat_latin",
        "write a python function that fair candy swap": "def fair_candy_swap",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def sort_array_by_parity_ii" not in synthesize_python(
        "write a python function that sort array by parity"
    )
    assert "def sort_array_by_parity\n" not in synthesize_python(
        "write a python function that sort array by parity ii"
    )
    assert "def is_sorted" not in synthesize_python(
        "write a python function that checks if an array is monotonic"
    )


def test_p13_gcd_strings_kids_pairs_shuffle():
    cases = {
        "write a python function that gcd of strings": "def gcd_of_strings",
        "write a python function unique number of occurrences": "def unique_occurrences",
        "write a python function kids with the greatest number of candies": "def kids_with_candies",
        "write a python function that remove outermost parentheses": "def remove_outer_parentheses",
        "write a python function that number of good pairs": "def num_good_pairs",
        "write a python function that shuffle the array": "def shuffle_array",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def gcd(" not in synthesize_python(
        "write a python function that gcd of strings"
    )
    assert "def candy(" not in synthesize_python(
        "write a python function kids with the greatest number of candies"
    )


def test_p14_defang_digits_smaller():
    cases = {
        "write a python function that defangs an IP address": "def defang_ip_addr",
        "write a python function that subtract product and sum of digits": "def subtract_product_and_sum",
        "write a python function that decompress run-length encoded list": "def decompress_rl_elist",
        "write a python function that replace elements with the greatest element on the right": "def replace_elements",
        "write a python function that finds numbers with even number of digits": "def find_numbers",
        "write a python function how many numbers are smaller than the current number": "def smaller_numbers_than_current",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def is_even" not in synthesize_python(
        "write a python function that finds numbers with even number of digits"
    )
    assert "def subtract(" not in synthesize_python(
        "write a python function that subtract product and sum of digits"
    )


def test_p15_steps_balloon_double_missing_dest_oddsub():
    cases = {
        "write a python function that number of steps to reduce a number to zero": "def number_of_steps",
        "write a python function maximum number of balloons": "def max_number_of_balloons",
        "write a python function that check if n and its double exist": "def check_if_n_and_double_exist",
        "write a python function that kth missing positive number": "def kth_missing_positive",
        "write a python function that destination city": "def dest_city",
        "write a python function that sum of all odd-length subarrays": "def sum_odd_length_subarrays",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def first_missing_positive" not in synthesize_python(
        "write a python function that kth missing positive number"
    )
    assert "def missing_number" not in synthesize_python(
        "write a python function that kth missing positive number"
    )


def test_p16_degree_pivot_cookies_zeros_lucky():
    cases = {
        "write a python function that degree of an array": "def degree_of_array",
        "write a python function that find the pivot index": "def pivot_index",
        "write a python function that assign cookies": "def assign_cookies",
        "write a python function that duplicate zeros": "def duplicate_zeros",
        "write a python function lucky numbers in a matrix": "def lucky_numbers",
        "write a python function that find the lucky integer in an array": "def find_lucky",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def duplicate_zeros" not in synthesize_python(
        "write a python function that move zeroes"
    )
    assert "def pivot_index" not in synthesize_python(
        "write a python function that find peak"
    )
    assert "def find_lucky" not in synthesize_python(
        "write a python function lucky numbers in a matrix"
    )
    assert "def lucky_numbers" not in synthesize_python(
        "write a python function that find the lucky integer in an array"
    )


def test_p17_ranks_parts_smoother_range_peri_surface():
    cases = {
        "write a python function that relative ranks": "def relative_ranks",
        "write a python function that three parts with equal sum": "def can_three_parts_equal_sum",
        "write a python function that image smoother": "def image_smoother",
        "write a python function that smallest range i": "def smallest_range_i",
        "write a python function that largest perimeter": "def largest_perimeter",
        "write a python function that surface area of 3d shapes": "def surface_area",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p18_uncommon_buddy_groups_error_alt_pattern():
    cases = {
        "write a python function uncommon words from two sentences": "def uncommon_from_sentences",
        "write a python function that buddy strings": "def buddy_strings",
        "write a python function that large group positions": "def large_group_positions",
        "write a python function that set mismatch": "def find_error_nums",
        "write a python function that has alternating bits": "def has_alternating_bits",
        "write a python function that find and replace pattern": "def find_and_replace_pattern",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def word_pattern" not in synthesize_python(
        "write a python function that find and replace pattern"
    )
    assert "def first_missing_positive" not in synthesize_python(
        "write a python function that set mismatch"
    )
    assert "def missing_number" not in synthesize_python(
        "write a python function that set mismatch"
    )


def test_pack21_goat_latin_and_friends():
    cases = {
        "write a python function that goat latin": "def to_goat_latin",
        "write a python function that reordered power of 2": "def reordered_power_of_2",
        "write a python function that prime number of set bits": "def prime_number_of_set_bits",
        "write a python function that valid square": "def valid_square",
        "write a python function that complex number multiply": "def complex_number_multiply",
        "write a python function that convert to base 7": "def convert_to_base7",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:220])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def is_power_of_two" not in synthesize_python(
        "write a python function that reordered power of 2"
    )
    assert "def is_prime" not in synthesize_python(
        "write a python function that prime number of set bits"
    )


def test_ranked_match_prefers_specific_sibling():
    from code_synth import match_template, iter_matching

    q = "write a python function that merge k lists"
    hits = [t.name for t in iter_matching(q)]
    assert "merge_sorted" not in hits
    assert "merge_k_lists" in hits
    picked = match_template(q)
    assert picked is not None and picked.name == "merge_k_lists"
    src = synthesize_python(q)
    assert "def merge_k_lists" in src

    q2 = "write a python function that goat latin"
    assert "def to_goat_latin" in synthesize_python(q2)

    q3 = "write a python function that merges two sorted lists"
    assert "def merge_two_lists" not in synthesize_python(q3)
    assert "def merge_sorted" in synthesize_python(q3)

    q4 = "write a python function that merges two sorted linked lists"
    assert "def merge_two_lists" in synthesize_python(q4)


def test_pack26_array_string_templates():
    cases = {
        "write a python function that two sum ii": "def two_sum_ii",
        "write a python function that two sum of a sorted array": "def two_sum_ii",
        "write a python function that count segments": "def count_segments",
        "write a python function that shortest unsorted continuous subarray": "def find_unsorted_subarray",
        "write a python function that maximum average subarray": "def find_max_average",
        "write a python function that longest continuous increasing": "def find_length_of_lcis",
        "write a python function that longest harmonious subsequence": "def find_lhs",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)

    src = synthesize_python("write a python function that two sum")
    assert "def two_sum(" in src
    assert "def two_sum_ii" not in src


def test_pack27_tree_bst_templates():
    cases = {
        "write a python function that merge two binary trees": "def merge_trees",
        "write a python function that search in a binary search tree": "def search_bst",
        "write a python function that average of levels": "def average_of_levels",
        "write a python function that sum of left leaves": "def sum_of_left_leaves",
        "write a python function that binary tree tilt": "def find_tilt",
        "write a python function that two sum in a bst": "def two_sum_iv",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    src = synthesize_python("write a python function that two sum")
    assert "def two_sum(" in src
    assert "def two_sum_iv" not in src


def test_pack33_easy_templates():
    cases = {
        "write a python function that root equals sum of children": "def check_tree",
        "write a python function that evaluate boolean binary tree": "def evaluate_tree",
        "write a python function that merge strings alternately": "def merge_alternately",
        "write a python function that richest customer wealth": "def richest_customer_wealth",
        "write a python function that find the highest altitude": "def highest_altitude",
        "write a python function that check if the sentence is a pangram": "def check_pangram",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)

    src = synthesize_python("write a python function that returns the maximum of two numbers")
    assert "def maximum(" in src
    assert "def richest_customer_wealth" not in src
    assert "def highest_altitude" not in src


def test_pack32_tree_array_templates():
    cases = {
        "write a python function that construct a string from a binary tree": "def tree2str",
        "write a python function that prune a binary tree": "def prune_tree",
        "write a python function that longest univalue path": "def longest_univalue_path",
        "write a python function that smallest string starting from leaf": "def smallest_from_leaf",
        "write a python function that maximum difference between node and ancestor": "def max_ancestor_diff",
        "write a python function that array pair sum": "def array_pair_sum",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)

    src = synthesize_python("write a python function that univalued binary tree")
    assert "def is_unival_tree(" in src
    assert "def longest_univalue_path" not in src


def test_pack31_tree_templates():
    cases = {
        "write a python function that maximum width of a binary tree": "def width_of_binary_tree",
        "write a python function that minimum difference in a bst": "def min_diff_bst",
        "write a python function that second minimum in a binary tree": "def find_second_minimum",
        "write a python function that lowest common ancestor of a bst": "def lowest_common_ancestor_bst",
        "write a python function that check completeness of a binary tree": "def is_complete_tree",
        "write a python function that sum root to leaf numbers": "def sum_numbers",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)

    # existing general LCA still wins when BST is not mentioned
    src = synthesize_python("write a python function that lowest common ancestor")
    assert "def lowest_common_ancestor(" in src
    assert "def lowest_common_ancestor_bst" not in src


def test_pack30_tree_templates():
    cases = {
        "write a python function that count nodes in a complete binary tree": "def count_nodes",
        "write a python function that cousins in a binary tree": "def is_cousins",
        "write a python function that find largest value in each tree row": "def largest_values",
        "write a python function that maximum level sum of a binary tree": "def max_level_sum",
        "write a python function that insert into a bst": "def insert_into_bst",
        "write a python function that closest value in a bst": "def closest_value",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_pack24_graph_templates():
    cases = {
        "write a python function for the max area of an island": "def max_area_of_island",
        "write a python function for keys and rooms": "def can_visit_all_rooms",
        "write a python function that opens the lock": "def open_lock",
        "write a python function for the shortest bridge": "def shortest_bridge",
        "write a python function that checks if a graph is bipartite": "def is_bipartite",
        "write a python function that finds the celebrity": "def find_celebrity",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p37_69_equiv_odds_xor_unique_truck():
    cases = {
        "write a python function that maximum 69 number": "def maximum_69_number",
        "write a python function that check if two string arrays are equivalent": "def array_strings_are_equal",
        "write a python function that count odd numbers in an interval": "def count_odds",
        "write a python function that decode xor encoded array": "def decode_xored_array",
        "write a python function that sum of unique elements": "def sum_of_unique",
        "write a python function that maximum units on a truck": "def max_units_on_truck",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p42_similar_squares_ascending_dest_split_bomb():
    cases = {
        "write a python function that count pairs of similar strings": "def count_pairs_of_similar_strings",
        "write a python function that sum of squares of special elements": "def sum_of_squares_of_special",
        "write a python function that maximum ascending subarray sum": "def max_ascending_subarray",
        "write a python function that count largest group": "def count_largest_group",
        "write a python function that split a string in balanced strings": "def balanced_string_split",
        "write a python function that defuse the bomb": "def defuse_the_bomb",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p43_arrival_achievable_people_indices_digit_twice():
    cases = {
        "write a python function that calculate delayed arrival time": "def delayed_arrival_time",
        "write a python function that find the maximum achievable number": "def max_achievable_number",
        "write a python function that sort the people": "def sort_the_people",
        "write a python function that find target indices after sorting": "def target_indices_after_sorting",
        "write a python function that difference between element sum and digit sum": "def difference_element_digit_sum",
        "write a python function that first letter to appear twice": "def first_letter_twice",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p44_date_oddstring_special_weekday_line_nrepeated():
    cases = {
        "write a python function that reformat date": "def reformat_date",
        "write a python function that generate a string with characters that have odd counts": "def generate_the_string",
        "write a python function that find special integer": "def find_special_integer",
        "write a python function that day of the week": "def day_of_the_week",
        "write a python function that check if it is a straight line": "def check_straight_line",
        "write a python function that n-repeated element in size 2n array": "def n_repeated_element",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p45_even_digits_restore_halves_bottles_sep_salary():
    cases = {
        "write a python function that numbers with even digits": "def numbers_with_even_digits",
        "write a python function that restore string": "def restore_string",
        "write a python function that determine if string halves are alike": "def halves_are_alike",
        "write a python function that water bottles": "def num_water_bottles",
        "write a python function that thousand separator": "def thousand_separator",
        "write a python function that average salary excluding the minimum and maximum": "def average_salary_excluding",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p46_seniors_multiples_temp_pairs_letter_employees():
    cases = {
        "write a python function that number of senior citizens": "def count_seniors",
        "write a python function that sum of multiples": "def sum_of_multiples",
        "write a python function that convert the temperature": "def convert_temperature",
        "write a python function that divide array into equal pairs": "def divide_array_equal_pairs",
        "write a python function that percentage of letter in string": "def percentage_of_letter",
        "write a python function that number of employees who met the target": "def number_of_employees_who_met_target",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p47_palnum_reshape_mono_double_rank_diag():
    cases = {
        "write a python function that palindrome number": "def palindrome_number",
        "write a python function that shift 2d grid": "def shift_grid",
        "write a python function that monotonic array": "def monotonic_array",
        "write a python function that cells with odd values": "def odd_cells",
        "write a python function that rank transform of an array": "def rank_transform",
        "write a python function that matrix diagonal sum": "def matrix_diagonal_sum",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p49_xor_lucky_three_kdiff_seat_tickets():
    cases = {
        "write a python function that sum of all subset xor totals": "def subset_xor_sum",
        "write a python function that sum of digits of string after convert": "def get_lucky",
        "write a python function that three divisors": "def is_three",
        "write a python function that count pairs with absolute difference k": "def count_k_difference",
        "write a python function that minimum number of moves to seat everyone": "def min_moves_to_seat",
        "write a python function that time needed to buy tickets": "def time_required_to_buy",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p48_ap_path_prices_prefix_crawler_nesting():
    cases = {
        "write a python function that can make arithmetic progression": "def can_make_arithmetic_progression",
        "write a python function that path crossing": "def path_crossing",
        "write a python function that final prices with a special discount": "def final_prices",
        "write a python function that check if a word occurs as a prefix of word in sentence": "def is_prefix_of_word",
        "write a python function that crawler log folder": "def crawler_log_folder",
        "write a python function that maximum nesting depth of the parentheses": "def max_nesting_depth",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p53_choco_typewriter_merge_minmax_pillow_excel():
    cases = {
        "write a python function that buy two chocolates": "def buy_choco",
        "write a python function that minimum time to type word using special typewriter": "def min_time_to_type",
        "write a python function that merge similar items": "def merge_similar_items",
        "write a python function that min max game": "def min_max_game",
        "write a python function that pass the pillow": "def pass_the_pillow",
        "write a python function that cells in a range on an excel sheet": "def cells_in_range",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p51_odd_ops_final_prefixes_digits_separate():
    cases = {
        "write a python function that largest odd number in string": "def largest_odd_number",
        "write a python function that count operations to obtain zero": "def count_operations",
        "write a python function that keep multiplying found values by two": "def find_final_value",
        "write a python function that count prefixes of a given string": "def count_prefixes",
        "write a python function that count the digits that divide a number": "def count_digits",
        "write a python function that separate the digits in an array": "def separate_digits",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p52_date_keys_symmetric_patterns_pivot_ascending():
    cases = {
        "write a python function that convert date to binary": "def convert_date_to_binary",
        "write a python function that number of changing keys": "def count_changing_keys",
        "write a python function that count symmetric integers": "def count_symmetric_integers",
        "write a python function that number of strings that appear as substrings": "def num_of_strings",
        "write a python function that find the pivot integer": "def pivot_integer",
        "write a python function that check if numbers are ascending in a sentence": "def are_numbers_ascending",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p54_common_product_even_local_occ_69():
    cases = {
        "write a python function that count common words with one occurrence": "def count_common_words",
        "write a python function that subtract the product and sum of digits": "def subtract_product_and_sum",
        "write a python function that most frequent even element": "def most_frequent_even",
        "write a python function that largest local values in a matrix": "def largest_local",
        "write a python function that check if all characters have equal number of occurrences": "def are_occurrences_equal",
        "write a python function that maximum 69 number": "def maximum_69_number",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p55_ops_decrypt_odd_binary_kor_neither_closest():
    cases = {
        "write a python function that minimum operations to make the array increasing": "def min_operations_increasing",
        "write a python function that decrypt string from alphabet to integer mapping": "def freq_alphabets",
        "write a python function that maximum odd binary number": "def maximum_odd_binary_number",
        "write a python function that find the k-or of an array": "def find_k_or",
        "write a python function that neither minimum nor maximum": "def neither_minimum_nor_maximum",
        "write a python function that find closest number to zero": "def find_closest_number",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p56_factors_diff_freq_peaks_xmatrix_board():
    cases = {
        "write a python function that number of common factors": "def common_factors",
        "write a python function that find the distinct difference array": "def distinct_difference_array",
        "write a python function that count elements with maximum frequency": "def max_frequency_elements",
        "write a python function that find the peaks": "def find_peaks",
        "write a python function that check if matrix is x-matrix": "def check_x_matrix",
        "write a python function that distinct numbers on board": "def distinct_integers_on_board",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p57_equiv_score_perm_div3_sneaky_digitsum():
    cases = {
        "write a python function that check if two string arrays are equivalent": "def array_strings_are_equal",
        "write a python function that score of a string": "def score_of_string",
        "write a python function that permutation difference between two strings": "def permutation_difference",
        "write a python function that minimum operations to make all elements divisible by three": "def minimum_operations_divisible_by_three",
        "write a python function that the two sneaky numbers of digitville": "def get_sneaky_numbers",
        "write a python function that minimum element after replacement with digit sum": "def min_element_after_digit_sum",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p58_min_game_digits_pairs_chess_champion_day():
    cases = {
        "write a python function that alice bob minimum number game": "def minimum_number_game",
        "write a python function that separate the digits in an array": "def separate_digits_in_array",
        "write a python function that number of beautiful pairs": "def beautiful_pairs",
        "write a python function that check if two chessboard squares have the same color": "def same_color_chessboard",
        "write a python function that find the champion": "def find_champion",
        "write a python function that count pairs that form a complete day": "def count_complete_day_pairs",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p59_path_devices_xor_bits_conc_acronym():
    cases = {
        "write a python function that find if path exists in graph": "def valid_path",
        "write a python function that split with minimum sum": "def split_num",
        "write a python function that maximum strong pair xor i": "def maximum_strong_pair_xor",
        "write a python function that number of even and odd bits": "def even_odd_bit",
        "write a python function that find the array concatenation value": "def find_the_array_conc_val",
        "write a python function that check if a string is an acronym of words": "def is_acronym",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)

def test_p62_separator_odd_distances_cars_time_width():
    cases = {
        "write a python function that split words by separator": "def split_words_by_separator",
        "write a python function that odd string difference": "def odd_string_difference",
        "write a python function that check distances between same letters": "def check_distances",
        "write a python function that points that intersect with cars": "def number_of_points",
        "write a python function that minimum number of operations to convert time": "def convert_time",
        "write a python function that find the width of columns of a grid": "def find_column_width",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p63_max_k_delete_keys_xmatrix_neg_subarrays():
    cases = {
        "write a python function largest positive integer that exists with its negative leetcode 2441": "def find_max_k",
        "write a python function that delete greatest value in each row": "def delete_greatest_value",
        "write a python function that number of changing keys": "def count_changing_keys",
        "write a python function check if matrix is x matrix leetcode 2319": "def check_x_matrix",
        "write a python function count negative numbers in a sorted matrix": "def count_negatives",
        "write a python function find subarrays with equal sum leetcode 2395": "def find_subarrays",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p64_triangle_harshad_clear_final_pairs_bowling():
    cases = {
        "write a python function type of triangle leetcode 3024": "def type_of_triangle",
        "write a python function harshad number leetcode 3099": "def sum_of_the_digits_of_harshad_number",
        "write a python function clear digits leetcode 3174": "def clear_digits",
        "write a python function final array state after k multiplication operations leetcode 3264": "def get_final_state",
        "write a python function find maximum number of string pairs leetcode 2744": "def maximum_number_of_string_pairs",
        "write a python function determine the winner of a bowling game leetcode 2660": "def is_winner",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p65_balanced_parity_degree_person_key_digits():
    cases = {
        "write a python function check balanced string leetcode 3340": "def is_balanced_digit_string",
        "write a python function transform array by parity leetcode 3467": "def transform_array_by_parity",
        "write a python function reverse degree of a string leetcode 3498": "def reverse_degree",
        "write a python function find closest person leetcode 3516": "def find_closest_person",
        "write a python function find the key of the numbers leetcode 3270": "def generate_key",
        "write a python function check if digits are equal in string after operations leetcode 3461": "def has_same_digits",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p66_alice_snake_chips_encrypt_purchase_leftright():
    cases = {
        "write a python function find if digit game can be won leetcode 3232": "def can_alice_win",
        "write a python function snake in matrix leetcode 3248": "def final_position_of_snake",
        "write a python function minimum number of chips to move leetcode 1217": "def min_cost_to_move_chips",
        "write a python function find the encrypted string leetcode 3210": "def get_encrypted_string",
        "write a python function account balance after purchase leetcode 2806": "def account_balance_after_purchase",
        "write a python function left and right sum differences leetcode 2574": "def left_right_difference",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p71_distance_divisor_trib_overlap_pressed_stone():
    cases = {
        "write a python function find the distance value between two arrays leetcode 1385": "def find_the_distance_value",
        "write a python function divisor game leetcode 1025": "def divisor_game",
        "write a python function nth tribonacci number leetcode 1137": "def tribonacci",
        "write a python function binary prefix divisible by 5 leetcode 1018": "def prefixes_div_by_5",
        "write a python function long pressed name leetcode 925": "def is_long_pressed_name",
        "write a python function last stone weight leetcode 1046": "def last_stone_weight",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p70_peaks_boxes_ant_intersect_stable_special():
    cases = {
        "write a python function find the number of winning players leetcode 3238": "def winning_player_count",
        "write a python function apple redistribution into boxes leetcode 3074": "def minimum_boxes",
        "write a python function ant on the boundary leetcode 3028": "def return_to_boundary_count",
        "write a python function find common elements between two arrays leetcode 2956": "def find_intersection_values",
        "write a python function find indices of stable mountains leetcode 3285": "def stable_mountains",
        "write a python function count the number of special characters leetcode 3120": "def number_of_special_chars",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p69_key_missing_digits_concat_encrypt_freq():
    cases = {
        "write a python function find the key of the numbers leetcode 3270": "def generate_key",
        "write a python function find missing and repeated values leetcode 2965": "def find_missing_and_repeated_values",
        "write a python function count the digits that divide the number leetcode 2520": "def count_digits",
        "write a python function find the array concatenation value leetcode 2562": "def find_the_array_conc_val",
        "write a python function sum of encrypted integers leetcode 3079": "def sum_of_encrypted_int",
        "write a python function count elements with maximum frequency leetcode 3005": "def max_frequency_elements",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p68_count_conflict_flips_diff_hills_goodint():
    cases = {
        "write a python function maximum count of positive integer and negative integer leetcode 2529": "def maximum_count",
        "write a python function determine if two events have conflict leetcode 2446": "def have_conflict",
        "write a python function minimum bit flips to convert number leetcode 2220": "def min_bit_flips",
        "write a python function find the difference of two arrays leetcode 2215": "def find_difference",
        "write a python function count hills and valleys in an array leetcode 2210": "def count_hill_valley",
        "write a python function largest 3-same-digit number in string leetcode 2264": "def largest_good_integer",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p67_days_fourdigit_pivot_pairs_div_odd():

    cases = {
        "write a python function count days spent together leetcode 2409": "def count_days_together",
        "write a python function minimum sum of four digit number leetcode 2160": "def minimum_sum_four_digit",
        "write a python function find the pivot integer leetcode 2485": "def find_the_pivot_integer",
        "write a python function minimum average of smallest and largest elements leetcode 3194": "def find_minimum_average",
        "write a python function divisible and non divisible sums difference leetcode 2894": "def divisible_and_non_divisible",
        "write a python function maximum odd binary number leetcode 2864": "def maximum_odd_binary",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p73_record_letter_dominant_bigram_baseball_mismatch():
    cases = {
        "write a python function student attendance record i leetcode 551": "def check_record",
        "write a python function find smallest letter greater than target leetcode 744": "def next_greatest_letter",
        "write a python function largest number at least twice of others leetcode 747": "def dominant_index",
        "write a python function occurrences after bigram leetcode 1078": "def find_ocurrences",
        "write a python function baseball game leetcode 682": "def cal_points",
        "write a python function set mismatch leetcode 645": "def find_error_nums",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p74_perfect_build_concat_ops_reversal_chairs():
    cases = {
        "write a python function perfect number leetcode 507": "def check_perfect_number",
        "write a python function build array from permutation leetcode 1920": "def build_array",
        "write a python function find the integer added to array i leetcode 3131": "def added_integer",
        "write a python function final value of variable after performing operations leetcode 2011": "def final_value_after_operations",
        "write a python function a number after a double reversal leetcode 2119": "def is_same_after_reversals",
        "write a python function minimum number of chairs in a waiting room leetcode 3168": "def minimum_chairs",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p75_equal_index_min_string_pairs_intersect_good_balance():
    cases = {
        "write a python function smallest index with equal value leetcode 2057": "def smallest_equal",
        "write a python function minimize string length leetcode 2716": "def minimized_string_length",
        "write a python function count equal and divisible pairs in an array leetcode 2176": "def count_equal_divisible_pairs",
        "write a python function intersection of multiple arrays leetcode 2248": "def intersection_multiple_arrays",
        "write a python function largest 3-same-digit number in string leetcode 2264": "def largest_good_integer",
        "write a python function account balance after rounded purchase leetcode 2806": "def account_balance_after_purchase",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p76_circular_ops_prefix_threshold_div3_twice_xor():
    cases = {
        "write a python function circular sentence leetcode 2490": "def is_circular_sentence",
        "write a python function apply operations to an array leetcode 2460": "def apply_operations",
        "write a python function find the prefix common array of two arrays leetcode 2657": "def find_the_prefix_common_array",
        "write a python function minimum operations to exceed threshold value i leetcode 3065": "def min_operations",
        "write a python function minimum number of operations to make all array elements divisible by three leetcode 3190": "def minimum_operations",
        "write a python function xor of numbers which appear twice leetcode 3158": "def duplicate_numbers_xor",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p77_rings_bits_grid_kth_triples_coin():
    cases = {
        "write a python function rings and rods leetcode 2103": "def count_points",
        "write a python function smallest number with all bits set leetcode 3370": "def smallest_number",
        "write a python function check if grid satisfies conditions leetcode 3142": "def satisfies_conditions",
        "write a python function find the k-th character in string game i leetcode 3304": "def kth_character",
        "write a python function count subarrays of length three with a condition leetcode 3392": "def count_subarrays",
        "write a python function find the winning player in coin game leetcode 3222": "def losing_player",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p78_decibinary_bank_start_middle_distinct_ones():
    cases = {
        "write a python function partitioning into minimum number of deci-binary numbers leetcode 1689": "def min_partitions",
        "write a python function calculate money in leetcode bank leetcode 1716": "def total_money",
        "write a python function minimum value to get positive step by step sum leetcode 1413": "def min_start_value",
        "write a python function find the middle index in array leetcode 1991": "def find_middle_index",
        "write a python function substrings of size three with distinct characters leetcode 1876": "def count_good_substrings",
        "write a python function check if binary string has at most one segment of ones leetcode 1784": "def check_ones_segment",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p79_chess_balls_base_push_runs_wordsum():
    cases = {
        "write a python function determine color of a chessboard square leetcode 1812": "def square_is_white",
        "write a python function maximum number of balls in a box leetcode 1742": "def count_balls",
        "write a python function sum of digits in base k leetcode 1837": "def sum_base",
        "write a python function button with longest push time leetcode 3386": "def button_with_longest_time",
        "write a python function longer contiguous segments of ones than zeros leetcode 1869": "def check_zero_ones",
        "write a python function check if word equals summation of two words leetcode 1880": "def is_sum_equal",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p80_boundary_candies_diagonal_circular_good_ship():
    cases = {
        "write a python function ant on the boundary leetcode 3028": "def return_to_boundary_count",
        "write a python function distribute candies among children leetcode 2928": "def distribute_candies",
        "write a python function maximum area of longest diagonal rectangle leetcode 3000": "def area_of_max_diagonal",
        "write a python function maximum difference between adjacent elements in a circular array leetcode 3423": "def max_adjacent_distance",
        "write a python function sum of good numbers leetcode 3452": "def sum_of_good_numbers",
        "write a python function maximum containers on a ship leetcode 3492": "def max_containers",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)

def test_p81_freq_typed_varsum_setbits_ball_triples():
    cases = {
        "write a python function maximum difference between even and odd frequency i leetcode 3442": "def max_freq_odd_even_diff",
        "write a python function find the original typed string i leetcode 3330": "def possible_string_count",
        "write a python function sum of variable length subarrays leetcode 3427": "def variable_length_subarray_sum",
        "write a python function smallest number with all set bits leetcode 3370": "def smallest_number_all_set_bits",
        "write a python function find the child who has the ball after k seconds leetcode 3178": "def child_with_ball",
        "write a python function count square sum triples leetcode 1925": "def count_square_sum_triples",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p82_string_value_swap_or_indices_distinct_monotonic():
    cases = {
        "write a python function maximum value of a string in an array leetcode 2496": "def maximum_value",
        "write a python function lexicographically smallest string after a swap leetcode 3216": "def get_smallest_string",
        "write a python function check if bitwise or has trailing zeros leetcode 2980": "def has_trailing_zeros",
        "write a python function find indices with index and value difference i leetcode 2903": "def find_indices",
        "write a python function subarrays distinct element sum of squares i leetcode 2913": "def sum_counts",
        "write a python function longest monotonic subarray leetcode 3105": "def longest_monotonic_subarray",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)



def test_p83_chessboards_diff_collect_box_digits_kdistant():
    cases = {
        "write a python function check if two chessboards have the same color leetcode 3274": "def check_two_chessboards",
        "write a python function maximum difference between increasing elements leetcode 2016": "def maximum_difference",
        "write a python function minimum operations to collect elements leetcode 2869": "def min_operations",
        "write a python function categorize box according to criteria leetcode 2525": "def categorize_box",
        "write a python function check if number has equal digit count and digit value leetcode 2283": "def digit_count",
        "write a python function find all k-distant indices in an array leetcode 2200": "def find_k_distant_indices",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p85_beams_append_password_people_digit_units():
    cases = {
        "write a python function number of laser beams in a bank leetcode 2125": "def number_of_beams",
        "write a python function append characters to string to make subsequence leetcode 2486": "def append_characters",
        "write a python function strong password checker ii leetcode 2299": "def strong_password_checker_ii",
        "write a python function remove digit from number to maximize result leetcode 2259": "def remove_digit",
        "write a python function adding spaces to a string leetcode 2109": "def add_spaces",
        "write a python function maximum ice cream bars leetcode 1833": "def max_ice_cream",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p86_adjacent_great_spaces_gap_digit_prefix():
    cases = {
        "write a python function remove all adjacent duplicates in string leetcode 1047": "def remove_all_adjacent_duplicates",
        "write a python function make the string great leetcode 1544": "def make_good",
        "write a python function rearrange spaces between words leetcode 1592": "def reorder_spaces",
        "write a python function largest substring between two equal characters leetcode 1624": "def max_length_between_equal_characters",
        "write a python function second largest digit in a string leetcode 1796": "def second_highest",
        "write a python function check if string is a prefix of array leetcode 1961": "def is_prefix_string",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)

def test_p87_vowel_range_matrix_pairs_groups_digits_freq():
    cases = {
        "write a python function count the number of vowel strings in range leetcode 2586": "def vowel_strings_in_range",
        "write a python function modify the matrix leetcode 3033": "def modified_matrix",
        "write a python function find the number of good pairs i leetcode 3162": "def number_of_good_pairs_i",
        "write a python function alternating groups i leetcode 3206": "def alternating_groups_i",
        "write a python function maximum product of two digits leetcode 3536": "def max_product_two_digits",
        "write a python function find most frequent vowel and consonant leetcode 3541": "def most_frequent_vowel_consonant",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p88_faulty_keys_harshad_div3_snake_balanced():
    cases = {
        "write a python function faulty keyboard leetcode 2810": "def faulty_keyboard",
        "write a python function number of changing keys leetcode 3019": "def number_of_changing_keys",
        "write a python function minimum sum of mountain triplets i leetcode 2908": "def minimum_sum_mountain_triplets",
        "write a python function unique three digit even numbers leetcode 3483": "def unique_three_digit_even",
        "write a python function snake in matrix leetcode 3248": "def snake_in_matrix",
        "write a python function check balanced string leetcode 3340": "def check_balanced_string",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)



def test_p89_adjacent_prime_ops_div_trionic_order():
    cases = {
        "write a python function resulting string after adjacent removals leetcode 3561": "def resulting_string_after_adjacent_removals",
        "write a python function check if any element has prime frequency leetcode 3591": "def has_prime_frequency",
        "write a python function process string with special operations i leetcode 3612": "def process_string_special_operations",
        "write a python function check divisibility by digit sum and product leetcode 3622": "def check_divisibility_digit_sum_product",
        "write a python function trionic array i leetcode 3637": "def is_trionic",
        "write a python function restore finishing order leetcode 3668": "def restore_finishing_order",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p90_equalize_finish_decimal_score_freq_multiple():
    cases = {
        "write a python function minimum operations to equalize array leetcode 3674": "def min_operations_equalize_array",
        "write a python function earliest time to finish one task leetcode 3683": "def earliest_time_to_finish_one_task",
        "write a python function compute decimal representation leetcode 3697": "def decimal_representation",
        "write a python function equal score substrings leetcode 3707": "def equal_score_substrings",
        "write a python function sum of elements with frequency divisible by k leetcode 3712": "def sum_freq_divisible_by_k",
        "write a python function smallest missing multiple leetcode 3718": "def missing_multiple",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)

def test_p91_zeros_missing_moves_flips_removals_kdiff():
    cases = {
        "write a python function remove zeros in decimal representation leetcode 3726": "def remove_zeros_decimal",
        "write a python function find missing elements leetcode 3731": "def find_missing_elements",
        "write a python function minimum moves to equal array elements iii leetcode 3736": "def min_moves_equal_array_iii",
        "write a python function minimum flips to reverse binary string leetcode 3750": "def min_flips_reverse_binary",
        "write a python function minimum string length after balanced removals leetcode 3746": "def min_length_balanced_removals",
        "write a python function absolute difference between maximum and minimum k elements leetcode 3774": "def abs_diff_k_extremes",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)




def test_p92_digit_nice_rotated_swap_population_freq():
    cases = {
        "write a python function second largest digit in a string leetcode 1796": "def second_largest_digit",
        "write a python function longest nice substring leetcode 1763": "def longest_nice_substring",
        "write a python function check if array is sorted and rotated leetcode 1752": "def check_sorted_rotated",
        "write a python function check if one string swap can make strings equal leetcode 1790": "def one_string_swap",
        "write a python function maximum population year leetcode 1854": "def maximum_population_year",
        "write a python function minimum changes to make alternating binary string leetcode 1758": "def min_changes_alternating",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    both = synthesize_python("write a python function second largest digit in a string leetcode 1796")
    assert "def second_largest_digit" in both
    assert "def second_highest" in both


def test_p93_integers_distance_equal_typed_fancy_moves():
    cases = {
        "write a python function number of different integers in a string leetcode 1805": "def num_different_integers",
        "write a python function minimum distance to the target element leetcode 1848": "def min_distance_target",
        "write a python function redistribute characters to make all strings equal leetcode 1897": "def make_equal_strings",
        "write a python function maximum number of words you can type leetcode 1935": "def can_be_typed_words",
        "write a python function delete characters to make fancy string leetcode 1957": "def make_fancy_string",
        "write a python function minimum moves to convert string leetcode 2027": "def minimum_moves_convert_string",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p94_houses_candies_ops_beauty_letter_cups():
    cases = {
        "write a python function two furthest houses with different colors leetcode 2078": "def max_distance_colors",
        "write a python function minimum cost of buying candies with a discount leetcode 2144": "def minimum_cost_candies",
        "write a python function count operations to obtain zero leetcode 2169": "def count_operations_zero",
        "write a python function find the k beauty of a number leetcode 2269": "def k_beauty",
        "write a python function greatest english letter in upper and lower case leetcode 2309": "def greatest_letter",
        "write a python function minimum amount of time to fill cups leetcode 2335": "def fill_cups",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p95_zero_recolors_limited_freq_worker_clocks():
    cases = {
        "write a python function make array zero by subtracting equal amounts leetcode 2357": "def minimum_operations_array_zero",
        "write a python function minimum recolors to get k consecutive black blocks leetcode 2379": "def minimum_recolors",
        "write a python function longest subsequence with limited sum leetcode 2389": "def answer_queries_limited_sum",
        "write a python function remove letter to equalize frequency leetcode 2423": "def equal_frequency",
        "write a python function employee that worked on the longest task leetcode 2432": "def hardest_worker",
        "write a python function number of valid clock times leetcode 2437": "def count_valid_clock_times",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p96_reverse_avg_triplets_cuts_digits_time():
    cases = {
        "write a python function count number of distinct integers after reverse operations leetcode 2442": "def count_distinct_integers_reverse",
        "write a python function number of distinct averages leetcode 2465": "def distinct_averages",
        "write a python function number of unequal triplets in array leetcode 2475": "def unequal_triplets",
        "write a python function minimum cuts to divide a circle leetcode 2481": "def minimum_cuts_circle",
        "write a python function calculate digit sum of a string leetcode 2243": "def digit_sum_string",
        "write a python function latest time by replacing hidden digits leetcode 1736": "def latest_time_hidden",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p97_origin_common_missing_special_day_average():
    cases = {
        "write a python function furthest point from origin leetcode 2833": "def furthest_point_from_origin",
        "write a python function find common elements between two arrays leetcode 2956": "def common_elements_two_arrays",
        "write a python function convert date to binary leetcode 3280": "def date_to_binary",
        "write a python function special array i leetcode 3151": "def special_array_i",
        "write a python function count pairs that form a complete day leetcode 3184": "def count_complete_day_pairs",
        "write a python function minimum average of smallest and largest elements leetcode 3194": "def minimum_average",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p98_two_strict_reverse_nearest_evenodd_diag():
    cases = {
        "write a python function two out of three leetcode 2032": "def two_out_of_three",
        "write a python function count elements with strictly smaller and greater leetcode 2148": "def count_elements_strict",
        "write a python function make two arrays equal by reversing subarrays leetcode 1460": "def can_be_equal_reverse",
        "write a python function find nearest point that has the same x or y leetcode 1779": "def nearest_valid_point",
        "write a python function longest even odd subarray with threshold leetcode 2760": "def longest_even_odd_subarray",
        "write a python function prime in diagonal leetcode 2614": "def diagonal_prime",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)


def test_p99_knight_alternating_div_good_semi_substr():
    cases = {
        "write a python function check knight tour configuration leetcode 2596": "def check_knight_tour_configuration",
        "write a python function longest alternating subarray leetcode 2765": "def longest_alternating_subarray",
        "write a python function find the maximum divisibility score leetcode 2644": "def maximum_divisibility_score",
        "write a python function check if array is good leetcode 2784": "def check_array_is_good",
        "write a python function semi-ordered permutation leetcode 2717": "def semi_ordered_permutation",
        "write a python function existence of a substring in a string and its reverse leetcode 3083": "def existence_of_substring_reverse",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def permute" in synthesize_python("write a python function that returns all permutations")
    assert "def reverse_string" in synthesize_python("implement a python function to reverse a string")


def test_p100_split_twoocc_valid_cost_distinct_equal_k():
    cases = {
        "write a python function split the array leetcode 3046": "def is_possible_to_split",
        "write a python function maximum length substring with two occurrences leetcode 3090": "def maximum_length_substring_two_occurrences",
        "write a python function valid word leetcode 3136": "def is_valid_word",
        "write a python function minimum cost to reach every position leetcode 3502": "def min_cost_to_reach_position",
        "write a python function count substrings of length three with all distinct leetcode 3258": "def count_distinct_length_three",
        "write a python function minimum operations to make array values equal to k leetcode 3375": "def min_operations_equal_k",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def permute" in synthesize_python("write a python function that returns all permutations")
    assert "def reverse_string" in synthesize_python("implement a python function to reverse a string")


def test_p101_special_ii_almost_reformat_prefix_beautiful_equal_one():
    cases = {
        "write a python function count the number of special characters ii leetcode 3121": "def number_of_special_chars_ii",
        "write a python function check whether two strings are almost equivalent leetcode 2068": "def check_almost_equivalent",
        "write a python function reformat the string leetcode 1417": "def reformat_string",
        "write a python function find the original array of prefix xor leetcode 2433": "def find_array_prefix_xor",
        "write a python function minimum number of changes to make binary string beautiful leetcode 2914": "def min_changes_beautiful",
        "write a python function minimum operations to make binary array elements equal to one i leetcode 3191": "def min_operations_equal_one",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def number_of_special_chars" in synthesize_python(
        "write a python function count the number of special characters i leetcode 3120"
    )
    assert "def min_changes_alternating" in synthesize_python(
        "write a python function minimum changes to make alternating binary string leetcode 1758"
    )
    assert "def decode_xored_array" in synthesize_python(
        "write a python function decode xored array leetcode 1720"
    )


def test_p102_sum_divisible_neighbor_xor_min_end_swaps_len_sort():
    cases = {
        "write a python function minimum operations to make array sum divisible by k leetcode 3512": "def min_operations_sum_divisible_by_k",
        "write a python function neighboring bitwise xor leetcode 2683": "def does_valid_array_exist",
        "write a python function minimum array end leetcode 3133": "def min_array_end",
        "write a python function minimum number of swaps to make the string balanced leetcode 1963": "def min_swaps_balanced",
        "write a python function minimum length of string after operations leetcode 3223": "def minimum_length_after_ops",
        "write a python function find if array can be sorted leetcode 3011": "def can_sort_array",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def sum_list" in synthesize_python("write a python function that sums a list of numbers")
    assert "def min_operations_equal_one" in synthesize_python(
        "write a python function minimum operations to make binary array elements equal to one i leetcode 3191"
    )


def test_p103_circular_similar_ends_fish_lunch_parens_teemo():
    cases = {
        "write a python function shortest distance to target string in a circular array leetcode 2515": "def circular_target_distance",
        "write a python function minimum length of string after deleting similar ends leetcode 1750": "def min_length_similar_ends",
        "write a python function maximum number of fish in a grid leetcode 2658": "def find_max_fish",
        "write a python function number of students unable to eat lunch leetcode 1700": "def count_students_lunch",
        "write a python function minimum add to make parentheses valid leetcode 921": "def min_add_parentheses",
        "write a python function teemo attacking leetcode 495": "def teemo_attacking",
        "write a python function shortest distance to a character leetcode 821": "def shortest_to_char",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def minimum_length_after_ops" in synthesize_python(
        "write a python function minimum length of string after operations leetcode 3223"
    )


def test_p104_lines_groups_letters_balloons_slowest_replace():
    cases = {
        "write a python function that number of lines to write": "def number_of_lines",
        "write a python function that large group positions": "def large_group_positions",
        "write a python function reverse only letters leetcode 917": "def reverse_only_letters",
        "write a python function maximum number of balloons leetcode 1189": "def max_number_of_balloons",
        "write a python function slowest key leetcode 1629": "def slowest_key",
        "write a python function replace elements with greatest element on right side leetcode 1299": "def replace_elements_right",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def reverse_string" in synthesize_python(
        "implement a python function to reverse a string"
    )


def test_p105_reshape_integers_pairs_average_ksum_digits_score():
    cases = {
        "write a python function convert 1d array into 2d array leetcode 2022": "def construct_2d_array",
        "write a python function add two integers leetcode 2235": "def add_two_integers",
        "write a python function maximum number of pairs in array leetcode 2341": "def number_of_pairs_in_array",
        "write a python function average value of even numbers that are divisible by three leetcode 2455": "def average_even_divisible_by_three",
        "write a python function k items with the maximum sum leetcode 2600": "def k_items_with_maximum_sum",
        "write a python function smallest number from two digit arrays leetcode 2605": "def min_number_from_two_digit_arrays",
        "write a python function maximum number of operations with the same score i leetcode 3038": "def max_operations_same_score",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "return a + b" in synthesize_python("write a python function that adds two numbers")
    assert "def average" in synthesize_python("write a python function that averages two numbers")


def test_p106_gcd_array_kscores_evenodd_anagrams_rearrange_pushes():
    cases = {
        "write a python function greatest common divisor of an array leetcode 1979": "def find_gcd_array",
        "write a python function minimum difference between highest and lowest of k scores leetcode 1984": "def min_diff_k_scores",
        "write a python function sort even and odd indices independently leetcode 2164": "def sort_even_odd_indices",
        "write a python function resultant array after removing anagrams leetcode 2273": "def remove_anagrams",
        "write a python function rearrange characters to make target string leetcode 2287": "def rearrange_characters",
        "write a python function minimum number of pushes to type word i leetcode 3014": "def minimum_pushes",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def gcd" in synthesize_python("write a python function that returns the greatest common divisor")
    assert "def sort_list" in synthesize_python("write a python function that sorts a list")
    assert "def is_anagram" in synthesize_python("write a python function that checks if two strings are anagrams")


def test_p107_partitions_pair_fruits_removal_index_second_largest():
    cases = {
        "write a python function partitions with even sum difference leetcode 3432": "def count_partitions_even_sum_diff",
        "write a python function valid pair of adjacent digits leetcode 3438": "def find_valid_pair",
        "write a python function fruits into baskets ii leetcode 3477": "def num_of_unplaced_fruits",
        "write a python function minimum pair removal to sort leetcode 3507": "def minimum_pair_removal",
        "write a python function smallest index with digit sum equal to index leetcode 3550": "def smallest_index_digit_sum",
        "write a python function that returns the second largest number in a list": "def second_largest",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    digit = synthesize_python(
        "write a python function second largest digit in a string leetcode 1796"
    )
    assert "def second_largest_digit" in digit
    assert "def second_largest(" not in digit


def test_p108_square_digit_product_stones_distinct_columns_zigzag():
    cases = {
        "write a python function make a square with the same color leetcode 3127": "def can_make_square",
        "write a python function smallest divisible digit product i leetcode 3345": "def smallest_divisible_digit_product",
        "write a python function stone removal game leetcode 3360": "def stone_removal_game",
        "write a python function minimum operations to make elements distinct leetcode 3396": "def minimum_operations_distinct",
        "write a python function minimum operations to make columns strictly increasing leetcode 3402": "def minimum_operations_columns",
        "write a python function zigzag grid traversal with skip leetcode 3417": "def zigzag_traversal",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def can_jump" in synthesize_python("write a python function for the jump game")
    assert "def minimum_operations" not in synthesize_python("write a python function that moves zeroes to the end")


def test_p109_unique_logs_hex_rides_gcd_digit():
    cases = {
        "write a python function maximum unique subarray sum after deletion leetcode 3487": "def max_unique_subarray_sum",
        "write a python function minimum log transportation cost leetcode 3560": "def min_log_transport_cost",
        "write a python function hexadecimal and hexatrigesimal conversion leetcode 3602": "def concat_hex36",
        "write a python function earliest finish time for land and water rides leetcode 3633": "def earliest_finish_rides",
        "write a python function gcd of odd and even sums leetcode 3658": "def gcd_odd_even_sums",
        "write a python function find the least frequent digit leetcode 3663": "def least_frequent_digit",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def max_sub_array" in synthesize_python("write a python function maximum subarray kadane") or "def max" in synthesize_python("write a python function maximum subarray")
    assert "def least_frequent_digit" not in synthesize_python("write a python function that counts the digits of a number")


def test_p110_absent_kdistinct_majority_altsum_coupon_replacements():
    cases = {
        "write a python function smallest absent positive greater than average leetcode 3678": "def smallest_absent_above_average",
        "write a python function maximize sum of at most k distinct elements leetcode 3684": "def max_sum_k_distinct",
        "write a python function majority frequency characters leetcode 3692": "def majority_frequency_characters",
        "write a python function compute alternating sum leetcode 3701": "def alternating_sum",
        "write a python function coupon code validator leetcode 3606": "def validate_coupons",
        "write a python function number of student replacements leetcode 3616": "def student_replacements",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def has_alternating_bits" in synthesize_python(
        "write a python function that checks alternating bits"
    )
    assert "def missing_multiple" in synthesize_python(
        "write a python function smallest missing multiple of k leetcode 3718"
    )
    assert "def alternating_sum" not in synthesize_python(
        "write a python function alternating digit sum leetcode 2544"
    )


def test_p111_mirror_prefix_even_residue_score_monobit():
    cases = {
        "write a python function mirror distance of an integer leetcode 3783": "def mirror_distance",
        "write a python function reverse string prefix leetcode 3794": "def reverse_string_prefix",
        "write a python function largest even number leetcode 3798": "def largest_even_number",
        "write a python function count residue prefixes leetcode 3803": "def count_residue_prefixes",
        "write a python function vowel-consonant score leetcode 3813": "def vowel_consonant_score",
        "write a python function count monobit integers leetcode 3827": "def count_monobit",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def reverse_prefix" in synthesize_python(
        "write a python function reverse prefix of word leetcode 2000"
    )
    assert "def count_vowels" in synthesize_python(
        "write a python function that counts vowels"
    )
    assert "def reverse_vowels" in synthesize_python(
        "write a python function that reverses vowels in a string"
    )


def test_p114_special_equiv_logs_mirror_time_even_broken():
    cases = {
        "write a python function groups of special-equivalent strings leetcode 893": "def num_special_equiv_groups",
        "write a python function reorder data in log files leetcode 937": "def reorder_log_files",
        "write a python function mirror reflection leetcode 858": "def mirror_reflection",
        "write a python function largest time for given digits leetcode 949": "def largest_time_from_digits",
        "write a python function sum of even numbers after queries leetcode 985": "def sum_even_after_queries",
        "write a python function broken calculator leetcode 991": "def broken_calc",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def basic_calculator" in synthesize_python(
        "write a python function basic calculator ii"
    ) or "def calculate" in synthesize_python(
        "write a python function basic calculator ii"
    )
    assert "def largest_time_from_digits" not in synthesize_python(
        "write a python function largest number"
    )


def test_p113_rotated_subdomain_closest_transpose_robot_squares():
    cases = {
        "write a python function rotated digits leetcode 788": "def rotated_digits",
        "write a python function subdomain visit count leetcode 811": "def subdomain_visits",
        "write a python function maximize distance to closest person leetcode 849": "def max_dist_to_closest",
        "write a python function transpose matrix leetcode 867": "def transpose",
        "write a python function walking robot simulation leetcode 874": "def robot_sim",
        "write a python function squares of a sorted array leetcode 977": "def sorted_squares",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def search_rotated" in synthesize_python(
        "write a python function search in rotated sorted array"
    ) or "def find_min" in synthesize_python(
        "write a python function find minimum in rotated sorted array"
    )
    assert "def sort_list" in synthesize_python(
        "write a python function that sorts a list"
    )
    assert "def shortest_to_char" in synthesize_python(
        "write a python function shortest distance to a character"
    )



def test_p115_palindrome_sub_sort_string_stack_modify_repeat_strict():
    cases = {
        "write a python function remove palindromic subsequences leetcode 1332": "def remove_palindrome_sub",
        "write a python function increasing decreasing string leetcode 1370": "def increasing_decreasing_string",
        "write a python function build an array with stack operations leetcode 1441": "def build_array_stack",
        "write a python function replace all question marks to avoid consecutive repeating characters leetcode 1576": "def modify_string",
        "write a python function maximum repeating substring leetcode 1668": "def max_repeating",
        "write a python function strictly palindromic number leetcode 2396": "def is_strictly_palindromic",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def is_palindrome" in synthesize_python(
        "write a python function that checks a palindrome"
    ) or "def is_palindrome" in synthesize_python(
        "write a python function is palindrome"
    )
    assert "def min_stack" in synthesize_python(
        "write a python function min stack"
    ) or "class MinStack" in synthesize_python(
        "write a python function min stack"
    )


def test_p116_bit_changes_bitwise_increasing_zero_possum_pattern():
    cases = {
        "write a python function number of bit changes to make two integers equal leetcode 3226": "def bit_changes_to_equal",
        "write a python function construct the minimum bitwise array leetcode 3314": "def min_bitwise_array",
        "write a python function adjacent increasing subarrays detection leetcode 3349": "def has_increasing_subarrays",
        "write a python function make array elements equal to zero leetcode 3354": "def count_valid_selections",
        "write a python function minimum positive sum subarray leetcode 3364": "def minimum_positive_sum",
        "write a python function substring matching pattern leetcode 3407": "def substring_matching_pattern",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def reverse_bits" in synthesize_python(
        "write a python function reverse bits"
    ) or "bin(" in synthesize_python("write a python function reverse bits")


def test_p118_binary_covered_quad_tax_poker_forts():
    cases = {
        "write a python function convert binary number in a linked list to integer leetcode 1290": "def get_decimal_value",
        "write a python function check if all the integers in a range are covered leetcode 1893": "def is_covered",
        "write a python function count special quadruplets leetcode 1995": "def count_quadruplets",
        "write a python function calculate amount paid in taxes leetcode 2303": "def calculate_tax",
        "write a python function best poker hand leetcode 2347": "def best_hand",
        "write a python function maximum enemy forts that can be captured leetcode 2511": "def capture_forts",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    # do not steal four-sum quadruplets or generic binary reverse
    four = synthesize_python("write a python function quadruplets that sum to a target")
    assert "def count_quadruplets" not in four
    assert "def reverse_list" in synthesize_python("write a python function reverse a linked list") or "reverse" in synthesize_python("write a python function reverse a linked list")


def test_p117_days_subseq_visited_special_even_parity():
    cases = {
        "write a python function number of days between two dates leetcode 1360": "def days_between_dates",
        "write a python function minimum subsequence in non-increasing order leetcode 1403": "def min_subsequence",
        "write a python function most visited sector in a circular track leetcode 1560": "def most_visited",
        "write a python function special positions in a binary matrix leetcode 1582": "def num_special",
        "write a python function finding 3-digit even numbers leetcode 2094": "def find_even_numbers",
        "write a python function largest number after digit swaps by parity leetcode 2231": "def largest_integer",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    # do not steal unique-3-digit-even or generic palindrome
    uniq = synthesize_python("write a python function unique 3-digit even numbers")
    assert "def unique_three_digit_even" in uniq or "unique" in uniq
    assert "def find_even_numbers" not in uniq
    assert "def is_palindrome" in synthesize_python("write a python function that checks a palindrome") or "def is_palindrome" in synthesize_python("write a python function is palindrome")


def test_p119_remap_tank_pair_visited_equal_time():
    cases = {
        "write a python function maximum difference by remapping a digit leetcode 2566": "def min_max_difference",
        "write a python function total distance traveled leetcode 2739": "def distance_traveled",
        "write a python function max pair sum in an array leetcode 2815": "def max_pair_sum",
        "write a python function last visited integers leetcode 2899": "def last_visited_integers",
        "write a python function make three strings equal leetcode 2937": "def find_minimum_operations",
        "write a python function latest time you can obtain after replacing characters leetcode 3114": "def find_latest_time",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    # do not steal generic max or add
    assert "def maximum" in synthesize_python("write a python function maximum of two numbers") or "def max" in synthesize_python("write a python function maximum of two numbers")
    assert "def add" in synthesize_python("write a python function that adds two numbers")
    assert "def min_max_difference" not in synthesize_python("write a python function maximum difference between two elements")


def test_p120_ksum_split_cars_grid_encrypt_parity():
    cases = {
        "write a python function maximum sum with exactly k elements leetcode 2656": "def maximize_sum",
        "write a python function split strings by separator leetcode 2788": "def split_words_by_separator",
        "write a python function points that intersect with cars leetcode 2848": "def number_of_points",
        "write a python function find missing and repeated values leetcode 2965": "def find_missing_and_repeated_values",
        "write a python function sum of encrypted integers leetcode 3079": "def sum_of_encrypted_int",
        "write a python function transform array by parity leetcode 3467": "def transform_array",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    # do not steal generic max, split, or sort
    assert "def maximize_sum" not in synthesize_python("write a python function maximum of two numbers")
    assert "def split_words_by_separator" not in synthesize_python("write a python function split a list in half")
    assert "def transform_array" not in synthesize_python("write a python function sort a list")


def test_p121_prefix_distribute_cost_or_balls_special():
    cases = {
        "write a python function count prefix and suffix pairs i leetcode 3042": "def count_prefix_suffix_pairs",
        "write a python function distribute elements into two arrays i leetcode 3069": "def result_array_two",
        "write a python function divide an array into subarrays with minimum cost i leetcode 3010": "def minimum_cost_subarrays",
        "write a python function shortest subarray with or at least k i leetcode 3095": "def minimum_subarray_length_or",
        "write a python function minimum number of operations to move all balls to each box leetcode 1769": "def min_operations_balls",
        "write a python function find the count of numbers which are not special leetcode 3233": "def not_special_count",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def minimum_cost_subarrays" not in synthesize_python("write a python function minimum cost climbing stairs")
    assert "def min_operations_balls" not in synthesize_python("write a python function minimum operations to exceed threshold value i leetcode 3065")
    assert "def not_special_count" not in synthesize_python("write a python function count the number of special characters i leetcode 3120")


def test_p122_spam_xsum_screen_missing_equal_flip():
    cases = {
        "write a python function report spam message leetcode 3295": "def report_spam",
        "write a python function find x-sum of all k-long subarrays i leetcode 3318": "def find_x_sum",
        "write a python function find the sequence of strings appeared on the screen leetcode 3324": "def string_sequence",
        "write a python function find the largest almost missing integer leetcode 3471": "def largest_almost_missing",
        "write a python function transform array to all equal elements leetcode 3576": "def can_make_equal",
        "write a python function flip square submatrix vertically leetcode 3643": "def reverse_submatrix",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def can_make_equal" not in synthesize_python(
        "write a python function transform array by parity leetcode 3467"
    )
    assert "def largest_almost_missing" not in synthesize_python(
        "write a python function find the largest integer"
    )
    assert "def report_spam" not in synthesize_python(
        "write a python function report a file path"
    )


def test_p123_balance_unique_columns_ships_heaters_stack():
    cases = {
        "write a python function account balance after rounded purchase leetcode 2806": "def account_balance_after_purchase",
        "write a python function largest unique number leetcode 1133": "def largest_unique_number",
        "write a python function delete columns to make sorted leetcode 944": "def min_deletion_size",
        "write a python function battleships in a board leetcode 419": "def count_battleships",
        "write a python function heaters leetcode 475": "def find_radius",
        "write a python function validate stack sequences leetcode 946": "def validate_stack_sequences",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def min_deletion_size" not in synthesize_python(
        "write a python function minimum deletion to make string balanced"
    )
    assert "def find_radius" not in synthesize_python(
        "write a python function find the radius of a circle"
    )
    assert "def largest_unique_number" not in synthesize_python(
        "write a python function largest unique character"
    )

def test_p124_triangle_tag_neighbor_rope_squares():
    cases = {
        "write a python function maximum height of a triangle leetcode 3200": "def max_height_of_triangle",
        "write a python function generate tag for video caption leetcode 3582": "def generate_tag",
        "write a python function neighbor sum adjacent leetcode 3242": "def neighbor_adjacent_sum",
        "write a python function neighbor diagonal sum leetcode 3242": "def neighbor_diagonal_sum",
        "write a python function minimum time to make rope colorful leetcode 1578": "def min_cost_rope_colorful",
        "write a python function count square submatrices with all ones leetcode 1277": "def count_squares",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def max_height_of_triangle" not in synthesize_python(
        "write a python function maximum height of a binary tree"
    )
    assert "def count_squares" not in synthesize_python(
        "write a python function valid perfect square"
    )


def test_p125_covered_days_arrows_insert_intersect_erase():
    cases = {
        "write a python function to remove covered intervals": "def remove_covered_intervals",
        "write a function that counts days without meetings": "def count_days",
        "write a python function for minimum number of arrows to burst balloons": "def find_min_arrow_shots",
        "write a python function insert interval leetcode 57": "def insert_interval",
        "write a python function interval list intersections leetcode 986": "def interval_intersection",
        "write a python function non-overlapping intervals leetcode 435": "def erase_overlap_intervals",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    assert "def burst_balloons" not in synthesize_python(
        "write a python function for minimum number of arrows to burst balloons"
    )
    assert "def merge_intervals" not in synthesize_python(
        "write a python function non-overlapping intervals"
    )
    assert "def find_min_arrow_shots" not in synthesize_python(
        "write a python function burst balloons leetcode 312"
    )
    assert "def erase_overlap_intervals" not in synthesize_python(
        "write a python function merge intervals"
    )


def test_p126_product_carpool_partition_zigzag_atoi_freq():
    cases = {
        "write a python function maximum product of two elements in an array leetcode 1464": "def max_product",
        "write a python function car pooling leetcode 1094": "def carPooling",
        "write a python function partition labels leetcode 763": "def partitionLabels",
        "write a python function zigzag conversion leetcode 6": "def convert",
        "write a python function string to integer atoi leetcode 8": "def myAtoi",
        "write a python function sort characters by frequency leetcode 451": "def frequencySort",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    plain = synthesize_python("write a python function to multiply two numbers")
    assert "def multiply" in plain
    assert "def max_product" not in plain


def test_p127_next_greater_iii_skyline_bulls():
    cases = {
        "write a function for next greater element III leetcode 556": "def nextGreaterElement",
        "implement max increase to keep city skyline leetcode 807": "def maxIncreaseKeepingSkyline",
        "write a function bulls and cows leetcode 299": "def getHint",
        "implement string to integer atoi": "def myAtoi",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    plain = synthesize_python("write a python function next greater element")
    assert "def next_greater_element" in plain
    assert "def nextGreaterElement" not in plain
    from agents import _wants_code_written
    assert _wants_code_written("implement max increase to keep city skyline leetcode 807")
    assert not _wants_code_written("```python\nprint(1)\n```")
    assert not _wants_code_written("print(2 + 2)")


def test_p128_queue_rooms_koko_letters_envelopes_division():
    cases = {
        "write a python function queue reconstruction by height leetcode 406": "def reconstructQueue",
        "write a python function serialize binary tree leetcode 297": "def serialize",
        "write a python function koko eating bananas leetcode 875": "def minEatingSpeed",
        "write a python function remove duplicate letters leetcode 316": "def removeDuplicateLetters",
        "write a python function russian doll envelopes leetcode 354": "def maxEnvelopes",
        "write a python function evaluate division leetcode 399": "def calcEquation",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
    # do not steal remove-duplicates-from-array or next-greater
    plain = synthesize_python("write a python function remove duplicates from sorted array")
    assert "def removeDuplicateLetters" not in plain
    rooms = synthesize_python("write a python function for meeting rooms ii")
    assert "def meeting_rooms_ii" in rooms
    assert "def serialize" not in rooms


def test_p129_reverse_add_password():
    cases = {
        "reverse string leetcode 344": "def reverseString",
        "reverse string ii leetcode 541": "def reverseStr",
        "add two numbers ii leetcode 445": "def addTwoNumbers",
        "strong password checker leetcode 420": "def strongPasswordChecker",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
        assert bundle["fallback"] is False
    plain = synthesize_python("write a function to reverse a string")
    assert "def reverse_string" in plain
    assert "def reverseString" not in plain
    add = synthesize_python("add two numbers")
    assert "def add(" in add
    assert "def addTwoNumbers" not in add
    rooms = synthesize_python("write a python function for meeting rooms ii")
    assert "def meeting_rooms_ii" in rooms
    assert "def minMeetingRooms" not in rooms


def test_p130_graph_dp_board():
    cases = {
        "swim in rising water leetcode 778": "def swimInWater",
        "path with minimum effort leetcode 1631": "def minimumEffortPath",
        "shortest path in binary matrix leetcode 1091": "def shortestPathBinaryMatrix",
        "snakes and ladders leetcode 909": "def snakesAndLadders",
        "bus routes leetcode 815": "def numBusesToDestination",
        "sequence reconstruction leetcode 444": "def sequenceReconstruction",
        "implement cherry pickup leetcode 741": "def cherryPickup",
        "implement odd even jump leetcode 975": "def oddEvenJumps",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
        assert bundle["fallback"] is False
    add = synthesize_python("write a python function that adds two numbers")
    assert "def add(" in add
    rooms = synthesize_python("write a python function for meeting rooms ii")
    assert "def meeting_rooms_ii" in rooms


def test_p132_taps_jobs_puzzle():
    cases = {
        "minimum number of taps to open to water a garden leetcode 1326": "def minTaps",
        "shortest path visiting all nodes leetcode 847": "def shortestPathLength",
        "maximum profit in job scheduling leetcode 1235": "def jobScheduling",
        "sliding puzzle leetcode 773": "def slidingPuzzle",
        "minimum cost to make at least one valid path leetcode 1368": "def minCost",
        "race car leetcode 818": "def racecar",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
        assert bundle["fallback"] is False
    stock = synthesize_python("write a python function that computes max profit on a stock")
    assert "def max_profit" in stock
    lock = synthesize_python("open the lock leetcode 752")
    assert "def openLock" in lock or "def open_lock" in lock


def test_p133_trees_keys_knight():
    cases = {
        "cut off trees for golf event leetcode 675": "def cutOffTree",
        "shortest path to get all keys leetcode 864": "def shortestPathAllKeys",
        "shortest path in a grid with obstacles elimination leetcode 1293": "def shortestPath",
        "dungeon game leetcode 174": "def calculateMinimumHP",
        "knight probability in chessboard leetcode 688": "def knightProbability",
        "minimum knight moves leetcode 1197": "def minKnightMoves",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
        assert bundle["fallback"] is False
    stock = synthesize_python("write a python function that computes max profit on a stock")
    assert "def max_profit" in stock
    lock = synthesize_python("open the lock leetcode 752")
    assert "def openLock" in lock or "def open_lock" in lock


def test_p134_gates_enclaves():
    cases = {
        "walls and gates leetcode 286": "def wallsAndGates",
        "as far from land as possible leetcode 1162": "def maxDistance",
        "path with maximum probability leetcode 1514": "def maxProbability",
        "number of enclaves leetcode 1020": "def numEnclaves",
        "making a large island leetcode 827": "def largestIsland",
        "minimum genetic mutation leetcode 433": "def minMutation",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
        assert bundle["fallback"] is False
    islands = synthesize_python("number of islands leetcode 200")
    assert "def num_islands" in islands or "def numIslands" in islands
    knight = synthesize_python("knight probability in chessboard leetcode 688")
    assert "def knightProbability" in knight


def test_p135_closed_islands_routes():
    cases = {
        "number of closed islands leetcode 1254": "def closedIsland",
        "all paths from source to target leetcode 797": "def allPathsSourceTarget",
        "find eventual safe states leetcode 802": "def eventualSafeNodes",
        "time needed to inform all employees leetcode 1376": "def numOfMinutes",
        "detonate the maximum bombs leetcode 2101": "def maximumDetonation",
        "reorder routes to make all paths lead to the city zero leetcode 1466": "def minReorder",
    }
    for q, needle in cases.items():
        src = synthesize_python(q)
        assert needle in src, (q, src[:240])
        bundle = synthesize_and_verify(q)
        assert bundle["verified"] is True, (q, bundle)
        assert bundle["fallback"] is False
    islands = synthesize_python("number of islands leetcode 200")
    assert "def num_islands" in islands or "def numIslands" in islands
    tickets = synthesize_python("time needed to buy tickets")
    assert "def time_required_to_buy" in tickets



def test_p136_missing_graph():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "clone graph leetcode 133": "clone_graph",
        "graph valid tree leetcode 261": "graph_valid_tree",
        "possible bipartition leetcode 886": "possible_bipartition",
        "flower planting with no adjacent gardens leetcode 1042": "flower_planting",
        "nearest exit from entrance in maze leetcode 1926": "nearest_exit",
        "max area of island leetcode 695": "max_area_of_island",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("can place flowers in a flowerbed").name == "can_place_flowers"
    assert match_template("is graph bipartite").name == "is_bipartite"


def test_p137_maze_union():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "the maze leetcode 490": "the_maze",
        "the maze ii leetcode 505": "the_maze_ii",
        "sentence similarity ii leetcode 737": "sentence_similarity_ii",
        "satisfiability of equality equations leetcode 990": "equality_equations",
        "count unreachable pairs of nodes in an undirected graph leetcode 2316": "unreachable_pairs",
        "find closest node to given two nodes leetcode 2359": "closest_meeting_node",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("nearest exit from entrance in maze leetcode 1926").name == "nearest_exit"
    assert match_template("is graph bipartite").name == "is_bipartite"


def test_p138_maze_swaps():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "the maze iii leetcode 499": "the_maze_iii",
        "regions cut by slashes leetcode 959": "regions_cut_by_slashes",
        "smallest string with swaps leetcode 1202": "smallest_string_with_swaps",
        "accounts merge leetcode 721": "accounts_merge",
        "redundant connection leetcode 684": "redundant_connection",
        "similar string groups leetcode 839": "similar_string_groups",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("the maze leetcode 490").name == "the_maze"
    assert match_template("the maze ii leetcode 505").name == "the_maze_ii"
    assert match_template("smallest string starting from leaf").name != "smallest_string_with_swaps"
    assert match_template("redundant connection ii") is None or match_template("redundant connection ii").name != "redundant_connection"


def test_p139_directed_weighted_graphs():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "redundant connection ii leetcode 685": "redundant_connection_ii",
        "shortest path with alternating colors leetcode 1129": "shortest_alternating_paths",
        "network delay time leetcode 743": "network_delay_time",
        "cheapest flights within k stops leetcode 787": "cheapest_flights",
        "open the lock leetcode 752": "open_the_lock",
        "critical connections in a network leetcode 1192": "critical_connections",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("redundant connection leetcode 684").name == "redundant_connection"
    assert match_template("swim in rising water leetcode 778").name == "swim_rising_water_778"
    assert match_template("alternating sum of an array").name != "shortest_alternating_paths"


def test_p140_graph_union_mst():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "number of operations to make network connected leetcode 1319": "make_network_connected",
        "most stones removed with same row or column leetcode 947": "most_stones_removed",
        "find the city with the smallest number of neighbors at a threshold distance leetcode 1334": "find_the_city",
        "minimum obstacle removal to reach corner leetcode 2290": "min_obstacle_removal",
        "number of distinct islands leetcode 694": "distinct_islands",
        "connecting cities with minimum cost leetcode 1135": "connecting_cities_min_cost",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("number of islands leetcode 200").name == "num_islands"
    assert match_template("min cost to connect all points leetcode 1584").name == "min_cost_connect_points"
    assert match_template("shortest path in a grid with obstacles elimination leetcode 1293").name == "shortest_path_obstacles"
    assert match_template("number of connected components in an undirected graph leetcode 323").name == "count_components"


def test_p141_graph_mst_paths():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "count the number of complete components leetcode 2685": "count_complete_components",
        "checking existence of edge length limited paths leetcode 1697": "distance_limited_paths",
        "find critical and pseudo-critical edges in minimum spanning tree leetcode 1489": "critical_pseudo_critical_edges",
        "minimum score of a path between two cities leetcode 2492": "min_score_path",
        "minimum cost to make at least one valid path in a grid leetcode 1368": "min_cost_valid_path",
        "number of restricted paths from first to last node leetcode 1786": "count_restricted_paths",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("critical connections in a network leetcode 1192").name == "critical_connections"
    assert match_template("connecting cities with minimum cost leetcode 1135").name == "connecting_cities_min_cost"
    assert match_template("number of islands leetcode 200").name == "num_islands"


def test_p142_path_counts_meetings():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "number of ways to arrive at destination leetcode 1976": "count_paths_arrive",
        "minimum fuel cost to report to the capital leetcode 2477": "minimum_fuel_capital",
        "minimum cost to reach destination in time leetcode 1928": "min_cost_destination_time",
        "reachable nodes in subdivided graph leetcode 882": "reachable_nodes_subdivided",
        "second minimum time to reach destination leetcode 2045": "second_minimum_time",
        "find all people with secret leetcode 2092": "find_all_people_secret",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("cheapest flights within k stops leetcode 787").name == "cheapest_flights"
    assert match_template("network delay time leetcode 743").name == "network_delay_time"
    assert match_template("path with maximum probability leetcode 1514").name == "maximum_probability_path"


def test_p143_friends_water_visit():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "the earliest moment when everyone become friends leetcode 1101": "earliest_friends",
        "optimize water distribution in a village leetcode 1168": "optimize_water_distribution",
        "minimum time to visit a cell in a grid leetcode 2577": "min_time_visit_cell",
        "shortest path visiting all nodes leetcode 847": "shortest_path_visiting_all",
        "last day where you can still cross leetcode 1970": "last_day_to_cross",
        "word ladder leetcode 127": "word_ladder",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("bus routes leetcode 815").name == "bus_routes_815"
    assert match_template("word break leetcode 139").name != "word_ladder"
    assert match_template("the maze ii shortest rolling distance").name != "word_ladder"


def test_p144_bfs_maze_home():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "minimum operations to convert number leetcode 2059": "minimum_operations_convert",
        "escape the ghosts leetcode 789": "escape_ghosts",
        "escape a large maze leetcode 1036": "escape_large_maze",
        "shortest path to get food leetcode 1730": "shortest_path_food",
        "check if there is a valid path in a grid leetcode 1391": "valid_street_path",
        "minimum jumps to reach home leetcode 1654": "minimum_jumps_home",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("jump game ii minimum jumps to last index").name == "jump_game_ii"
    assert match_template("minimum cost to make at least one valid path in a grid leetcode 1368").name == "min_cost_valid_path"
    assert match_template("the maze ii shortest rolling distance").name != "escape_large_maze"


def test_p145_box_courses_island():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "minimum moves to move a box to their target location leetcode 1263": "min_push_box",
        "parallel courses iii leetcode 2050": "parallel_courses_iii",
        "minimum number of days to disconnect island leetcode 1568": "min_days_disconnect_island",
        "as far from land as possible leetcode 1162": "as_far_from_land",
        "time needed to inform all employees leetcode 1376": "inform_employees",
        "minimum number of vertices to reach all nodes leetcode 1557": "min_vertices_reach_all",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("number of islands leetcode 200").name == "num_islands"
    assert match_template("making a large island leetcode 827").name != "min_days_disconnect_island"
    assert match_template("number of closed islands leetcode 1254").name != "min_days_disconnect_island"



def test_p146_heap_ladder_ii():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "word ladder ii leetcode 126 all shortest transformation sequences": "word_ladder_ii",
        "ipo leetcode 502 maximized capital": "ipo_capital",
        "maximum performance of a team leetcode 1383": "max_team_performance",
        "furthest building you can reach leetcode 1642": "furthest_building",
        "minimum cost to hire k workers leetcode 857": "min_cost_hire_workers",
        "minimum number of refueling stops leetcode 871": "min_refuel_stops",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("word ladder leetcode 127").name == "word_ladder"
    assert match_template("course schedule leetcode 207").name == "course_schedule"
    assert match_template("trapping rain water leetcode 42").name == "trap_rain_water"


def test_p147_interval_game():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "strange printer leetcode 664": "strange_printer",
        "minimum cost to cut a stick leetcode 1547": "min_cost_cut_stick",
        "cat and mouse game leetcode 913": "cat_mouse_game",
        "super egg drop leetcode 887": "super_egg_drop",
        "palindrome partitioning ii leetcode 132 minimum cuts": "palindrome_partition_ii",
        "maximum profit in job scheduling leetcode 1235": "job_scheduling_profit",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("palindrome partitioning leetcode 131").name == "palindrome_partition"
    assert match_template("best time to buy and sell stock").name != "job_scheduling_profit"


def test_snake_aliases_for_legacy_smoke():
    """Later packs emit LC camelCase; older smoke rows expect snake_case defs."""
    from code_synth import synthesize_and_verify
    asks = {
        "write a python function for network delay time": "def network_delay_time",
        "write a python function for cheapest flights with k stops": "def cheapest_flights",
        "write a python function for word ladder": "def word_ladder",
        "write a python function that merges accounts": "def accounts_merge",
        "write a python function for redundant connection": "def redundant_connection",
        "write a python function for critical connections": "def critical_connections",
        "write a python function that open the lock": "def open_lock",
        "network delay time leetcode 743": "def networkDelayTime",
        "word ladder leetcode 127": "def ladderLength",
    }
    for ask, needle in asks.items():
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
        assert needle in out["source"], (ask, needle)


def test_p148_hard_dp_games():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "cat and mouse ii leetcode 1728": "cat_mouse_ii",
        "minimum cost to merge stones leetcode 1000": "merge_stones",
        "longest palindromic substring leetcode 5": "longest_palindromic_substring",
        "shortest common supersequence leetcode 1092": "shortest_common_supersequence",
        "distinct subsequences ii leetcode 940": "distinct_subsequences_ii",
        "minimum score triangulation leetcode 1039": "min_score_triangulation",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], out
    assert match_template("cat and mouse game leetcode 913").name == "cat_mouse_game"
    assert match_template("distinct subsequences leetcode 115").name == "distinct_subsequences"
    assert match_template("longest palindromic subsequence").name == "longest_palindromic_subsequence"


def test_p150_stolen_and_missing():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "maximize sum of array after k negations leetcode 1005": "largest_sum_after_k_negations",
        "count negative numbers in a sorted matrix leetcode 1351": "count_negatives_1351",
        "sort integers by the number of 1 bits leetcode 1356": "sort_by_bits",
        "verifying an alien dictionary leetcode 953": "is_alien_sorted",
        "distribute candies to people leetcode 1103": "distribute_candies_people",
        "convert integer to the sum of two no-zero integers leetcode 1317": "get_no_zero_integers",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a python function that sums a list of numbers").name == "sum_list"
    assert match_template("candy leetcode 135").name == "candy"
    assert match_template("leetcode 135 ratings").name == "candy"


def test_p152_product_cameras_string_fixed_pairs_powers():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "maximum product of three numbers": "maximum_product",
        "leetcode 628": "maximum_product",
        "binary tree cameras": "min_camera_cover",
        "smallest string with a given numeric value": "get_smallest_string",
        "fixed point in a sorted array": "fixed_point",
        "index pairs of a string": "index_pairs",
        "check if number is a sum of powers of three": "check_powers_of_three",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("maximum product of two elements").name == "max_product_two"
    assert match_template("smallest string with swaps").name == "smallest_string_with_swaps"
    assert match_template("write a python function that sums a list of numbers").name == "sum_list"


def test_p153_schedule_iii_stone_ii_vowels_split_hand_span():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "course schedule iii leetcode 630": "course_schedule_iii",
        "last stone weight ii leetcode 1049": "last_stone_weight_ii",
        "maximum number of vowels in a substring of given length leetcode 1456": "max_vowels",
        "number of ways to split a string leetcode 1573": "num_ways_split",
        "hand of straights leetcode 846": "hand_of_straights",
        "online stock span leetcode 901": "online_stock_span",
        "course schedule leetcode 207": "course_schedule",
        "last stone weight leetcode 1046": "last_stone_weight",
        "write a python function that counts vowels in a string": "count_vowels",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)


def test_p154_elimination_parens_ramp_tokens_boats_fleet():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "elimination game leetcode 390": "elimination_game",
        "minimum add to make parentheses valid leetcode 921": "min_add_to_make_valid",
        "maximum width ramp leetcode 962": "maximum_width_ramp",
        "bag of tokens leetcode 948": "bag_of_tokens",
        "boats to save people leetcode 881": "boats_to_save",
        "car fleet leetcode 853": "car_fleet",
        "valid parentheses": "valid_parentheses",
        "car pooling leetcode 1094": "car_pooling",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)


def test_p155_grammar_pancake_deck_advantage_chunks_malware():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "kth grammar leetcode 779": "kth_grammar",
        "pancake sorting leetcode 969": "pancake_sort",
        "reveal cards in increasing order leetcode 950": "deck_revealed_increasing",
        "advantage shuffle leetcode 870": "advantage_shuffle",
        "max chunks to make sorted leetcode 769": "max_chunks_to_sorted",
        "minimize malware spread leetcode 924": "min_malware_spread",
        "car fleet leetcode 853": "car_fleet",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)


def test_p156_wiggle_malware_stack_tokens_disjoint_digits():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "wiggle sort ii leetcode 324": "wiggle_sort_ii",
        "minimize malware spread ii leetcode 928": "min_malware_spread_ii",
        "validate stack sequences leetcode 946": "validate_stack_sequences",
        "bag of tokens leetcode 948": "bag_of_tokens",
        "partition array into disjoint intervals leetcode 915": "partition_disjoint",
        "monotone increasing digits leetcode 738": "monotone_increasing_digits",
        "longest wiggle subsequence": "wiggle_subsequence",
        "minimize malware spread leetcode 924": "min_malware_spread",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)


def test_p157_even_or_missing_ops_triplet_groups_shifts_split():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "bitwise or of even numbers in an array leetcode 3688": "even_numbers_bitwise_or",
        "smallest missing integer greater than sequential prefix sum leetcode 2996": "missing_integer",
        "check if strings can be made equal with operations i leetcode 2839": "can_be_equal_ops",
        "maximum value of an ordered triplet i leetcode 2873": "maximum_triplet_value",
        "longest unequal adjacent groups subsequence i leetcode 2900": "unequal_adjacent_groups",
        "matrix similarity after cyclic shifts leetcode 2946": "matrix_similarity_shifts",
        "maximum even split leetcode 2178": "maximum_even_split",
        "write a python function that checks if a number is even": "is_even",
        "write a python function that computes the running sum of a list": "running_sum",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)


def test_p158_merge_invert_zip_sorted_keys():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a python function that merges two dictionaries": "merge_dicts",
        "write a function that returns the keys of a dictionary sorted by value": "keys_sorted_by_value",
        "write a function that inverts a dictionary": "invert_dict",
        "write a python function that swaps keys and values of a dict": "invert_dict",
        "write a python function to zip two lists into a dict": "zip_to_dict",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("merge intervals leetcode 56").name != "merge_dicts"
    alien = match_template("alien dictionary leetcode 269")
    assert alien is None or alien.name != "invert_dict"


def test_p160_copy_longest_filter_query_order_none():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a python function that deep copies a list": "deep_copy",
        "write a function that returns the longest word in a sentence": "longest_word",
        "write a python function that filters even numbers": "filter_even",
        "write a python function that parses a query string into a dict": "parse_query",
        "write a python function to check if two lists are equal ignoring order": "equal_ignore_order",
        "write a function to drop none values from a list": "drop_none",
        "write a function that capitalizes each word": "title_case",
        "write a python function that reverses words in a sentence": "reverse_words",
        "write a function that snake_case converts a string": "camel_to_snake",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that checks if a number is even").name == "is_even"


def test_p161_interleave_digit_unique_swap_punct_pairs():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a python function that interleaves two lists": "interleave",
        "write a function that returns the digit sum of a number": "digit_sum",
        "write a function that returns unique characters in a string": "unique_chars",
        "write a python function that swaps two variables": "swap_values",
        "write a function that removes punctuation from a string": "remove_punctuation",
        "write a python function that converts a list of pairs to a dict": "pairs_to_dict",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a python function to zip two lists into a dict").name == "zip_to_dict"
    assert match_template("write a function that returns unique items in a list").name != "unique_chars"
    # Cycle 443: broad digit_sum must not steal LeetCode siblings.
    siblings = {
        "write a python function that sum of digits of string after convert": "get_lucky",
        "write a python function that count integers with even digit sum": "count_even",
        "write a python function sum of digits in base k leetcode 1837": "sum_base",
    }
    for ask, name in siblings.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)


def test_p162_collatz_rle_argmax_rot13_slug_ipv4():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a python function that counts collatz steps": "collatz_steps",
        "write a function that run length encodes a string": "run_length_encode",
        "write a function that returns the argmax of a list": "argmax_list",
        "write a python function that applies rot13": "rot13",
        "write a function that slugifies a title": "slugify",
        "write a function that checks if a string is a valid ipv4 address": "is_ipv4",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    # Must not steal Caesar, title-case, or defang.
    assert match_template("write a python function that applies a caesar shift").name == "caesar_shift"
    assert match_template("write a function that converts a string to title case").name != "slugify"
    assert match_template("write a function that defangs an ip address").name == "defang_ip_addr"




def test_p163_luhn_atbash_pig_isbn_soundex_hms():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a python function that checks a luhn checksum": "luhn_valid",
        "write a function that applies the atbash cipher": "atbash",
        "write a python function that converts text to pig latin": "pig_latin",
        "write a function that validates an isbn-10": "isbn10_valid",
        "write a function that returns the soundex code of a name": "soundex",
        "write a function that converts seconds to hms": "seconds_to_hms",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a python function that applies a caesar shift").name == "caesar_shift"
    assert match_template("write a python function that applies rot13").name == "rot13"


def test_p164_haversine_hamming_morse_hex_email_leap():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a python function that computes haversine distance": "haversine_km",
        "write a function that returns the hamming distance of two strings": "hamming_distance",
        "write a python function that encodes text as morse code": "morse_encode",
        "write a function that converts a hex color to rgb": "hex_to_rgb",
        "write a function that checks if a string is a valid email": "is_email",
        "write a function that checks if a year is a leap year": "is_leap_year",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that counts unique morse representations").name == "unique_morse_representations"
    assert match_template("write a python function that applies a caesar shift").name == "caesar_shift"


def test_p165_rgb_base_roman_url_wrap_weekday():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that converts rgb to hex": "rgb_to_hex",
        "write a python function that converts an integer to any base": "int_to_base",
        "write a function that returns the sample standard deviation": "sample_stdev",
        "write a function that url encodes a string": "url_encode",
        "write a python function that word wraps text": "word_wrap",
        "write a function that returns the weekday name of a date": "weekday_name",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that converts a hex color to rgb").name == "hex_to_rgb"
    assert match_template("write a function that converts roman numerals to an integer").name == "roman_to_int"
    assert match_template("write a python function that converts an integer to roman").name == "integer_to_roman"
    assert match_template("write a function that converts to base7").name == "convert_to_base7"


def test_p166_factors_b64_celsius_urldecode_pct_z():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the prime factors of an integer": "prime_factors",
        "write a function that base64 encodes a string": "base64_encode",
        "write a function that converts celsius to fahrenheit": "celsius_to_fahrenheit",
        "write a function that url decodes a string": "url_decode",
        "write a function that returns the percentile of a list": "percentile",
        "write a function that returns z-scores of a list": "z_scores",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that checks if a number is prime").name == "is_prime"
    assert match_template("write a function that decodes a string").name == "decode_string"
    assert match_template("write a function that url encodes a string").name == "url_encode"
    assert match_template("write a function that returns the sample standard deviation").name == "sample_stdev"


def test_p167_b64decode_f2c_rle_sha_binom_miles():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that base64 decodes a string": "base64_decode",
        "write a function that converts fahrenheit to celsius": "fahrenheit_to_celsius",
        "write a function that run-length decodes a list of pairs": "run_length_decode",
        "write a function that returns the sha256 hex digest of a string": "sha256_hex",
        "write a function that returns the binomial coefficient n choose k": "binomial",
        "write a function that converts miles to kilometers": "miles_to_km",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that base64 encodes a string").name == "base64_encode"
    assert match_template("write a function that converts celsius to fahrenheit").name == "celsius_to_fahrenheit"
    assert match_template("write a function that run-length encodes a string").name == "run_length_encode"
    assert match_template("write a function that decodes a string").name == "decode_string"
    assert match_template("write a function that returns the prime factors of an integer").name == "prime_factors"


def test_p168_md5_jaccard_bytes_kebab_html_cosine():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the md5 hex digest of a string": "md5_hex",
        "write a function that returns the jaccard similarity of two sets": "jaccard_similarity",
        "write a function that humanizes a byte count": "humanize_bytes",
        "write a function that converts a string to kebab-case": "kebab_case",
        "write a function that strips html tags from a string": "strip_html",
        "write a function that returns the cosine similarity of two vectors": "cosine_similarity",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that returns the sha256 hex digest of a string").name == "sha256_hex"
    assert match_template("write a function that converts camel case to snake case").name == "camel_to_snake"
    assert match_template("write a function that converts snake case to camel case").name == "snake_to_camel"
    assert match_template("write a function that decodes a string").name == "decode_string"


def test_p169_sha1_crc32_dice_thousands_query_hms_triangular():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the sha1 hex digest of a string": "sha1_hex",
        "write a function that returns the crc32 of a string": "crc32_hex",
        "write a function that returns the dice coefficient of two sets": "dice_coefficient",
        "write a function that formats a number with thousands separators": "thousands_separators",
        "write a function that builds a query string from a dict": "build_query",
        "write a function that parses hh:mm:ss to seconds": "hms_to_seconds",
        "write a function that returns the nth triangular number": "triangular",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a python function that parses a query string into a dict").name == "parse_query"
    assert match_template("write a function that converts seconds to hms").name == "seconds_to_hms"
    assert match_template("write a function that returns the sha256 hex digest of a string").name == "sha256_hex"
    assert match_template("write a function that returns the md5 hex digest of a string").name == "md5_hex"




def test_p170_hmac_iban_percent_uuid_digital_ellipsize_gray():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the hmac-sha256 hex digest of a message": "hmac_sha256_hex",
        "write a function that checks whether an iban is valid": "iban_valid",
        "write a function that percent-encodes a string": "percent_encode",
        "write a function that checks whether a string is a valid uuid": "is_uuid",
        "write a function that returns the digital root of a number": "digital_root",
        "write a function that ellipsizes a string": "ellipsize",
        "write a function that returns the gray code of an integer": "gray_code",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that returns the sha256 hex digest of a string").name == "sha256_hex"
    assert match_template("write a function that builds a query string from a dict").name == "build_query"


def test_p171_semver_base32_cidr_nfc_jw_duration_ean_pearson_shannon():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that parses a semver version": "parse_semver",
        "write a function that encodes a string as base32": "base32_encode",
        "write a function that checks whether an ip is in a cidr range": "ip_in_cidr",
        "write a function that normalizes unicode to nfc": "unicode_nfc",
        "write a function that returns the jaro-winkler similarity": "jaro_winkler",
        "write a function that formats a duration in seconds as human text": "humanize_duration",
        "write a function that checks an ean-13 barcode": "ean13_valid",
        "write a function that returns the pearson correlation of two lists": "pearson",
        "write a function that returns the shannon entropy of a string": "shannon_entropy",
        "write a function that wraps text to a width": "word_wrap",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that decodes a base32 string").name != "base32_encode"
    assert match_template("write a function that returns the sha256 hex digest of a string").name == "sha256_hex"


def test_p172_iso_plural_space_deep_spearman_accents_ngram_gmean_ordinal():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the iso week of a date": "iso_week",
        "write a function that pluralizes an english word": "pluralize",
        "write a function that collapses whitespace in a string": "collapse_whitespace",
        "write a function that deep gets a dotted path": "deep_get",
        "write a function that returns the spearman correlation of two lists": "spearman",
        "write a function that strips accents from text": "strip_accents",
        "write a function that returns character n-grams": "char_ngrams",
        "write a function that returns the geometric mean of a list": "geometric_mean",
        "write a function that returns the english ordinal of an integer": "ordinal",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that normalizes unicode to nfc").name == "unicode_nfc"
    assert match_template("write a function that returns the pearson correlation of two lists").name == "pearson"
    assert match_template("write a function that wraps text to a width").name == "word_wrap"


def test_p173_manhattan_chebyshev_softmax_iqr_vigenere_html_lerp_modinv():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the manhattan distance of two points": "manhattan_distance",
        "write a function that returns the chebyshev distance of two points": "chebyshev_distance",
        "write a function that returns the softmax of a list": "softmax",
        "write a function that returns the interquartile range of a list": "interquartile_range",
        "write a function that encrypts text with a vigenere cipher": "vigenere_encrypt",
        "write a function that escapes html special characters": "escape_html",
        "write a function that linearly interpolates two numbers": "lerp",
        "write a function that returns the modular inverse": "mod_inverse",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that returns the running sum").name == "running_sum"
    assert match_template("write a function that multiplies two numbers").name == "multiply"


def test_p174_harmonic_unix_onehot_quantile_var_singular_duration():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the harmonic mean of a list": "harmonic_mean",
        "write a function that converts a unix timestamp to an iso-8601 date": "unix_to_iso",
        "write a function that converts an iso-8601 date to a unix timestamp": "iso_to_unix",
        "write a function that one-hot encodes an index": "one_hot",
        "write a function that returns a quantile of a list": "quantile",
        "write a function that returns the population variance of a list": "population_variance",
        "write a function that singularizes an english noun": "singularize",
        "write a function that parses a duration string like 1h30m into seconds": "parse_duration",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that returns the average of two numbers").name == "average"
    assert match_template("write a function that returns the geometric mean of a list").name == "geometric_mean"
    assert match_template("write a function that returns the percentile of a list").name == "percentile"
    assert match_template("write a function that humanizes a duration in seconds").name == "humanize_duration"
    assert match_template("write a function that pluralizes an english word").name == "pluralize"


def test_p175_levenshtein_sigmoid_logsoftmax_url_snake_camel():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the levenshtein distance of two strings": "levenshtein",
        "write a function that returns the sigmoid of a number": "sigmoid",
        "write a function that returns the log softmax of a list": "log_softmax",
        "write a function that urlencodes query parameters": "urlencode",
        "write a function that converts text to snake case": "snake_case",
        "write a function that converts text to camel case": "camel_case",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that returns the softmax of a list").name == "softmax"


def test_p176_damerau_totient_rmse_mae_r2_fnv():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the damerau levenshtein distance of two strings": "damerau_levenshtein",
        "write a function that returns the euler totient of n": "euler_totient",
        "write a function that returns the rmse of two lists": "rmse",
        "write a function that returns the mean absolute error of two lists": "mae",
        "write a function that returns the r2 score of two lists": "r2_score",
        "write a function that returns the fnv1a hash of a string": "fnv1a_32",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that returns the levenshtein distance of two strings").name == "levenshtein"
    assert match_template("write a function that returns the average of two numbers").name == "average"
    assert match_template("write a function that returns the mean of a list").name == "average"


def test_p177_smoothstep_isbn13_adler_map_slerp():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that returns the smootherstep of an edge and x": "smootherstep",
        "write a function that returns the smoothstep of an edge and x": "smoothstep",
        "write a function that checks whether an isbn-13 is valid": "isbn13_valid",
        "write a function that returns the adler32 checksum of a string": "adler32",
        "write a function that remaps a number from one range to another": "map_range",
        "write a function that returns the slerp of two angles": "slerp_scalar",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that checks whether an isbn-10 is valid").name == "isbn10_valid"
    assert match_template("write a function that linearly interpolates two numbers").name == "lerp"


def test_p179_metar_dew_bearing_roman_direction():
    from code_synth import match_template, synthesize_and_verify
    asks = {
        "write a function that converts an integer to a roman numeral": "integer_to_roman",
        "write a function that parses a METAR weather string": "parse_metar",
        "write a function that computes the dew point from temperature and humidity": "dew_point_c",
        "write a function that computes the bearing between two coordinates": "initial_bearing",
        "write a function that returns the next prime after n": "next_prime",
        "write a function that returns the phonetic metaphone of a word": "metaphone_primary",
    }
    for ask, name in asks.items():
        hit = match_template(ask)
        assert hit is not None and hit.name == name, (ask, getattr(hit, "name", None))
        out = synthesize_and_verify(ask)
        assert out["verified"] and not out["fallback"], (ask, out)
    assert match_template("write a function that converts a roman numeral to an integer").name == "roman_to_int"
    assert match_template("write a function that computes the soundex code of a name").name == "soundex"
    assert match_template("write a function that computes haversine distance between two lat lon points").name == "haversine_km"


