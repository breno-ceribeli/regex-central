import re

class RegexBuilder:
    def __init__(self):
        self._pattern = ""
        self._parts = []

    def starts_with(self, text: str):
        self._pattern += "^" + re.escape(text)
        self._parts.append(f"Começa com \"{text}\"")
        return self
    
    def has_digits(self, quantifier: str = ""):
        self._pattern += r"\d" + quantifier
        self._parts.append(f"{quantifier or 'um ou mais'} dígito(s)")
        return self
    
    def ends_with(self, text: str):
        self._pattern += re.escape(text) + "$"
        self._parts.append(f"Termina com \"{text}\"")
        return self
    
    def build(self):
        return self._pattern
    
    def explain(self):
        return self._parts.copy()
    
    