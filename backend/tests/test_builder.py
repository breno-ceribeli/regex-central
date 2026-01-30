import re

import pytest

from builder import RegexBuilder


def test_quantifier_exact_and_plural_explanation():
    b = RegexBuilder()
    b.digits(qty=3)
    assert b.build() == r"\d{3}"
    expl = b.explain()
    assert any("3" in e for e in expl)


def test_special_quantifier_and_invalid_combo():
    b = RegexBuilder()
    with pytest.raises(ValueError):
        b.digits(qty=2, special_quantifier='+')


def test_literal_grouping_and_capturing_behavior():
    b = RegexBuilder().literal("ab", qty=2, capturing=False)
    assert "(?:ab){2}" in b.build()

    b2 = RegexBuilder().literal("ab", qty=2, capturing=True)
    assert "(ab){2}" in b2.build()


def test_start_and_end_anchors_multiline_and_text():
    assert RegexBuilder().start_anchor(multiline=True).build() == "^"
    assert RegexBuilder().start_anchor(multiline=False).build() == r"\A"
    assert RegexBuilder().end_anchor(multiline=True).build() == "$"
    assert RegexBuilder().end_anchor(multiline=False).build() == r"\Z"


def test_flags_combination_in_compile():
    b = RegexBuilder()
    b.enable_multiline(True).enable_ignorecase(True)
    # Add a trivial token so build() is not empty
    b.digits(1)
    compiled = b.compile()
    assert bool(compiled.flags & re.MULTILINE)
    assert bool(compiled.flags & re.IGNORECASE)


def test_lookaround_pattern_and_explanation_string():
    sub = RegexBuilder().digits(3)
    main = RegexBuilder().lookahead(sub)
    assert main.build() == r"(?=\d{3})"
    expl = main.explain()
    # explanation should contain a readable explanation for the lookahead
    assert any(isinstance(x, str) for x in expl)
    assert any("3" in x for x in expl)


def test_quantifier_edge_cases_errors():
    b = RegexBuilder()
    with pytest.raises(ValueError):
        b.digits(qty=0)
    with pytest.raises(ValueError):
        b.digits(min_qty=3, max_qty=2)


def test_word_and_non_word_and_whitespace_tokens():
    b = RegexBuilder().word_chars(qty=2).non_word_chars(special_quantifier='+').whitespace_chars(qty=3)
    assert r"\w{2}" in b.build()
    assert r"\W+" in b.build()
    assert r"\s{3}" in b.build()


def test_lookaround_fallback_to_subpattern():
    # Test fallback when sub-builder has empty explanations
    sub = RegexBuilder().digits(2)
    sub._explanations = []  # Force empty explanations
    main = RegexBuilder().lookahead(sub)
    
    assert main.build() == r"(?=\d{2})"
    expl = main.explain()
    # Should fallback to subpattern when no explanation items
    assert any(r"\d{2}" in str(e) for e in expl)


def test_process_lookaround_type_error():
    # Test TypeError when passing non-RegexBuilder to lookaround methods
    main = RegexBuilder()
    with pytest.raises(TypeError):
        main.lookahead("not_a_builder")  # type: ignore[arg-type]
    
    with pytest.raises(TypeError):
        main.negative_lookbehind(123)  # type: ignore[arg-type]


def test_literal_special_characters_escaping():
    b = RegexBuilder().literal("test.*+?[]{}()^$|\\")
    pattern = b.build()
    # Should escape all special regex characters
    assert "test\\.\\*\\+\\?" in pattern and "\\[\\]\\{\\}" in pattern


def test_chaining_composition_and_explanations():
    chain = (RegexBuilder()
             .start_anchor(multiline=False)
             .literal("hello", qty=2)
             .digits(min_qty=2, max_qty=4)
             .end_anchor(multiline=True))
    
    pattern = chain.build()
    assert r"\A" in pattern
    assert "hello" in pattern
    assert r"\d{2,4}" in pattern
    assert "$" in pattern
    
    explanations = chain.explain()
    assert len(explanations) >= 4  # Should have explanation for each part
    # All should be strings (guaranteed by explain())
    assert all(isinstance(e, str) for e in explanations)


