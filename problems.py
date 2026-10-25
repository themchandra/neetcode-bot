"""
Blind 75 problem list.
Each entry: (id, name, difficulty, topic, neetcode_url)
"""

PROBLEMS = [
    # ── Arrays ────────────────────────────────────────────────────────────────
    (1,  "Two Sum",                                        "Easy",   "Arrays",                    "https://neetcode.io/problems/two-sum"),
    (2,  "Best Time to Buy and Sell Stock",                "Easy",   "Arrays",                    "https://neetcode.io/problems/buy-and-sell-crypto"),
    (3,  "Contains Duplicate",                             "Easy",   "Arrays",                    "https://neetcode.io/problems/duplicate-integer"),
    (4,  "Product of Array Except Self",                   "Medium", "Arrays",                    "https://neetcode.io/problems/products-of-array-discluding-self"),
    (5,  "Maximum Subarray",                               "Medium", "Arrays",                    "https://neetcode.io/problems/maximum-subarray"),
    (6,  "Maximum Product Subarray",                       "Medium", "Arrays",                    "https://neetcode.io/problems/maximum-product-subarray"),
    (7,  "Find Minimum in Rotated Sorted Array",           "Medium", "Arrays",                    "https://neetcode.io/problems/find-minimum-in-rotated-sorted-array"),
    (8,  "Search in Rotated Sorted Array",                 "Medium", "Arrays",                    "https://neetcode.io/problems/search-in-rotated-sorted-array"),
    (9,  "3Sum",                                           "Medium", "Arrays",                    "https://neetcode.io/problems/three-integer-sum"),
    (10, "Container With Most Water",                      "Medium", "Arrays",                    "https://neetcode.io/problems/max-water-container"),

    # ── Binary ────────────────────────────────────────────────────────────────
    (11, "Sum of Two Integers",                            "Medium", "Binary",                    "https://neetcode.io/problems/sum-of-two-integers"),
    (12, "Number of 1 Bits",                               "Easy",   "Binary",                    "https://neetcode.io/problems/number-of-one-bits"),
    (13, "Counting Bits",                                  "Easy",   "Binary",                    "https://neetcode.io/problems/counting-bits"),
    (14, "Missing Number",                                 "Easy",   "Binary",                    "https://neetcode.io/problems/missing-number"),
    (15, "Reverse Bits",                                   "Easy",   "Binary",                    "https://neetcode.io/problems/reverse-bits"),

    # ── Dynamic Programming ───────────────────────────────────────────────────
    (16, "Climbing Stairs",                                "Easy",   "Dynamic Programming",       "https://neetcode.io/problems/climbing-stairs"),
    (17, "Coin Change",                                    "Medium", "Dynamic Programming",       "https://neetcode.io/problems/coin-change"),
    (18, "Longest Increasing Subsequence",                 "Medium", "Dynamic Programming",       "https://neetcode.io/problems/longest-increasing-subsequence"),
    (19, "Longest Common Subsequence",                     "Medium", "Dynamic Programming",       "https://neetcode.io/problems/longest-common-subsequence"),
    (20, "Word Break",                                     "Medium", "Dynamic Programming",       "https://neetcode.io/problems/word-break"),
    (21, "Combination Sum IV",                             "Medium", "Dynamic Programming",       "https://neetcode.io/problems/combination-target-sum-with-repetition"),
    (22, "House Robber",                                   "Medium", "Dynamic Programming",       "https://neetcode.io/problems/house-robber"),
    (23, "House Robber II",                                "Medium", "Dynamic Programming",       "https://neetcode.io/problems/house-robber-ii"),
    (24, "Decode Ways",                                    "Medium", "Dynamic Programming",       "https://neetcode.io/problems/decode-ways"),
    (25, "Unique Paths",                                   "Medium", "Dynamic Programming",       "https://neetcode.io/problems/count-paths"),
    (26, "Jump Game",                                      "Medium", "Dynamic Programming",       "https://neetcode.io/problems/jump-game"),

    # ── Graph ─────────────────────────────────────────────────────────────────
    (27, "Clone Graph",                                    "Medium", "Graph",                     "https://neetcode.io/problems/clone-graph"),
    (28, "Course Schedule",                                "Medium", "Graph",                     "https://neetcode.io/problems/course-schedule"),
    (29, "Pacific Atlantic Water Flow",                    "Medium", "Graph",                     "https://neetcode.io/problems/pacific-atlantic-water-flow"),
    (30, "Number of Islands",                              "Medium", "Graph",                     "https://neetcode.io/problems/count-number-of-islands"),
    (31, "Longest Consecutive Sequence",                   "Medium", "Graph",                     "https://neetcode.io/problems/longest-consecutive-sequence"),
    (32, "Alien Dictionary",                               "Hard",   "Graph",                     "https://neetcode.io/problems/foreign-dictionary"),
    (33, "Graph Valid Tree",                               "Medium", "Graph",                     "https://neetcode.io/problems/valid-tree"),
    (34, "Number of Connected Components in an Undirected Graph", "Medium", "Graph",             "https://neetcode.io/problems/count-connected-components"),

    # ── Interval ──────────────────────────────────────────────────────────────
    (35, "Insert Interval",                                "Medium", "Interval",                  "https://neetcode.io/problems/insert-new-interval"),
    (36, "Merge Intervals",                                "Medium", "Interval",                  "https://neetcode.io/problems/merge-intervals"),
    (37, "Non-overlapping Intervals",                      "Medium", "Interval",                  "https://neetcode.io/problems/non-overlapping-intervals"),
    (38, "Meeting Rooms",                                  "Easy",   "Interval",                  "https://neetcode.io/problems/meeting-schedule"),
    (39, "Meeting Rooms II",                               "Medium", "Interval",                  "https://neetcode.io/problems/meeting-schedule-ii"),

    # ── Linked List ───────────────────────────────────────────────────────────
    (40, "Reverse Linked List",                            "Easy",   "Linked List",               "https://neetcode.io/problems/reverse-a-linked-list"),
    (41, "Linked List Cycle",                              "Easy",   "Linked List",               "https://neetcode.io/problems/linked-list-cycle-detection"),
    (42, "Merge Two Sorted Lists",                         "Easy",   "Linked List",               "https://neetcode.io/problems/merge-two-sorted-linked-lists"),
    (43, "Merge K Sorted Lists",                           "Hard",   "Linked List",               "https://neetcode.io/problems/merge-k-sorted-linked-lists"),
    (44, "Remove Nth Node From End of List",               "Medium", "Linked List",               "https://neetcode.io/problems/remove-node-from-end-of-linked-list"),
    (45, "Reorder List",                                   "Medium", "Linked List",               "https://neetcode.io/problems/reorder-linked-list"),

    # ── Matrix ────────────────────────────────────────────────────────────────
    (46, "Set Matrix Zeroes",                              "Medium", "Matrix",                    "https://neetcode.io/problems/set-zeroes-in-matrix"),
    (47, "Spiral Matrix",                                  "Medium", "Matrix",                    "https://neetcode.io/problems/spiral-matrix"),
    (48, "Rotate Image",                                   "Medium", "Matrix",                    "https://neetcode.io/problems/rotate-matrix"),
    (49, "Word Search",                                    "Medium", "Matrix",                    "https://neetcode.io/problems/search-for-word"),

    # ── String ────────────────────────────────────────────────────────────────
    (50, "Longest Substring Without Repeating Characters", "Medium", "String",                    "https://neetcode.io/problems/longest-substring-without-duplicates"),
    (51, "Longest Repeating Character Replacement",        "Medium", "String",                    "https://neetcode.io/problems/longest-repeating-substring-with-replacement"),
    (52, "Minimum Window Substring",                       "Hard",   "String",                    "https://neetcode.io/problems/minimum-window-with-characters"),
    (53, "Valid Anagram",                                  "Easy",   "String",                    "https://neetcode.io/problems/is-anagram"),
    (54, "Group Anagrams",                                 "Medium", "String",                    "https://neetcode.io/problems/anagram-groups"),
    (55, "Valid Parentheses",                              "Easy",   "String",                    "https://neetcode.io/problems/validate-parentheses"),
    (56, "Valid Palindrome",                               "Easy",   "String",                    "https://neetcode.io/problems/is-palindrome"),
    (57, "Longest Palindromic Substring",                  "Medium", "String",                    "https://neetcode.io/problems/longest-palindromic-substring"),
    (58, "Palindromic Substrings",                         "Medium", "String",                    "https://neetcode.io/problems/palindromic-substrings"),
    (59, "Encode and Decode Strings",                      "Medium", "String",                    "https://neetcode.io/problems/string-encode-and-decode"),

    # ── Tree ──────────────────────────────────────────────────────────────────
    (60, "Maximum Depth of Binary Tree",                   "Easy",   "Tree",                      "https://neetcode.io/problems/depth-of-binary-tree"),
    (61, "Same Tree",                                      "Easy",   "Tree",                      "https://neetcode.io/problems/same-binary-tree"),
    (62, "Invert Binary Tree",                             "Easy",   "Tree",                      "https://neetcode.io/problems/invert-a-binary-tree"),
    (63, "Binary Tree Maximum Path Sum",                   "Hard",   "Tree",                      "https://neetcode.io/problems/binary-tree-maximum-path-sum"),
    (64, "Binary Tree Level Order Traversal",              "Medium", "Tree",                      "https://neetcode.io/problems/level-order-traversal-of-binary-tree"),
    (65, "Serialize and Deserialize Binary Tree",          "Hard",   "Tree",                      "https://neetcode.io/problems/serialize-and-deserialize-binary-tree"),
    (66, "Subtree of Another Tree",                        "Easy",   "Tree",                      "https://neetcode.io/problems/subtree-of-a-binary-tree"),
    (67, "Construct Binary Tree from Preorder and Inorder","Medium", "Tree",                      "https://neetcode.io/problems/binary-tree-from-preorder-and-inorder-traversal"),
    (68, "Validate Binary Search Tree",                    "Medium", "Tree",                      "https://neetcode.io/problems/valid-binary-search-tree"),
    (69, "Kth Smallest Element in a BST",                  "Medium", "Tree",                      "https://neetcode.io/problems/kth-smallest-integer-in-bst"),
    (70, "Lowest Common Ancestor of a BST",                "Medium", "Tree",                      "https://neetcode.io/problems/lowest-common-ancestor-in-binary-search-tree"),
    (71, "Implement Trie (Prefix Tree)",                   "Medium", "Tree",                      "https://neetcode.io/problems/implement-prefix-tree"),
    (72, "Design Add and Search Words Data Structure",     "Medium", "Tree",                      "https://neetcode.io/problems/design-word-search-data-structure"),
    (73, "Word Search II",                                 "Hard",   "Tree",                      "https://neetcode.io/problems/search-for-word-ii"),

    # ── Heap ──────────────────────────────────────────────────────────────────
    (74, "Top K Frequent Elements",                        "Medium", "Heap",                      "https://neetcode.io/problems/top-k-elements-in-list"),
    (75, "Find Median from Data Stream",                   "Hard",   "Heap",                      "https://neetcode.io/problems/find-median-in-a-data-stream"),
]

DIFFICULTY_EMOJI = {
    "Easy":   "🟢",
    "Medium": "🟡",
    "Hard":   "🔴",
}

TOPIC_EMOJI = {
    "Arrays":               "🗃️",
    "Binary":               "⚙️",
    "Dynamic Programming":  "📈",
    "Graph":                "🕸️",
    "Interval":             "📏",
    "Linked List":          "🔗",
    "Matrix":               "🔢",
    "String":               "🔤",
    "Tree":                 "🌳",
    "Heap":                 "🏔️",
}
