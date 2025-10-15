import re
from src.builder import RegexBuilder

# Manual experiments below. Run this file as a module from backend directory:
#   python -m tests.teste_manual
print("Manual tests for RegexBuilder")
b = RegexBuilder()
b.digits(qty=3)
print("Built regex:", b.build())