def test_explain_always_returns_strings():
    b = RegexBuilder()
    # Manually insert non-string items to test robustness
    b._explanations = ["text", 123, 45.6, None, True, []]  # type: ignore[list-item]
    
    explanations = b.explain()
    # All items should be converted to strings
    assert all(isinstance(e, str) for e in explanations)
    assert "123" in explanations
    assert "45.6" in explanations
    assert "None" in explanations
    assert "True" in explanations
    assert "[]" in explanations


def test_parametrized_quantifiers():
    # Test various quantifier combinations
    test_cases: list[tuple[dict[str, int | str], str]] = [
        ({"qty": 3}, r"\d{3}"),
        ({"min_qty": 2, "max_qty": 5}, r"\d{2,5}"),
        ({"min_qty": 1}, r"\d{1,}"),
        ({"max_qty": 4}, r"\d{0,4}"),
        ({"special_quantifier": "+"}, r"\d+"),
        ({"special_quantifier": "*"}, r"\d*"),
        ({"special_quantifier": "?"}, r"\d?"),
    ]
    
    for kwargs, expected_pattern in test_cases:
        b = RegexBuilder().digits(**kwargs)  # type: ignore[arg-type]
        assert expected_pattern in b.build()


def test_group_nesting_and_quantifiers():
    b = (RegexBuilder()
         .start_group(capturing=True)
         .literal("abc")
         .end_group(qty=2)
         .start_group(capturing=False)
         .digits(special_quantifier="+")
         .end_group(special_quantifier="?"))
    
    pattern = b.build()
    assert "(abc){2}" in pattern
    assert r"(?:\d+)?" in pattern

def test_named_group_behavior():
    # Test valid named group
    b = RegexBuilder()
    b.start_group(name="year_group")
    b.digits(4)
    b.end_group()
    pattern = b.build()
    
    # Verify the pattern syntax
    assert pattern == r"(?P<year_group>\d{4})"
    
    # Verify explanation contains the group name
    explanation = b.explain()
    assert any("Start of named group 'year_group'" in exc for exc in explanation)

    # Test execution with re module
    match = re.search(pattern, "2023")
    assert match is not None
    # Verify capture by name
    assert match.group("year_group") == "2023"

    # Test invalid named group (starts with digit)
    b_invalid = RegexBuilder()
    with pytest.raises(ValueError, match="Invalid group name"):
        # invalid identifier
        b_invalid.start_group(name="1st_group")
        
    # Test invalid named group (contains hyphen)
    with pytest.raises(ValueError, match="Invalid group name"):
        b_invalid.start_group(name="invalid-name")

    # Test that named group is implicitly capturing
    b_mixed = RegexBuilder()
    b_mixed.start_group(capturing=False, name="forced_capture")
    b_mixed.digits(1)
    b_mixed.end_group()
    assert b_mixed.build() == r"(?P<forced_capture>\d)"

def test_negative_lookarounds():
    sub = RegexBuilder().literal("test")
    main = RegexBuilder().negative_lookahead(sub).negative_lookbehind(sub)
    
    pattern = main.build()
    assert "(?!test)" in pattern
    assert "(?<!test)" in pattern
    
    explanations = main.explain()
    assert any("not followed by" in str(e) for e in explanations)
    assert any("not preceded by" in str(e) for e in explanations)


def test_boundary_anchors():
    b = RegexBuilder().word_boundary().literal("word").non_word_boundary()
    
    pattern = b.build()
    assert r"\b" in pattern
    assert "word" in pattern
    assert r"\B" in pattern
    
    explanations = b.explain()
    assert any("boundary" in str(e).lower() for e in explanations)


# =====================================================
# CHARACTER CLASSES TESTS
# =====================================================

def test_char_class_basic():
    """Test basic character class functionality"""
    b = RegexBuilder()
    b.char_class("abc")
    
    pattern = b.build()
    assert pattern == "[abc]"
    
    explanations = b.explain()
    assert len(explanations) == 1
    assert "Any character in 'abc'" in explanations[0]


