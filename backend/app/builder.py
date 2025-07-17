import re

class RegexBuilder:
    # Mapping of `re` module flags to a human-readable name and description.
    # Used to display flag information in the interface and generate documentation.
    FLAG_INFO = {
        re.MULTILINE: ("MULTILINE", "Faz com que ^ e $ correspondam ao início e ao fim de cada linha."),
        re.IGNORECASE: ("IGNORECASE", "Faz a correspondência sem diferenciar maiúsculas de minúsculas."),
        re.DOTALL: ("DOTALL", "Faz o ponto (.) corresponder também a quebras de linha.")
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

        anchor, explanation = ("^", "Início da linha") if multiline else (r"\A", "Início do texto")
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
        # Handle special quantifiers like +, *, ?
        if special_quantifier is not None:
            if any(v is not None for v in (qty, min_qty, max_qty)):
                raise ValueError("Não é permitido usar quantificador especial junto com quantidades.")
            if special_quantifier not in ("+", "*", "?"):
                raise ValueError(f"Quantificador especial inválido: {special_quantifier}")
            
            quantifier = special_quantifier
            explanation = {
                "+": "Um ou mais dígitos",
                "*": "Zero ou mais dígitos",
                "?": "Zero ou um dígito"
            }[quantifier]

        else:
            # Normalize input in case values come as strings
            try:
                if qty is not None:
                    qty = int(qty)
                if min_qty is not None:
                    min_qty = int(min_qty)
                if max_qty is not None:
                    max_qty = int(max_qty)
            except (ValueError, TypeError):
                raise ValueError("As quantidades devem ser números inteiros válidos ou None.")

            # Validate quantity constraints
            if any(v is not None and v < 0 for v in (qty, min_qty, max_qty)):
                raise ValueError("Quantidade de dígitos não pode ser negativa.")

            if min_qty is not None and max_qty is not None and min_qty >= max_qty:
                raise ValueError("min_qty não pode ser maior ou igual a max_qty.")
            
            # Determine quantifier and explanation
            if qty not in (None, 1):
                quantifier = f"{{{qty}}}"
                explanation = f"Exatamente {qty} dígitos"
            else:
                if min_qty is not None and max_qty is not None:
                    quantifier = f"{{{min_qty},{max_qty}}}"
                    explanation = f"Entre {min_qty} e {max_qty} dígitos"
                elif min_qty is not None:
                    quantifier = f"{{{min_qty},}}"
                    explanation = f"Pelo menos {min_qty} dígitos"
                elif max_qty is not None:
                    quantifier = f"{{0,{max_qty}}}"
                    explanation = f"Até {max_qty} dígitos"
                else:
                    quantifier = ""
                    explanation = "Exatamente 1 dígito"

        # Append regex and explanation
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

        anchor, explanation = ("$", "Fim da linha") if multiline else (r"\Z", "Fim do texto")
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