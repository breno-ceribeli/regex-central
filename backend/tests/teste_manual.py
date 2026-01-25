import re
from builder import RegexBuilder

# # Manual experiments below. Run this file as a module from backend directory:
# #   python -m tests.teste_manual

part = RegexBuilder().digits(3).any_char()
    
b = RegexBuilder()
b.alternation(["id_", part, "code"])

print(b.build())
print(b.explain())