def test_char_class_with_quantifiers():
    """Test character class with various quantifiers"""
    # Exact quantity
    b1 = RegexBuilder()
    b1.char_class("aeiou", qty=3)
    assert b1.build() == "[aeiou]{3}"
    assert "Exactly 3 characters" in b1.explain()[0]
    
    # Range quantity
    b2 = RegexBuilder()
    b2.char_class("xyz", min_qty=2, max_qty=5)
    assert b2.build() == "[xyz]{2,5}"
    assert "Between 2 and 5 characters" in b2.explain()[0]
    
    # Min quantity
    b3 = RegexBuilder()
    b3.char_class("123", min_qty=1)
    assert b3.build() == "[123]{1,}"
    assert "At least 1 character" in b3.explain()[0]
    
    # Max quantity
    b4 = RegexBuilder()
    b4.char_class("abc", max_qty=4)
    assert b4.build() == "[abc]{0,4}"
    assert "Up to 4 characters" in b4.explain()[0]
    
    # Special quantifiers
    b5 = RegexBuilder()
    b5.char_class("test", special_quantifier="+")
    assert b5.build() == "[test]+"
    assert "One or more characters" in b5.explain()[0]
    
    b6 = RegexBuilder()
    b6.char_class("opt", special_quantifier="*")
    assert b6.build() == "[opt]*"
    assert "Zero or more characters" in b6.explain()[0]
    
    b7 = RegexBuilder()
    b7.char_class("maybe", special_quantifier="?")
    assert b7.build() == "[maybe]?"
    assert "Zero or one character" in b7.explain()[0]


def test_char_class_negated():
    """Test negated character classes"""
    b = RegexBuilder()
    b.char_class("aeiou", negated=True)
    
    pattern = b.build()
    assert pattern == "[^aeiou]"
    
    explanations = b.explain()
    assert "Any character NOT in 'aeiou'" in explanations[0]


def test_char_class_negated_with_quantifiers():
    """Test negated character classes with quantifiers"""
    b1 = RegexBuilder()
    b1.char_class("abc", negated=True, qty=2)
    assert b1.build() == "[^abc]{2}"
    assert "Exactly 2 characters" in b1.explain()[0]
    assert "NOT in 'abc'" in b1.explain()[0]
    
    b2 = RegexBuilder()
    b2.char_class("xyz", negated=True, special_quantifier="+")
    assert b2.build() == "[^xyz]+"
    assert "One or more characters" in b2.explain()[0]
    assert "NOT in 'xyz'" in b2.explain()[0]


def test_any_char_basic_and_quantified():
    """Test the any_char (.) method functionality"""
    # Basic usage
    b1 = RegexBuilder()
    b1.any_char()
    assert b1.build() == "."
    assert "Exactly 1 character" in b1.explain()[0] # Default quantity is 1

    # With quantifier
    b2 = RegexBuilder()
    b2.any_char(qty=3)
    assert b2.build() == ".{3}"
    assert "Exactly 3 characters" in b2.explain()[0]

    # With special quantifier
    b3 = RegexBuilder()
    b3.any_char(special_quantifier="*")
    assert b3.build() == ".*"
    assert "Zero or more characters" in b3.explain()[0]


def test_any_char_compile_and_match():
    """Test that any_char generates valid regex that matches correctly"""
    # Should match anything
    b = RegexBuilder().any_char(special_quantifier="+")
    compiled = b.compile()
    
    assert compiled.match("abc-123")
    assert compiled.match("!@#")
    
    # By default, dot does usually (depending on engine) match newlines only with DOTALL.
    # Python's re matches everything EXCEPT newline by default.
    assert compiled.match("line")
    
    # Test with DOTALL
    b_dotall = RegexBuilder().enable_dotall().any_char(special_quantifier="+")
    compiled_dotall = b_dotall.compile()
    
    matching_newline = compiled_dotall.match("line1\nline2")
    assert matching_newline is not None
    # \n is matched
    assert matching_newline.group(0) == "line1\nline2"


def test_alternation_basic_strings():
    """Test alternation with simple string literals"""
    b = RegexBuilder()
    b.alternation(["cat", "dog", "bird"])
    
    pattern = b.build()
    # Should create non-capturing group with pipes
    assert pattern == "(?:cat|dog|bird)"
    
    expl = b.explain()[0]
    assert 'Match either "cat" OR "dog" OR "bird"' in expl


