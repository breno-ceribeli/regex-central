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
        self._pattern = ""
        self._parts = []
        self._flags = set()

    def add_start_anchor(self, multiline: bool = False):
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
        self._pattern += anchor
        self._parts.append(explanation)
        return self
    
    def has_digits(
        self,
        qty: int | None = None,
        min_qty: int | None = None,
        max_qty: int | None = None,
        special_quantifier: str | None = None
    ):
        """
        Adds a digit-matching pattern to the current regex expression.

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

        self._pattern += r"\d" + quantifier
        self._parts.append(explanation)
        return self

    def add_end_anchor(self, multiline: bool = False):
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
        self._pattern += anchor
        self._parts.append(explanation)
        return self
    
    def build(self):
        return self._pattern
    
    def compile(self):
        """
        Compiles the regex pattern with all defined parts and flags.

        Returns:
            re.Pattern: A compiled regular expression object using re.compile().
        """
        return re.compile(self.build(), flags=sum(self._flags))

    def explain(self):
        return self._parts.copy()
    
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