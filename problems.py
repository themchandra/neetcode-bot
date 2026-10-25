"""
Blind 75 problem list.
Each entry: (id, name, difficulty, topic, leetcode_url)
"""

PROBLEMS = [
    # ── Arrays ────────────────────────────────────────────────────────────────
    (1,  "Two Sum",                                        "Easy",   "Arrays",                    "https://leetcode.com/problems/two-sum/"),
    (2,  "Best Time to Buy and Sell Stock",                "Easy",   "Arrays",                    "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"),
    (3,  "Contains Duplicate",                             "Easy",   "Arrays",                    "https://leetcode.com/problems/contains-duplicate/"),
    (4,  "Product of Array Except Self",                   "Medium", "Arrays",                    "https://leetcode.com/problems/product-of-array-except-self/"),
    (5,  "Maximum Subarray",                               "Medium", "Arrays",                    "https://leetcode.com/problems/maximum-subarray/"),
    (6,  "Maximum Product Subarray",                       "Medium", "Arrays",                    "https://leetcode.com/problems/maximum-product-subarray/"),
    (7,  "Find Minimum in Rotated Sorted Array",           "Medium", "Arrays",                    "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/"),
    (8,  "Search in Rotated Sorted Array",                 "Medium", "Arrays",                    "https://leetcode.com/problems/search-in-rotated-sorted-array/"),
    (9,  "3Sum",                                           "Medium", "Arrays",                    "https://leetcode.com/problems/3sum/"),
    (10, "Container With Most Water",                      "Medium", "Arrays",                    "https://leetcode.com/problems/container-with-most-water/"),

    # ── Binary ────────────────────────────────────────────────────────────────
    (11, "Sum of Two Integers",                            "Medium", "Binary",                    "https://leetcode.com/problems/sum-of-two-integers/"),
    (12, "Number of 1 Bits",                               "Easy",   "Binary",                    "https://leetcode.com/problems/number-of-1-bits/"),
    (13, "Counting Bits",                                  "Easy",   "Binary",                    "https://leetcode.com/problems/counting-bits/"),
    (14, "Missing Number",                                 "Easy",   "Binary",                    "https://leetcode.com/problems/missing-number/"),
    (15, "Reverse Bits",                                   "Easy",   "Binary",                    "https://leetcode.com/problems/reverse-bits/"),

    # ── Dynamic Programming ───────────────────────────────────────────────────
    (16, "Climbing Stairs",                                "Easy",   "Dynamic Programming",       "https://leetcode.com/problems/climbing-stairs/"),
    (17, "Coin Change",                                    "Medium", "Dynamic Programming",       "https://leetcode.com/problems/coin-change/"),
    (18, "Longest Increasing Subsequence",                 "Medium", "Dynamic Programming",       "https://leetcode.com/problems/longest-increasing-subsequence/"),
    (19, "Longest Common Subsequence",                     "Medium", "Dynamic Programming",       "https://leetcode.com/problems/longest-common-subsequence/"),
    (20, "Word Break",                                     "Medium", "Dynamic Programming",       "https://leetcode.com/problems/word-break/"),
    (21, "Combination Sum IV",                             "Medium", "Dynamic Programming",       "https://leetcode.com/problems/combination-sum-iv/"),
    (22, "House Robber",                                   "Medium", "Dynamic Programming",       "https://leetcode.com/problems/house-robber/"),
    (23, "House Robber II",                                "Medium", "Dynamic Programming",       "https://leetcode.com/problems/house-robber-ii/"),
    (24, "Decode Ways",                                    "Medium", "Dynamic Programming",       "https://leetcode.com/problems/decode-ways/"),
    (25, "Unique Paths",                                   "Medium", "Dynamic Programming",       "https://leetcode.com/problems/unique-paths/"),
    (26, "Jump Game",                                      "Medium", "Dynamic Programming",       "https://leetcode.com/problems/jump-game/"),

    # ── Graph ─────────────────────────────────────────────────────────────────
    (27, "Clone Graph",                                    "Medium", "Graph",                     "https://leetcode.com/problems/clone-graph/"),
    (28, "Course Schedule",                                "Medium", "Graph",                     "https://leetcode.com/problems/course-schedule/"),
    (29, "Pacific Atlantic Water Flow",                    "Medium", "Graph",                     "https://leetcode.com/problems/pacific-atlantic-water-flow/"),
    (30, "Number of Islands",                              "Medium", "Graph",                     "https://leetcode.com/problems/number-of-islands/"),
    (31, "Longest Consecutive Sequence",                   "Medium", "Graph",                     "https://leetcode.com/problems/longest-consecutive-sequence/"),
    (32, "Alien Dictionary",                               "Hard",   "Graph",                     "https://leetcode.com/problems/alien-dictionary/"),
    (33, "Graph Valid Tree",                               "Medium", "Graph",                     "https://leetcode.com/problems/graph-valid-tree/"),
    (34, "Number of Connected Components in an Undirected Graph", "Medium", "Graph",             "https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/"),

    # ── Interval ──────────────────────────────────────────────────────────────
    (35, "Insert Interval",                                "Medium", "Interval",                  "https://leetcode.com/problems/insert-interval/"),
    (36, "Merge Intervals",                                "Medium", "Interval",                  "https://leetcode.com/problems/merge-intervals/"),
    (37, "Non-overlapping Intervals",                      "Medium", "Interval",                  "https://leetcode.com/problems/non-overlapping-intervals/"),
    (38, "Meeting Rooms",                                  "Easy",   "Interval",                  "https://leetcode.com/problems/meeting-rooms/"),
    (39, "Meeting Rooms II",                               "Medium", "Interval",                  "https://leetcode.com/problems/meeting-rooms-ii/"),

    # ── Linked List ───────────────────────────────────────────────────────────
    (40, "Reverse Linked List",                            "Easy",   "Linked List",               "https://leetcode.com/problems/reverse-linked-list/"),
    (41, "Linked List Cycle",                              "Easy",   "Linked List",               "https://leetcode.com/problems/linked-list-cycle/"),
    (42, "Merge Two Sorted Lists",                         "Easy",   "Linked List",               "https://leetcode.com/problems/merge-two-sorted-lists/"),
    (43, "Merge K Sorted Lists",                           "Hard",   "Linked List",               "https://leetcode.com/problems/merge-k-sorted-lists/"),
    (44, "Remove Nth Node From End of List",               "Medium", "Linked List",               "https://leetcode.com/problems/remove-nth-node-from-end-of-list/"),
    (45, "Reorder List",                                   "Medium", "Linked List",               "https://leetcode.com/problems/reorder-list/"),

    # ── Matrix ────────────────────────────────────────────────────────────────
    (46, "Set Matrix Zeroes",                              "Medium", "Matrix",                    "https://leetcode.com/problems/set-matrix-zeroes/"),
    (47, "Spiral Matrix",                                  "Medium", "Matrix",                    "https://leetcode.com/problems/spiral-matrix/"),
    (48, "Rotate Image",                                   "Medium", "Matrix",                    "https://leetcode.com/problems/rotate-image/"),
    (49, "Word Search",                                    "Medium", "Matrix",                    "https://leetcode.com/problems/word-search/"),

    # ── String ────────────────────────────────────────────────────────────────
    (50, "Longest Substring Without Repeating Characters", "Medium", "String",                    "https://leetcode.com/problems/longest-substring-without-repeating-characters/"),
    (51, "Longest Repeating Character Replacement",        "Medium", "String",                    "https://leetcode.com/problems/longest-repeating-character-replacement/"),
    (52, "Minimum Window Substring",                       "Hard",   "String",                    "https://leetcode.com/problems/minimum-window-substring/"),
    (53, "Valid Anagram",                                  "Easy",   "String",                    "https://leetcode.com/problems/valid-anagram/"),
    (54, "Group Anagrams",                                 "Medium", "String",                    "https://leetcode.com/problems/group-anagrams/"),
    (55, "Valid Parentheses",                              "Easy",   "String",                    "https://leetcode.com/problems/valid-parentheses/"),
    (56, "Valid Palindrome",                               "Easy",   "String",                    "https://leetcode.com/problems/valid-palindrome/"),
    (57, "Longest Palindromic Substring",                  "Medium", "String",                    "https://leetcode.com/problems/longest-palindromic-substring/"),
    (58, "Palindromic Substrings",                         "Medium", "String",                    "https://leetcode.com/problems/palindromic-substrings/"),
    (59, "Encode and Decode Strings",                      "Medium", "String",                    "https://leetcode.com/problems/encode-and-decode-strings/"),

    # ── Tree ──────────────────────────────────────────────────────────────────
    (60, "Maximum Depth of Binary Tree",                   "Easy",   "Tree",                      "https://leetcode.com/problems/maximum-depth-of-binary-tree/"),
    (61, "Same Tree",                                      "Easy",   "Tree",                      "https://leetcode.com/problems/same-tree/"),
    (62, "Invert Binary Tree",                             "Easy",   "Tree",                      "https://leetcode.com/problems/invert-binary-tree/"),
    (63, "Binary Tree Maximum Path Sum",                   "Hard",   "Tree",                      "https://leetcode.com/problems/binary-tree-maximum-path-sum/"),
    (64, "Binary Tree Level Order Traversal",              "Medium", "Tree",                      "https://leetcode.com/problems/binary-tree-level-order-traversal/"),
    (65, "Serialize and Deserialize Binary Tree",          "Hard",   "Tree",                      "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/"),
    (66, "Subtree of Another Tree",                        "Easy",   "Tree",                      "https://leetcode.com/problems/subtree-of-another-tree/"),
    (67, "Construct Binary Tree from Preorder and Inorder","Medium", "Tree",                      "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/"),
    (68, "Validate Binary Search Tree",                    "Medium", "Tree",                      "https://leetcode.com/problems/validate-binary-search-tree/"),
    (69, "Kth Smallest Element in a BST",                  "Medium", "Tree",                      "https://leetcode.com/problems/kth-smallest-element-in-a-bst/"),
    (70, "Lowest Common Ancestor of a BST",                "Medium", "Tree",                      "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/"),
    (71, "Implement Trie (Prefix Tree)",                   "Medium", "Tree",                      "https://leetcode.com/problems/implement-trie-prefix-tree/"),
    (72, "Design Add and Search Words Data Structure",     "Medium", "Tree",                      "https://leetcode.com/problems/design-add-and-search-words-data-structure/"),
    (73, "Word Search II",                                 "Hard",   "Tree",                      "https://leetcode.com/problems/word-search-ii/"),

    # ── Heap ──────────────────────────────────────────────────────────────────
    (74, "Top K Frequent Elements",                        "Medium", "Heap",                      "https://leetcode.com/problems/top-k-frequent-elements/"),
    (75, "Find Median from Data Stream",                   "Hard",   "Heap",                      "https://leetcode.com/problems/find-median-from-data-stream/"),
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