def test_alternation_mixed_types():
    """Test alternation mixing strings and RegexBuilder instances"""
    # Create a sub-builder for digits
    digits_part = RegexBuilder().digits(3)
    
    b = RegexBuilder()
    b.alternation(["id_", digits_part, "code"])
    
    pattern = b.build()
    # Strings are escaped, builder pattern is inserted directly
    # \d{3} comes from digits_part
    assert pattern == r"(?:id_|\d{3}|code)"
    
    expl = b.explain()[0]
    # Check that explanation contains parts from all sources
    assert '"id_"' in expl
    assert '"code"' in expl
    assert "Exactly 3 digits" in expl


def test_alternation_special_chars_escaping():
    """Test that special characters in string parts are escaped"""
    b = RegexBuilder()
    # These contain regex special chars that must be escaped
    b.alternation(["(a)", "b.c", "d|e"])
    
    pattern = b.build()
    # Should overlap with expected escaped version
    # (a) -> \(a\)
    # b.c -> b\.c
    # d|e -> d\|e
    assert r"\(a\)" in pattern
    assert r"b\.c" in pattern
    assert r"d\|e" in pattern
    assert pattern == r"(?:\(a\)|b\.c|d\|e)"


def test_alternation_with_quantifiers_and_capturing():
    """Test alternation with quantifiers and capturing mode"""
    # Capturing = True
    b1 = RegexBuilder()
    b1.alternation(["a", "b"], capturing=True)
    assert b1.build() == "(a|b)"  # Capturing group
    
    # With quantifier
    b2 = RegexBuilder()
    b2.alternation(["a", "b"], qty=3)
    assert b2.build() == "(?:a|b){3}"
    assert "Exactly 3 alternation groups" in b2.explain()[0]
    
    # With special quantifier
    b3 = RegexBuilder()
    b3.alternation(["a", "b"], special_quantifier="+")
    assert b3.build() == "(?:a|b)+"


def test_alternation_validation():
    """Test error handling for alternation"""
    # Empty list
    with pytest.raises(ValueError, match="Alternation parts cannot be empty"):
        RegexBuilder().alternation([])
        
    # Invalid type
    with pytest.raises(TypeError):
        RegexBuilder().alternation(["ok", 123])  # type: ignore


def test_alternation_real_world():
    """Test a realistic usage of alternation"""
    # Matches common image extensions: .jpg OR .png OR .gif
    
    # Correct logic: flags are applied to the builder instance
    b = (RegexBuilder()
         .enable_ignorecase()
         .literal(".")
         .alternation(["jpg", "png", "gif"]))
         
    pattern = b.build()
    compiled = b.compile()
    
    assert pattern == r"\.(?:jpg|png|gif)"
    assert compiled.match(".jpg")
    assert compiled.match(".PNG") # IgnoreCase
    assert compiled.match(".Gif")
    assert not compiled.match(".bmp")


def test_char_class_special_characters():
    """Test character class with special regex characters"""
    # Characters that need escaping inside character class
    b1 = RegexBuilder()
    b1.char_class("]-^")
    pattern1 = b1.build()
    assert pattern1 == r"[\]\-^]"  # ] and - should be escaped, ^ shouldn't at end
    
    # Dash in various positions
    b2 = RegexBuilder()
    b2.char_class("-abc")  # Dash at beginning
    assert b2.build() == "[-abc]"
    
    b3 = RegexBuilder()
    b3.char_class("abc-")  # Dash at end
    assert b3.build() == "[abc-]"
    
    # Various punctuation
    b4 = RegexBuilder()
    b4.char_class(".,;!?")
    assert b4.build() == "[.,;!?]"
    
    explanations1 = b1.explain()
    assert len(explanations1) == 1
    # Check that explanation contains the characters (order may vary)
    assert "Any character in '" in explanations1[0] 
    assert "'" in explanations1[0] and "]" in explanations1[0] and "^" in explanations1[0]
    
    explanations2 = b2.explain()
    # Check that explanation contains the characters (order may vary)
    assert "Any character in '" in explanations2[0]
    assert "-" in explanations2[0] and "a" in explanations2[0] and "b" in explanations2[0] and "c" in explanations2[0]
    
    explanations3 = b3.explain()
    # Check that explanation contains the characters (order may vary)  
    assert "Any character in '" in explanations3[0]
    assert "a" in explanations3[0] and "b" in explanations3[0] and "c" in explanations3[0] and "-" in explanations3[0]
    
    explanations4 = b4.explain()
    # Check that explanation contains the characters (order may vary)
    assert "Any character in '" in explanations4[0]
    assert "." in explanations4[0] and "," in explanations4[0] and ";" in explanations4[0] and "!" in explanations4[0] and "?" in explanations4[0]


