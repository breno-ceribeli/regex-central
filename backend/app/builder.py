import re

class RegexBuilder:
    def __init__(self):
        self._pattern = ""
        self._parts = []

    def starts_with(self, text: str):
        self._pattern += "^" + re.escape(text)
        self._parts.append(f"Começa com \"{text}\"")
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

    def ends_with(self, text: str):
        self._pattern += re.escape(text) + "$"
        self._parts.append(f"Termina com \"{text}\"")
        return self
    
    def build(self):
        return self._pattern
    
    def explain(self):
        return self._parts.copy()
    
    