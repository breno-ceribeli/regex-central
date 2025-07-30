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

    def build(self) -> str:
        return ''.join(self._pattern_parts)
    
    def compile(self):
        """
        Compiles the regex pattern with all defined parts and flags.

        Returns:
            re.Pattern: A compiled regular expression object using re.compile().
        """
        return re.compile(self.build(), flags=sum(self._flags))

    def explain(self):
        return self._explanations.copy()
    
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