def test_char_range_basic():
    """Test basic character range functionality"""
    # Letter range
    b1 = RegexBuilder()
    b1.char_range("a", "z")
    assert b1.build() == "[a-z]"
    assert "Any character in range 'a' to 'z'" in b1.explain()[0]
    
    # Digit range
    b2 = RegexBuilder()
    b2.char_range("0", "9")
    assert b2.build() == "[0-9]"
    assert "Any character in range '0' to '9'" in b2.explain()[0]
    
    # Uppercase range
    b3 = RegexBuilder()
    b3.char_range("A", "Z")
    assert b3.build() == "[A-Z]"
    assert "Any character in range 'A' to 'Z'" in b3.explain()[0]


def test_char_range_partial():
    """Test partial character ranges"""
    # Partial digit ranges
    b1 = RegexBuilder()
    b1.char_range("0", "5")
    assert b1.build() == "[0-5]"
    
    b2 = RegexBuilder()
    b2.char_range("3", "7")
    assert b2.build() == "[3-7]"
    
    # Partial letter ranges
    b3 = RegexBuilder()
    b3.char_range("a", "g")
    assert b3.build() == "[a-g]"
    
    b4 = RegexBuilder()
    b4.char_range("M", "P")
    assert b4.build() == "[M-P]"
    
    explanations1 = b1.explain()
    assert "Any character in range '0' to '5'" in explanations1[0]
    
    explanations2 = b2.explain()
    assert "Any character in range '3' to '7'" in explanations2[0]
    
    explanations3 = b3.explain()
    assert "Any character in range 'a' to 'g'" in explanations3[0]
    
    explanations4 = b4.explain()
    assert "Any character in range 'M' to 'P'" in explanations4[0]


def test_char_range_with_quantifiers():
    """Test character range with quantifiers"""
    b1 = RegexBuilder()
    b1.char_range("0", "9", qty=3)
    assert b1.build() == "[0-9]{3}"
    
    b2 = RegexBuilder()
    b2.char_range("a", "z", special_quantifier="+")
    assert b2.build() == "[a-z]+"
    
    b3 = RegexBuilder()
    b3.char_range("A", "Z", min_qty=2, max_qty=4)
    assert b3.build() == "[A-Z]{2,4}"
    
    explanations1 = b1.explain()
    assert "Exactly 3 characters" in explanations1[0]
    assert "Any character in range '0' to '9'" in explanations1[0]
    
    explanations2 = b2.explain()
    assert "One or more characters" in explanations2[0]
    assert "Any character in range 'a' to 'z'" in explanations2[0]
    
    explanations3 = b3.explain()
    assert "Between 2 and 4 characters" in explanations3[0]
    assert "Any character in range 'A' to 'Z'" in explanations3[0]


def test_char_range_negated():
    """Test negated character ranges"""
    b1 = RegexBuilder()
    b1.char_range("0", "9", negated=True)
    assert b1.build() == "[^0-9]"
    assert "Any character NOT in range '0' to '9'" in b1.explain()[0]
    
    b2 = RegexBuilder()
    b2.char_range("a", "z", negated=True, special_quantifier="*")
    assert b2.build() == "[^a-z]*"
    assert "Any character NOT in range 'a' to 'z'" in b2.explain()[0]


