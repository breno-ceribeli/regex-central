import re

class RegexBuilder:
    # Mapping of `re` module flags to a human-readable name and description.
    # Used to display flag information in the interface and generate documentation.
    FLAG_INFO = {
        re.MULTILINE: ("MULTILINE", "Makes ^ and $ match the start and end of each line."),
        re.IGNORECASE: ("IGNORECASE", "Enables case-insensitive matching."),
        re.DOTALL: ("DOTALL", "Makes dot (.) match newline characters as well.")
    }

    def __init__(self):
        self._pattern_parts = []
        self._explanations = []
        self._flags = set()

    def start_anchor(self, multiline: bool = False):
        """
        Adds a start-of-line or start-of-text anchor to the regex pattern.

        Args:
            multiline (bool, optional): 
                If True, uses '^' to match the beginning of each line 
                (when re.MULTILINE is enabled).
                If False (default), uses '\\A' to match only the start 
                of the entire input string.

        Returns:
            self: Enables method chaining.
        """

        anchor, explanation = ("^", "Start of line") if multiline else (r"\A", "Start of text")
        self._pattern_parts.append(anchor)
        self._explanations.append(explanation)
        return self
    
    def digits(
        self,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a digit-matching pattern (`\\d`) to the current regex expression.

        Supports exact quantities (e.g., `{3}`), ranged quantities (e.g., `{2,5}`),
        and special quantifiers (`+`, `*`, `?`) to define how many digits should be matched.

        Args:
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            Self: Enables method chaining.
        """

        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=("digit", "digits")
        )

        self._pattern_parts.append(r"\d" + quantifier)
        self._explanations.append(explanation)
        return self

    def non_digits(
        self,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a non-digit-matching pattern (`\\D`) to the current regex expression.

        Supports exact quantities (e.g., `{3}`), ranged quantities (e.g., `{2,5}`),
        and special quantifiers (`+`, `*`, `?`) to define how many non-digit characters should be matched.

        Args:
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            Self: Enables method chaining.
        """

        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=("non-digit character", "non-digit characters")
        )

        self._pattern_parts.append(r"\D" + quantifier)
        self._explanations.append(explanation)
        return self

    def word_chars(
        self,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a word character-matching pattern (`\\w`) to the current regex expression.

        Supports exact quantities (e.g., `{3}`), ranged quantities (e.g., `{2,5}`),
        and special quantifiers (`+`, `*`, `?`) to define how many word characters should be matched.

        Note: `\\w` matches any alphanumeric character (letters and digits) and underscore.

        Args:
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            Self: Enables method chaining.
        """
        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=("word character", "word characters")
        )

        self._pattern_parts.append(r"\w" + quantifier)
        self._explanations.append(explanation)
        return self

    def non_word_chars(
        self,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a non-word character-matching pattern (`\\W`) to the current regex expression.

        Supports exact quantities (e.g., `{3}`), ranged quantities (e.g., `{2,5}`),
        and special quantifiers (`+`, `*`, `?`) to define how many non-word characters should be matched.

        Note: `\\W` matches any character that is not a letter, digit, or underscore.

        Args:
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            Self: Enables method chaining.
        """
        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=("non-word character", "non-word characters")
        )

        self._pattern_parts.append(r"\W" + quantifier)
        self._explanations.append(explanation)
        return self

    def whitespace_chars(
        self,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a whitespace-matching pattern (`\\s`) to the current regex expression.

        Matches any whitespace character, including space, tab, newline, carriage return,
        vertical tab, and form feed.

        Supports exact quantities (e.g., `{3}`), ranged quantities (e.g., `{2,5}`),
        and special quantifiers (`+`, `*`, `?`) to define how many whitespace characters should be matched.

        Args:
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            Self: Enables method chaining.
        """

        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=("whitespace character", "whitespace characters")
        )

        self._pattern_parts.append(r"\s" + quantifier)
        self._explanations.append(explanation)
        return self

    def non_whitespace_chars(
        self,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a non-whitespace-matching pattern (`\\S`) to the current regex expression.

        Matches any character that is not considered whitespace (i.e., not space, tab,
        newline, carriage return, vertical tab, or form feed).

        Supports exact quantities (e.g., `{3}`), ranged quantities (e.g., `{2,5}`),
        and special quantifiers (`+`, `*`, `?`) to define how many non-whitespace characters should be matched.

        Args:
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            Self: Enables method chaining.
        """

        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=("non-whitespace character", "non-whitespace characters")
        )

        self._pattern_parts.append(r"\S" + quantifier)
        self._explanations.append(explanation)
        return self

    def end_anchor(self, multiline: bool = False):
        """
        Adds an end-of-line or end-of-text anchor to the regex pattern.

        Args:
            multiline (bool, optional):
                If True, uses '$' to match the ending of each line 
                (when re.MULTILINE is enabled).
                If False (default), uses '\\Z' to match only the start 
                of the entire input string.

        Returns:
            self: Enables method chaining.
        """

        anchor, explanation = ("$", "End of line") if multiline else (r"\Z", "End of text")
        self._pattern_parts.append(anchor)
        self._explanations.append(explanation)
        return self
    
    def word_boundary(self):
        """
        Adds a word boundary anchor (`\\b`) to the regex pattern.

        This anchor matches a position where a word character (letters, digits,
        or underscores) is adjacent to a non-word character (like whitespace,
        punctuation, or the start/end of the string). Commonly used to ensure
        a word starts or ends at a given position.

        Returns:
            self: Enables method chaining.
        """
        self._pattern_parts.append(r"\b")
        self._explanations.append("Word boundary")
        return self

    def non_word_boundary(self):
        """
        Adds a non-word-boundary anchor (`\\B`) to the regex pattern.

        This anchor matches a position where two word characters or two
        non-word characters are adjacent—i.e., not at the boundary of a word.
        Useful to ensure a match occurs strictly inside or outside of words.

        Returns:
            self: Enables method chaining.
        """
        self._pattern_parts.append(r"\B")
        self._explanations.append("Non-word boundary")
        return self

    def literal(
        self,
        text: str,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None,
        capturing: bool = False
    ):
        """
        Adds a literal (exact) string to the regex pattern, escaping special characters.

        Supports exact quantities (e.g., `{3}`), ranged quantities (e.g., `{2,5}`),
        and special quantifiers (`+`, `*`, `?`) to define how many times the entire
        string should be matched.

        Args:
            text (str): The exact string to match literally.
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            self: Enables method chaining.
        """
        if not text:
            return self  # Nothing to add

        escaped = re.escape(text)

        unit_names = ("literal string", "literal strings")

        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=unit_names
        )

        # Group the literal if it has more than 1 character and quantifier is used
        if len(escaped) > 1 and quantifier:
            escaped = f"({escaped})" if capturing else f"(?:{escaped})"

        self._pattern_parts.append(escaped + quantifier)

        # Final explanation
        self._explanations.append(
            f'"{text}"' if not quantifier else f'{explanation}: "{text}"'
        )

        return self

    def start_group(self, capturing: bool = False):
        """
        Starts a new group in the regex pattern.

        Args:
            capturing (bool, optional): 
                If True, creates a capturing group using '()'. 
                If False (default), creates a non-capturing group using '(?:)'.

        Returns:
            self: Enables method chaining.
        """
        self._pattern_parts.append("(" if capturing else "(?:")
        self._explanations.append(
            "Start of capturing group" if capturing else "Start of non-capturing group"
        )
        return self

    def end_group(
    self,
    qty: int | None = None,
    min_qty: int | None = None,
    max_qty: int | None = None,
    special_quantifier: str | None = None
):
        """
        Ends the most recently opened group and optionally applies quantifiers to it.

        Supports exact quantities (e.g., `{3}`), ranged quantities (e.g., `{2,5}`),
        and special quantifiers (`+`, `*`, `?`) to define how many times the group
        should be matched.

        Args:
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            self: Enables method chaining.
        """
        self._pattern_parts.append(")")

        unit_names = ("group", "groups")
        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=unit_names
        )

        if quantifier:
            self._pattern_parts.append(quantifier)
            self._explanations.append(explanation)
        else:
            self._explanations.append(explanation + "and end of group")

        return self

    def lookahead(self, builder: 'RegexBuilder') -> 'RegexBuilder':
        subpattern, explanation = self._process_lookaround_pattern(builder)
        self._pattern_parts.append(f"(?={subpattern})")
        self._explanations.append(f'if followed by {explanation}')
        return self
    
    def negative_lookahead(self, builder: 'RegexBuilder') -> 'RegexBuilder':
        subpattern, explanation = self._process_lookaround_pattern(builder)
        self._pattern_parts.append(f"(?!{subpattern})")
        self._explanations.append(f'if not followed by {explanation}')
        return self

    def lookbehind(self, builder: 'RegexBuilder') -> 'RegexBuilder':
        subpattern, explanation = self._process_lookaround_pattern(builder)
        self._pattern_parts.append(f"(?<={subpattern})")
        self._explanations.append(f'if preceded by {explanation}')
        return self
    
    def negative_lookbehind(self, builder: 'RegexBuilder') -> 'RegexBuilder':
        subpattern, explanation = self._process_lookaround_pattern(builder)
        self._pattern_parts.append(f"(?<!{subpattern})")
        self._explanations.append(f'if not preceded by {explanation}')
        return self

    def char_class(
        self,
        chars: str,
        negated: bool = False,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a character class with specific characters to the regex pattern.

        Creates a character class like [abc] that matches any of the specified characters.
        Can be negated to create [^abc] which matches any character NOT in the set.

        Args:
            chars (str): Characters to include in the class (e.g., "abc", "aeiou").
            negated (bool, optional): If True, creates a negated class [^chars]. Defaults to False.
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            self: Enables method chaining.

        Raises:
            ValueError: If chars is empty or contains invalid characters.
        """
        if not chars:
            raise ValueError("Character class cannot be empty")
        
        # Validate and escape characters for use in character class
        escaped_chars = self._escape_char_class_chars(chars)
        
        # Build the character class
        prefix = "^" if negated else ""
        char_class = f"[{prefix}{escaped_chars}]"
        
        # Handle quantifiers
        unit_names = ("character from class", "characters from class")
        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=unit_names
        )
        
        self._pattern_parts.append(char_class + quantifier)
        
        # Build explanation
        char_display = ''.join(sorted(set(chars)))  # Remove duplicates and sort for display
        base_explanation = f"Any character {'NOT ' if negated else ''}in '{char_display}'"
        final_explanation = base_explanation if not quantifier else f"{explanation}: {base_explanation}"
        
        self._explanations.append(final_explanation)
        return self

    def char_range(
        self,
        start: str,
        end: str,
        negated: bool = False,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a character range to the regex pattern.

        Creates a character class with a range like [a-z] that matches any character
        in the specified range. Can be negated to create [^a-z].

        Args:
            start (str): Start character of the range (e.g., 'a', '0', 'A').
            end (str): End character of the range (e.g., 'z', '9', 'Z').
            negated (bool, optional): If True, creates a negated range [^start-end]. Defaults to False.
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            self: Enables method chaining.

        Raises:
            ValueError: If range is invalid (e.g., start > end, multi-character inputs).
        """
        # Validate the range
        self._validate_char_range(start, end)
        
        # Build the character class with range
        prefix = "^" if negated else ""
        char_class = f"[{prefix}{start}-{end}]"
        
        # Handle quantifiers
        unit_names = ("character from range", "characters from range")
        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=unit_names
        )
        
        self._pattern_parts.append(char_class + quantifier)
        
        # Build explanation
        range_description = f"'{start}' to '{end}'"
        base_explanation = f"Any character {'NOT ' if negated else ''}in range {range_description}"
        final_explanation = base_explanation if not quantifier else f"{explanation}: {base_explanation}"
        
        self._explanations.append(final_explanation)
        return self

    def char_ranges(
        self,
        ranges: list[tuple[str, str]],
        negated: bool = False,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds multiple character ranges to the regex pattern.

        Creates a character class with multiple ranges like [a-zA-Z0-9] that matches
        any character in any of the specified ranges.

        Args:
            ranges (list[tuple[str, str]]): List of (start, end) tuples for ranges.
            negated (bool, optional): If True, creates a negated class. Defaults to False.
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            self: Enables method chaining.

        Raises:
            ValueError: If ranges list is empty or contains invalid ranges.
        """
        if not ranges:
            raise ValueError("Ranges list cannot be empty")
        
        # Validate all ranges
        for start, end in ranges:
            self._validate_char_range(start, end)
        
        # Build the character class with multiple ranges
        range_parts = [f"{start}-{end}" for start, end in ranges]
        prefix = "^" if negated else ""
        char_class = f"[{prefix}{''.join(range_parts)}]"
        
        # Handle quantifiers
        unit_names = ("character from ranges", "characters from ranges")
        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=unit_names
        )
        
        self._pattern_parts.append(char_class + quantifier)
        
        # Build explanation
        range_descriptions = [f"'{start}'-'{end}'" for start, end in ranges]
        ranges_text = ", ".join(range_descriptions)
        base_explanation = f"Any character {'NOT ' if negated else ''}in ranges: {ranges_text}"
        final_explanation = base_explanation if not quantifier else f"{explanation}: {base_explanation}"
        
        self._explanations.append(final_explanation)
        return self

    def char_class_mixed(
        self,
        chars: str = "",
        ranges: list[tuple[str, str]] | None = None,
        escape_sequences: list[str] | None = None,
        negated: bool = False,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a mixed character class combining individual characters, ranges, and escape sequences.

        Creates complex character classes like [a-zA-Z0-9\s._-] that can include:
        - Individual characters
        - Character ranges
        - Escape sequences (\d, \w, \s, etc.)

        Args:
            chars (str, optional): Individual characters to include. Defaults to "".
            ranges (list[tuple[str, str]] | None): List of character ranges. Defaults to None.
            escape_sequences (list[str] | None): List of escape sequences. Defaults to None.
            negated (bool, optional): If True, creates a negated class. Defaults to False.
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.

        Returns:
            self: Enables method chaining.

        Raises:
            ValueError: If all parameters are empty or contain invalid values.
        """
        # Validate that we have at least something to build
        has_chars = bool(chars)
        has_ranges = bool(ranges)
        has_escapes = bool(escape_sequences)
        
        if not (has_chars or has_ranges or has_escapes):
            raise ValueError("Character class cannot be empty - provide chars, ranges, or escape_sequences")
        
        # Build the parts of the character class
        class_parts = []
        
        # Add individual characters (escaped)
        if chars:
            # In mixed classes, we need to escape hyphens even at the end if there are ranges/escapes after
            has_content_after = bool(ranges) or bool(escape_sequences)
            escaped_chars = self._escape_char_class_chars_mixed(chars, has_content_after)
            class_parts.append(escaped_chars)
        
        # Add ranges
        if ranges:
            for start, end in ranges:
                self._validate_char_range(start, end)
                class_parts.append(f"{start}-{end}")
        
        # Add escape sequences
        if escape_sequences:
            for seq in escape_sequences:
                self._validate_escape_sequence(seq)
                class_parts.append(seq)
        
        # Build the character class
        prefix = "^" if negated else ""
        char_class = f"[{prefix}{''.join(class_parts)}]"
        
        # Handle quantifiers
        unit_names = ("character from class", "characters from class")
        quantifier, explanation = self._get_quantifier_and_explanation(
            qty=qty,
            min_qty=min_qty,
            max_qty=max_qty,
            special_quantifier=special_quantifier,
            unit_names=unit_names
        )
        
        self._pattern_parts.append(char_class + quantifier)
        
        # Build explanation
        explanation_parts = []
        if chars:
            char_display = ''.join(sorted(set(chars)))
            explanation_parts.append(f"characters '{char_display}'")
        if ranges:
            range_descriptions = [f"'{start}'-'{end}'" for start, end in ranges]
            explanation_parts.append(f"ranges {', '.join(range_descriptions)}")
        if escape_sequences:
            explanation_parts.append(f"escape sequences {', '.join(escape_sequences)}")
        
        combined_description = ", ".join(explanation_parts)
        base_explanation = f"Any character {'NOT ' if negated else ''}matching: {combined_description}"
        final_explanation = base_explanation if not quantifier else f"{explanation}: {base_explanation}"
        
        self._explanations.append(final_explanation)
        return self

    def build(self) -> str:
        return ''.join(self._pattern_parts)
    
    def compile(self):
        """
        Compiles the regex pattern with all defined parts and flags.

        Returns:
            re.Pattern: A compiled regular expression object using re.compile().
        """
        # Combine flags using bitwise OR to form a proper mask
        flags_mask = 0
        for f in self._flags:
            flags_mask |= int(f)
        return re.compile(self.build(), flags=flags_mask)

    def explain(self):
        # Always return strings - convert any non-string items to string representation
        return [str(item) for item in self._explanations]
    
    def enable_multiline(self, enabled: bool = True):
        """
        Enables or disables the MULTILINE flag in the regex.

        Args:
            enabled (bool, optional):
                If True (default), '^' and '$' will match the start and end of each line.
                If False, they match only the start and end of the whole string.

        Returns:
            self: Enables method chaining.
        """
        self._set_flag(re.MULTILINE, enabled)
        return self

    def enable_ignorecase(self, enabled: bool = True):
        """
        Enables or disables case-insensitive matching (IGNORECASE flag).

        Args:
            enabled (bool, optional):
                If True (default), makes the pattern case-insensitive.
                If False, case sensitivity is preserved.

        Returns:
            self: Enables method chaining.
        """
        self._set_flag(re.IGNORECASE, enabled)
        return self
    
    def enable_dotall(self, enabled: bool = True):
        """
        Enables or disables the DOTALL flag, affecting dot (.) behavior.

        Args:
            enabled (bool, optional):
                If True (default), the '.' character matches newline characters as well.
                If False, '.' does not match newlines.

        Returns:
            self: Enables method chaining.
        """
        self._set_flag(re.DOTALL, enabled)
        return self

    def _set_flag(self, flag: re.RegexFlag, enabled: bool):
        """
        Adds or removes a regex flag from the internal set.

        Args:
            flag (re.RegexFlag): The regex flag to enable or disable.
            enabled (bool): Whether to enable (add) or disable (remove) the flag.
        """
        if enabled:
            self._flags.add(flag)
        else:
            self._flags.discard(flag)

    def _validate_char_range(self, start: str, end: str) -> None:
        """
        Validates that a character range is valid for use in a character class.

        Args:
            start (str): Start character of the range.
            end (str): End character of the range.

        Raises:
            ValueError: If the range is invalid.
        """
        if not isinstance(start, str) or not isinstance(end, str):
            raise ValueError("Range characters must be strings")
        
        if len(start) != 1:
            raise ValueError(f"Range start must be a single character, got: '{start}' (length {len(start)})")
        
        if len(end) != 1:
            raise ValueError(f"Range end must be a single character, got: '{end}' (length {len(end)})")
        
        start_ord = ord(start)
        end_ord = ord(end)
        
        if start_ord > end_ord:
            raise ValueError(
                f"Invalid range '{start}-{end}': start character '{start}' (ASCII {start_ord}) "
                f"must be <= end character '{end}' (ASCII {end_ord})"
            )
        
        # Check for potentially confusing ranges that cross character types
        if start.isalpha() != end.isalpha() and start_ord != end_ord:
            import warnings
            warnings.warn(
                f"Range '{start}-{end}' crosses character types (letter/non-letter). "
                "This may match unexpected characters.",
                UserWarning,
                stacklevel=3
            )
        
        if start.isdigit() != end.isdigit() and start_ord != end_ord:
            import warnings
            warnings.warn(
                f"Range '{start}-{end}' crosses character types (digit/non-digit). "
                "This may match unexpected characters.",
                UserWarning,
                stacklevel=3
            )

    def _escape_char_class_chars(self, chars: str) -> str:
        """
        Escapes special characters for use inside character classes.

        Inside character classes [], certain characters have special meaning and need escaping:
        - ] closes the character class (always needs escaping)
        - \ is the escape character (always needs escaping)  
        - ^ negates the class (only when at the start)
        - - creates ranges (only when between two characters)

        Args:
            chars (str): Characters to escape for use in character class.

        Returns:
            str: Escaped characters safe for use in [].

        Raises:
            ValueError: If chars contains null characters or is empty.
        """
        if not chars:
            raise ValueError("Cannot escape empty character string")
        
        if '\x00' in chars:
            raise ValueError("Null character (\\x00) not allowed in character class")
        
        # Check for non-ASCII characters and warn if found
        try:
            chars.encode('ascii')
        except UnicodeEncodeError:
            import warnings
            non_ascii = [c for c in chars if ord(c) > 127]
            warnings.warn(
                f"Non-ASCII characters detected: {non_ascii}. "
                "Ensure proper encoding handling in your regex engine.",
                UserWarning,
                stacklevel=3
            )
        
        escaped = ""
        for i, char in enumerate(chars):
            if char == ']':
                # ] always needs escaping inside character class
                escaped += r'\]'
            elif char == '\\':
                # \ always needs escaping
                escaped += r'\\'
            elif char == '^' and i == 0:
                # ^ only needs escaping if it's the first character (negation)
                escaped += r'\^'
            elif char == '-' and 0 < i < len(chars) - 1:
                # - only needs escaping if it's in the middle (could be interpreted as range)
                escaped += r'\-'
            else:
                # All other characters are safe in character classes
                escaped += char
        
        return escaped

    def _escape_char_class_chars_mixed(self, chars: str, has_content_after: bool = False) -> str:
        """
        Escapes special characters for use inside mixed character classes.
        
        This is similar to _escape_char_class_chars but handles the case where
        characters are mixed with ranges or escape sequences, requiring different
        escaping rules for hyphens.
        
        Args:
            chars (str): Characters to escape for use in character class.
            has_content_after (bool): Whether there will be ranges or escape sequences after these chars.
        
        Returns:
            str: Escaped characters safe for use in mixed character classes.
        """
        if not chars:
            raise ValueError("Cannot escape empty character string")
        
        if '\x00' in chars:
            raise ValueError("Null character (\\x00) not allowed in character class")
        
        # Check for non-ASCII characters and warn if found
        try:
            chars.encode('ascii')
        except UnicodeEncodeError:
            import warnings
            non_ascii = [c for c in chars if ord(c) > 127]
            warnings.warn(
                f"Non-ASCII characters detected: {non_ascii}. "
                "Ensure proper encoding handling in your regex engine.",
                UserWarning,
                stacklevel=3
            )
        
        escaped = ""
        for i, char in enumerate(chars):
            if char == ']':
                # ] always needs escaping inside character class
                escaped += r'\]'
            elif char == '\\':
                # \ always needs escaping
                escaped += r'\\'
            elif char == '^' and i == 0:
                # ^ only needs escaping if it's the first character (negation)
                escaped += r'\^'
            elif char == '-':
                # In mixed classes, hyphen needs escaping if:
                # 1. It's in the middle of chars (between two characters), OR
                # 2. It's at the end and there's content after (ranges/escapes)
                needs_escape = (0 < i < len(chars) - 1) or (i == len(chars) - 1 and has_content_after)
                if needs_escape:
                    escaped += r'\-'
                else:
                    escaped += char
            else:
                # All other characters are safe in character classes
                escaped += char
        
        return escaped

    def _validate_escape_sequence(self, sequence: str) -> None:
        """
        Validates that an escape sequence is valid for use in character classes.

        Args:
            sequence (str): The escape sequence to validate (e.g., '\\d', '\\w').

        Raises:
            ValueError: If the escape sequence is invalid.
        """
        if not isinstance(sequence, str):
            raise ValueError("Escape sequence must be a string")
        
        # Valid escape sequences for character classes
        valid_sequences = {
            r'\d', r'\D',  # Digits and non-digits
            r'\w', r'\W',  # Word characters and non-word characters  
            r'\s', r'\S',  # Whitespace and non-whitespace
            r'\t',         # Tab
            r'\n',         # Newline
            r'\r',         # Carriage return
            r'\f',         # Form feed
            r'\v',         # Vertical tab
        }
        
        if sequence not in valid_sequences:
            valid_list = ', '.join(sorted(valid_sequences))
            raise ValueError(
                f"Invalid escape sequence: '{sequence}'. "
                f"Valid sequences for character classes are: {valid_list}"
            )

    def _get_quantifier_and_explanation(
        self,
        qty: int | None,
        min_qty: int | None,
        max_qty: int | None,
        special_quantifier: str | None,
        unit_names: tuple[str, str]  # (singular, plural)
    ) -> tuple[str, str]:
        """
        Internal method to generate a quantifier and its human-readable explanation.

        This method handles both standard quantifiers (like `{n}`, `{min,max}`) and 
        special quantifiers (`+`, `*`, `?`), and return the quantifier and an 
        explanation using appropriate singular or plural terms.

        Args:
            qty (int | None): Exact quantity, e.g., 3 for `{3}`.
            min_qty (int | None): Minimum quantity, used in ranged quantifiers.
            max_qty (int | None): Maximum quantity, used in ranged quantifiers.
            special_quantifier (str | None): One of '+', '*', or '?', for shorthand quantifiers.
            unit_names (tuple[str, str]): Singular and plural forms of the item being quantified.

        Returns:
            tuple[str, str]: A tuple containing the regex quantifier string and its explanation.
        """
        singular, plural = unit_names

        if special_quantifier is not None:
            if any(v is not None for v in (qty, min_qty, max_qty)):
                raise ValueError("Cannot use special quantifier along with quantity values.")
            if special_quantifier not in ("+", "*", "?"):
                raise ValueError(f"Invalid special quantifier: {special_quantifier}")
            
            explanation = {
                "+": f"One or more {plural}",
                "*": f"Zero or more {plural}",
                "?": f"Zero or one {singular}"
            }[special_quantifier]

            return special_quantifier, explanation
        
        try:
            if qty is not None:
                qty = int(qty)
            if min_qty is not None:
                min_qty = int(min_qty)
            if max_qty is not None:
                max_qty = int(max_qty)
        except (ValueError, TypeError):
            raise ValueError("Quantities must be valid integers or None.")

        if any(v is not None and v <= 0 for v in (qty, min_qty, max_qty)):
            raise ValueError("Quantities cannot be equal to or less than zero.")
        if min_qty is not None and max_qty is not None and min_qty >= max_qty:
            raise ValueError("min_qty must be less than max_qty.")

        if qty not in (None, 1):
            return f"{{{qty}}}", f"Exactly {qty} {plural}"
        if min_qty is not None and max_qty is not None:
            return f"{{{min_qty},{max_qty}}}", f"Between {min_qty} and {max_qty} {plural}"
        if min_qty is not None:
            unit = singular if min_qty == 1 else plural
            return f"{{{min_qty},}}", f"At least {min_qty} {unit}"
        if max_qty is not None:
            unit = singular if max_qty == 1 else plural
            return f"{{0,{max_qty}}}", f"Up to {max_qty} {unit}"

        return "", f"Exactly 1 {singular}"

    def _process_lookaround_pattern(self, builder: 'RegexBuilder') -> tuple[str, str]:
        if not isinstance(builder, RegexBuilder):
            raise TypeError("Lookaround pattern must be a RegexBuilder instance.")

        subpattern = builder.build()
        # builder.explain() returns list[str]; convert items safely to strings,
        # strip whitespace and filter out empty entries before joining.
        explanation_list = builder.explain() or []
        items = [s.strip() for s in map(str, explanation_list) if s is not None and str(s).strip()]
        # If we have no readable explanation items, fall back to using the raw subpattern
        explanation = "; ".join(items) if items else subpattern
        return subpattern, explanation