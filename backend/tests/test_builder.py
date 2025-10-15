import re
import pytest
from src.builder import RegexBuilder


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
        main.lookahead("not_a_builder")
    
    with pytest.raises(TypeError):
        main.negative_lookbehind(123)


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
    b._explanations = ["text", 123, 45.6, None, True, []]
    
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
    test_cases = [
        ({"qty": 3}, r"\d{3}"),
        ({"min_qty": 2, "max_qty": 5}, r"\d{2,5}"),
        ({"min_qty": 1}, r"\d{1,}"),
        ({"max_qty": 4}, r"\d{0,4}"),
        ({"special_quantifier": "+"}, r"\d+"),
        ({"special_quantifier": "*"}, r"\d*"),
        ({"special_quantifier": "?"}, r"\d?"),
    ]
    
    for kwargs, expected_pattern in test_cases:
        b = RegexBuilder().digits(**kwargs)
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