def test_char_ranges_multiple():
    """Test multiple character ranges"""
    # Basic multiple ranges
    b1 = RegexBuilder()
    b1.char_ranges([("a", "z"), ("A", "Z")])
    assert b1.build() == "[a-zA-Z]"
    assert "Any character in ranges: 'a'-'z', 'A'-'Z'" in b1.explain()[0]
    
    # Alphanumeric
    b2 = RegexBuilder()
    b2.char_ranges([("a", "z"), ("A", "Z"), ("0", "9")])
    assert b2.build() == "[a-zA-Z0-9]"
    assert "'a'-'z', 'A'-'Z', '0'-'9'" in b2.explain()[0]


def test_char_ranges_with_quantifiers():
    """Test multiple ranges with quantifiers"""
    b1 = RegexBuilder()
    b1.char_ranges([("a", "z"), ("0", "9")], qty=5)
    assert b1.build() == "[a-z0-9]{5}"
    
    b2 = RegexBuilder()
    b2.char_ranges([("A", "Z"), ("0", "9")], special_quantifier="+")
    assert b2.build() == "[A-Z0-9]+"
    
    explanations1 = b1.explain()
    assert "Exactly 5 characters" in explanations1[0]
    assert "Any character in ranges: 'a'-'z', '0'-'9'" in explanations1[0]
    
    explanations2 = b2.explain()
    assert "One or more characters" in explanations2[0]
    assert "Any character in ranges: 'A'-'Z', '0'-'9'" in explanations2[0]


def test_char_ranges_negated():
    """Test negated multiple ranges"""
    b = RegexBuilder()
    b.char_ranges([("a", "z"), ("A", "Z")], negated=True)
    assert b.build() == "[^a-zA-Z]"
    assert "Any character NOT in ranges" in b.explain()[0]


def test_char_class_mixed():
    """Test mixed character class with chars, ranges, and escape sequences"""
    # Basic mixed
    b1 = RegexBuilder()
    b1.char_class_mixed(
        chars="aeiou",
        ranges=[("0", "9")],
        escape_sequences=[r"\s"]
    )
    assert b1.build() == "[aeiou0-9\\s]"
    assert "characters 'aeiou'" in b1.explain()[0]
    assert "ranges '0'-'9'" in b1.explain()[0]
    assert "escape sequences \\s" in b1.explain()[0]
    
    # Complex mixed
    b2 = RegexBuilder()
    b2.char_class_mixed(
        chars="._-",
        ranges=[("a", "z"), ("A", "Z"), ("0", "9")],
        escape_sequences=[r"\w", r"\d"]
    )
    pattern2 = b2.build()
    assert "._\\-" in pattern2
    assert "a-z" in pattern2
    assert "A-Z" in pattern2
    assert "0-9" in pattern2
    assert r"\w" in pattern2
    assert r"\d" in pattern2
    
    explanations2 = b2.explain()
    assert "characters '" in explanations2[0]
    assert "ranges 'a'-'z', 'A'-'Z', '0'-'9'" in explanations2[0]
    assert "escape sequences \\w, \\d" in explanations2[0]


def test_char_class_mixed_negated():
    """Test negated mixed character class"""
    b = RegexBuilder()
    b.char_class_mixed(
        chars="xyz",
        ranges=[("0", "2")],
        negated=True
    )
    assert b.build() == "[^xyz0-2]"
    assert "Any character NOT matching" in b.explain()[0]


def test_char_class_mixed_with_quantifiers():
    """Test mixed character class with quantifiers"""
    b1 = RegexBuilder()
    b1.char_class_mixed(
        chars="!@#",
        ranges=[("a", "z")],
        qty=3
    )
    assert b1.build() == "[!@#a-z]{3}"
    
    b2 = RegexBuilder()
    b2.char_class_mixed(
        ranges=[("0", "9"), ("A", "F")],
        special_quantifier="+"
    )
    assert b2.build() == "[0-9A-F]+"

    explanations1 = b1.explain()
    assert "Exactly 3 characters" in explanations1[0]
    # Check that explanation contains the characters and ranges (order may vary)
    assert "Any character matching: characters '" in explanations1[0]
    assert "!, @, #" in explanations1[0] or ("!" in explanations1[0] and "@" in explanations1[0] and "#" in explanations1[0])
    assert "ranges 'a'-'z'" in explanations1[0]
    
    explanations2 = b2.explain()
    assert "One or more characters" in explanations2[0]
    assert "Any character matching: ranges '0'-'9', 'A'-'F'" in explanations2[0]


def test_char_class_empty_validation():
    """Test validation for empty character classes"""
    with pytest.raises(ValueError, match="Character class cannot be empty"):
        RegexBuilder().char_class("")
    
    with pytest.raises(ValueError, match="Character class cannot be empty"):
        RegexBuilder().char_class_mixed()


def test_char_range_validation():
    """Test validation for character ranges"""
    # Invalid range order
    with pytest.raises(ValueError, match="Invalid range 'z-a'"):
        RegexBuilder().char_range("z", "a")
    
    # Multiple characters
    with pytest.raises(ValueError, match="Range start must be a single character"):
        RegexBuilder().char_range("ab", "z")
    
    with pytest.raises(ValueError, match="Range end must be a single character"):
        RegexBuilder().char_range("a", "yz")
    
    # Empty strings
    with pytest.raises(ValueError, match="Range start must be a single character"):
        RegexBuilder().char_range("", "z")
    
    with pytest.raises(ValueError, match="Range end must be a single character"):
        RegexBuilder().char_range("a", "")


def test_char_ranges_validation():
    """Test validation for multiple ranges"""
    # Empty ranges list
    with pytest.raises(ValueError, match="Ranges list cannot be empty"):
        RegexBuilder().char_ranges([])
    
    # Invalid range in list
    with pytest.raises(ValueError, match="Invalid range 'z-a'"):
        RegexBuilder().char_ranges([("a", "m"), ("z", "a")])


def test_escape_sequences_validation():
    """Test validation for escape sequences"""
    valid_sequences = [r"\d", r"\D", r"\w", r"\W", r"\s", r"\S", r"\t", r"\n", r"\r", r"\f", r"\v"]
    
    # Test all valid sequences
    for seq in valid_sequences:
        b = RegexBuilder()
        b.char_class_mixed(escape_sequences=[seq])
        pattern = b.build()
        assert seq in pattern
    
    # Test invalid sequences
    invalid_sequences = [r"\x", r"\z", r"\p", r"\q", "d", "\\d\\w"]
    
    for seq in invalid_sequences:
        with pytest.raises(ValueError, match="Invalid escape sequence"):
            RegexBuilder().char_class_mixed(escape_sequences=[seq])


def test_quantifier_conflicts():
    """Test validation for quantifier conflicts"""
    # Cannot mix special quantifier with numeric quantifiers
    with pytest.raises(ValueError, match="Cannot use special quantifier along with quantity values"):
        RegexBuilder().char_class("abc", qty=2, special_quantifier="+")
    
    with pytest.raises(ValueError, match="Cannot use special quantifier along with quantity values"):
        RegexBuilder().char_range("a", "z", min_qty=1, special_quantifier="*")


def test_character_class_method_chaining():
    """Test method chaining with character classes"""
    # Basic chaining
    b1 = (RegexBuilder()
          .start_anchor()
          .char_range("A", "Z")
          .char_class("aeiou", special_quantifier="+")
          .char_range("0", "9", qty=3)
          .end_anchor())
    
    pattern1 = b1.build()
    assert pattern1 == r"\A[A-Z][aeiou]+[0-9]{3}\Z"
    
    # Complex chaining
    b2 = (RegexBuilder()
          .word_boundary()
          .char_ranges([("a", "z"), ("A", "Z")], special_quantifier="+")
          .char_class("._-", special_quantifier="?")
          .char_range("0", "9", min_qty=1, max_qty=3)
          .word_boundary())
    
    pattern2 = b2.build()
    assert r"\b" in pattern2
    assert "[a-zA-Z]+" in pattern2
    assert "[._-]?" in pattern2
    assert "[0-9]{1,3}" in pattern2


def test_character_class_compilation():
    """Test that character classes compile correctly"""
    # Test various patterns actually work with re.compile
    test_cases = [
        RegexBuilder().char_class("aeiou"),
        RegexBuilder().char_range("0", "9"),
        RegexBuilder().char_ranges([("a", "z"), ("A", "Z")]),
        RegexBuilder().char_class_mixed(chars="!@#", ranges=[("0", "9")]),
        RegexBuilder().char_class("abc", negated=True),
        RegexBuilder().char_range("a", "z", special_quantifier="+"),
    ]
    
    for builder in test_cases:
        compiled = builder.compile()
        
        # Should compile without error
        assert compiled is not None
        assert hasattr(compiled, 'match')
        assert hasattr(compiled, 'search')


def test_character_class_real_world_patterns():
    """Test character classes in real-world scenarios"""
    # Email-like pattern
    email_builder = (RegexBuilder()
                    .char_ranges([("a", "z"), ("A", "Z"), ("0", "9")], special_quantifier="+")
                    .char_class("._-", special_quantifier="*")
                    .literal("@")
                    .char_ranges([("a", "z"), ("A", "Z"), ("0", "9")], special_quantifier="+")
                    .literal(".")
                    .char_range("a", "z", min_qty=2, max_qty=4))
    
    email_regex = email_builder.compile()
    
    # Should match valid emails
    assert email_regex.match("user@domain.com")
    assert email_regex.match("test123@site.org")
    
    # Should not match invalid emails
    assert not email_regex.match("@invalid.com")
    assert not email_regex.match("user@.com")
    
    # Hexadecimal color
    hex_builder = (RegexBuilder()
                  .literal("#")
                  .char_ranges([("0", "9"), ("a", "f"), ("A", "F")], qty=6))
    
    hex_regex = hex_builder.compile()
    
    assert hex_regex.match("#FF0000")
    assert hex_regex.match("#00ff00")
    assert hex_regex.match("#123ABC")
    assert not hex_regex.match("#GG0000")
    assert not hex_regex.match("#FF00")
    
        # Username pattern  
    username_builder = (RegexBuilder()
                           .start_anchor()
                           .char_range("a", "z")  # Must start with lowercase
                           .char_ranges([("a", "z"), ("0", "9")], min_qty=2, max_qty=15)
                           .end_anchor())
        
    username_regex = username_builder.compile()
        
    assert username_regex.match("user123")
    assert username_regex.match("testuser") 
    assert username_regex.match("abc123")
    assert not username_regex.match("123user")  # Starts with number
    assert not username_regex.match("User")     # Starts with uppercase
    assert not username_regex.match("a")        # Too short


def test_character_class_warnings():
    """Test warnings for character classes"""
    import warnings
    
    # Test cross-type range warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should generate warnings for cross-type range
        RegexBuilder().char_range("9", "A")
        
        # Check that warnings were generated
        assert len(w) >= 1
        warning_messages = [str(warning.message) for warning in w]
        assert any("crosses character types" in msg for msg in warning_messages)
    
    # Test non-ASCII character warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # This should generate warning for non-ASCII characters
        RegexBuilder().char_class("áéíóú")
        
        # Check that warning was generated
        assert len(w) >= 1
        warning_messages = [str(warning.message) for warning in w]
        assert any("Non-ASCII characters detected" in msg for msg in warning_messages)


def test_character_class_edge_cases():
    """Test edge cases for character classes"""
    # Single character
    b1 = RegexBuilder().char_class("x")
    assert b1.build() == "[x]"
    
    # Same start and end range
    b2 = RegexBuilder().char_range("a", "a")
    assert b2.build() == "[a-a]"
    
    # Large character set
    large_chars = "".join(chr(i) for i in range(33, 127))  # Printable ASCII
    b3 = RegexBuilder().char_class(large_chars)
    pattern3 = b3.build()
    assert pattern3.startswith("[")
    assert pattern3.endswith("]")
    
    # Mixed with empty components
    b4 = RegexBuilder().char_class_mixed(
        chars="abc",
        ranges=[],
        escape_sequences=[]
    )
    assert b4.build() == "[abc]"


def test_unclosed_group_validation():
    """Test validation for unclosed groups during build."""
    b = RegexBuilder()
    b.start_group()
    b.digits(3)
    # Missing end_group()
    
    with pytest.raises(ValueError, match="Unclosed group"):
        b.build()


def test_extra_end_group_validation():
    """Test validation for closing a group when no group is open."""
    b = RegexBuilder()
    b.start_group()
    b.end_group()
    
    with pytest.raises(ValueError, match="No open group to close"):
        b.end_group()
