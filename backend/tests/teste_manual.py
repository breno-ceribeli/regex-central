import re
from src.builder import RegexBuilder

# # Manual experiments below. Run this file as a module from backend directory:
# #   python -m tests.teste_manual

# def test_character_classes():
#     print("=" * 60)
#     print("TESTANDO CHARACTER CLASSES NO REGEXBUILDER")
#     print("=" * 60)
    
#     # 1. Teste básico de char_class
#     print("\n1. CHAR_CLASS BÁSICO:")
#     try:
#         b1 = RegexBuilder()
#         b1.char_class("aeiou")
#         pattern1 = b1.build()
#         explanation1 = b1.explain()
#         print(f"   Pattern: {pattern1}")
#         print(f"   Explanation: {explanation1}")
        
#         # Testar se funciona
#         compiled1 = re.compile(pattern1)
#         test_text1 = "hello world"
#         matches1 = compiled1.findall(test_text1)
#         print(f"   Matches em '{test_text1}': {matches1}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 2. Teste char_class com quantificador
#     print("\n2. CHAR_CLASS COM QUANTIFICADOR:")
#     try:
#         b2 = RegexBuilder()
#         b2.char_class("aeiou", qty=2)
#         pattern2 = b2.build()
#         explanation2 = b2.explain()
#         print(f"   Pattern: {pattern2}")
#         print(f"   Explanation: {explanation2}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 3. Teste char_range
#     print("\n3. CHAR_RANGE:")
#     try:
#         b3 = RegexBuilder()
#         b3.char_range("a", "z")
#         pattern3 = b3.build()
#         explanation3 = b3.explain()
#         print(f"   Pattern: {pattern3}")
#         print(f"   Explanation: {explanation3}")
        
#         # Testar range parcial
#         b3b = RegexBuilder()
#         b3b.char_range("0", "5")
#         pattern3b = b3b.build()
#         print(f"   Range parcial [0-5]: {pattern3b}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 4. Teste char_class negado
#     print("\n4. CHAR_CLASS NEGADO:")
#     try:
#         b4 = RegexBuilder()
#         b4.char_class("aeiou", negated=True)
#         pattern4 = b4.build()
#         explanation4 = b4.explain()
#         print(f"   Pattern: {pattern4}")
#         print(f"   Explanation: {explanation4}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 5. Teste char_range negado
#     print("\n5. CHAR_RANGE NEGADO:")
#     try:
#         b5 = RegexBuilder()
#         b5.char_range("0", "9", negated=True)
#         pattern5 = b5.build()
#         explanation5 = b5.explain()
#         print(f"   Pattern: {pattern5}")
#         print(f"   Explanation: {explanation5}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 6. Teste char_ranges (múltiplos ranges)
#     print("\n6. CHAR_RANGES (múltiplos):")
#     try:
#         b6 = RegexBuilder()
#         b6.char_ranges([("a", "z"), ("A", "Z"), ("0", "9")])
#         pattern6 = b6.build()
#         explanation6 = b6.explain()
#         print(f"   Pattern: {pattern6}")
#         print(f"   Explanation: {explanation6}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 7. Teste char_class_mixed
#     print("\n7. CHAR_CLASS_MIXED:")
#     try:
#         b7 = RegexBuilder()
#         b7.char_class_mixed(
#             chars="aeiou",
#             ranges=[("0", "9"), ("A", "Z")],
#             escape_sequences=[r"\s"]
#         )
#         pattern7 = b7.build()
#         explanation7 = b7.explain()
#         print(f"   Pattern: {pattern7}")
#         print(f"   Explanation: {explanation7}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 8. Teste char_class_mixed negado
#     print("\n8. CHAR_CLASS_MIXED NEGADO:")
#     try:
#         b8 = RegexBuilder()
#         b8.char_class_mixed(
#             chars="xyz",
#             ranges=[("0", "2")],
#             negated=True,
#             special_quantifier="+"
#         )
#         pattern8 = b8.build()
#         explanation8 = b8.explain()
#         print(f"   Pattern: {pattern8}")
#         print(f"   Explanation: {explanation8}")
#     except Exception as e:
#         print(f"   ERRO: {e}")

# def test_character_classes_edge_cases():
#     print("\n" + "=" * 60)
#     print("TESTANDO CASOS ESPECIAIS E VALIDAÇÕES")
#     print("=" * 60)
    
#     # 9. Teste chars com caracteres especiais
#     print("\n9. CARACTERES ESPECIAIS:")
#     try:
#         b9 = RegexBuilder()
#         b9.char_class("]-^")
#         pattern9 = b9.build()
#         print(f"   Chars especiais ']-^': {pattern9}")
        
#         b9b = RegexBuilder()
#         b9b.char_class(".,;!?")
#         pattern9b = b9b.build()
#         print(f"   Pontuação '.,;!?': {pattern9b}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 10. Teste range inválido (deve dar erro)
#     print("\n10. RANGE INVÁLIDO (deve dar erro):")
#     try:
#         b10 = RegexBuilder()
#         b10.char_range("z", "a")  # Range invertido
#         pattern10 = b10.build()
#         print(f"   ERRO: Deveria ter falhado! Pattern: {pattern10}")
#     except Exception as e:
#         print(f"   ✅ ERRO esperado: {e}")
    
#     # 11. Teste char_class vazio (deve dar erro)
#     print("\n11. CHAR_CLASS VAZIO (deve dar erro):")
#     try:
#         b11 = RegexBuilder()
#         b11.char_class("")
#         pattern11 = b11.build()
#         print(f"   ERRO: Deveria ter falhado! Pattern: {pattern11}")
#     except Exception as e:
#         print(f"   ✅ ERRO esperado: {e}")
    
#     # 12. Teste escape_sequence inválida (deve dar erro)
#     print("\n12. ESCAPE_SEQUENCE INVÁLIDA (deve dar erro):")
#     try:
#         b12 = RegexBuilder()
#         b12.char_class_mixed(escape_sequences=[r"\x"])  # Inválida
#         pattern12 = b12.build()
#         print(f"   ERRO: Deveria ter falhado! Pattern: {pattern12}")
#     except Exception as e:
#         print(f"   ✅ ERRO esperado: {e}")
    
#     # 13. Teste range com caracteres múltiplos (deve dar erro)
#     print("\n13. RANGE COM MÚLTIPLOS CHARS (deve dar erro):")
#     try:
#         b13 = RegexBuilder()
#         b13.char_range("ab", "z")  # Primeiro argumento tem 2 chars
#         pattern13 = b13.build()
#         print(f"   ERRO: Deveria ter falhado! Pattern: {pattern13}")
#     except Exception as e:
#         print(f"   ✅ ERRO esperado: {e}")

# def test_character_classes_real_world():
#     print("\n" + "=" * 60)
#     print("TESTANDO CASOS DO MUNDO REAL")
#     print("=" * 60)
    
#     # 14. Hexadecimal
#     print("\n14. HEXADECIMAL:")
#     try:
#         b14 = RegexBuilder()
#         b14.char_class_mixed(ranges=[("0", "9"), ("a", "f"), ("A", "F")])
#         pattern14 = b14.build()
#         explanation14 = b14.explain()
#         print(f"   Hexadecimal: {pattern14}")
#         print(f"   Explanation: {explanation14}")
        
#         # Testar com texto real
#         compiled14 = re.compile(pattern14)
#         hex_text = "FF00A1B2"
#         matches14 = compiled14.findall(hex_text)
#         print(f"   Matches em '{hex_text}': {matches14}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 15. Apenas consoantes (negando vogais)
#     print("\n15. CONSOANTES (negando vogais):")
#     try:
#         b15 = RegexBuilder()
#         b15.char_class("aeiouAEIOU", negated=True).word_chars()
#         pattern15 = b15.build()
#         explanation15 = b15.explain()
#         print(f"   Pattern: {pattern15}")
#         print(f"   Explanation: {explanation15}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 16. Dígitos não-zero
#     print("\n16. DÍGITOS NÃO-ZERO:")
#     try:
#         b16 = RegexBuilder()
#         b16.char_range("1", "9")
#         pattern16 = b16.build()
#         explanation16 = b16.explain()
#         print(f"   Pattern: {pattern16}")
#         print(f"   Explanation: {explanation16}")
        
#         # Testar
#         compiled16 = re.compile(pattern16)
#         test_text16 = "102304"
#         matches16 = compiled16.findall(test_text16)
#         print(f"   Matches em '{test_text16}': {matches16}")
#     except Exception as e:
#         print(f"   ERRO: {e}")
    
#     # 17. Email básico (exemplo com múltiplas classes)
#     print("\n17. EMAIL BÁSICO:")
#     try:
#         b17 = (RegexBuilder()
#                .char_ranges([("a", "z"), ("A", "Z"), ("0", "9")], special_quantifier="+")
#                .literal("@")
#                .char_ranges([("a", "z"), ("A", "Z"), ("0", "9")], special_quantifier="+")
#                .literal(".")
#                .char_range("a", "z", min_qty=2, max_qty=4))
        
#         pattern17 = b17.build()
#         explanation17 = b17.explain()
#         print(f"   Pattern: {pattern17}")
#         print(f"   Explanation: {explanation17}")
        
#         # Testar
#         compiled17 = re.compile(pattern17)
#         emails = ["user@domain.com", "test@site.org", "invalid@", "@invalid.com"]
#         for email in emails:
#             match = compiled17.match(email)
#             print(f"   '{email}': {'✅ Match' if match else '❌ No match'}")
#     except Exception as e:
#         print(f"   ERRO: {e}")

# def test_chaining():
#     print("\n" + "=" * 60)
#     print("TESTANDO METHOD CHAINING")
#     print("=" * 60)
    
#     # 18. Chaining complexo
#     print("\n18. CHAINING COMPLEXO:")
#     try:
#         b18 = (RegexBuilder()
#                .start_anchor()
#                .char_range("A", "Z")  # Letra maiúscula
#                .char_range("a", "z", special_quantifier="+")  # Letras minúsculas
#                .char_range("0", "9", qty=3)  # Exatamente 3 dígitos
#                .end_anchor())
        
#         pattern18 = b18.build()
#         explanation18 = b18.explain()
#         print(f"   Pattern: {pattern18}")
#         print(f"   Explanation: {explanation18}")
        
#         # Testar
#         compiled18 = re.compile(pattern18)
#         test_cases = ["Abc123", "ABC123", "a123", "Abcd123", "Ab12"]
#         for test_case in test_cases:
#             match = compiled18.match(test_case)
#             print(f"   '{test_case}': {'✅ Match' if match else '❌ No match'}")
    
#     except Exception as e:
#         print(f"   ERRO: {e}")

# def test_warnings():
#     print("\n" + "=" * 60)
#     print("TESTANDO WARNINGS")
#     print("=" * 60)
    
#     import warnings
    
#     # Capturar warnings para mostrar
#     with warnings.catch_warnings(record=True) as w:
#         warnings.simplefilter("always")  # Sempre mostrar warnings
        
#         # 1. Range que cruza tipos de caracteres
#         print("\n19. RANGE CROSS-TYPE (deve gerar warning):")
#         try:
#             b19 = RegexBuilder()
#             b19.char_range("9", "A")  # Dígito para letra
#             pattern19 = b19.build()
#             print(f"   Pattern: {pattern19}")
            
#             # Verificar se warning foi gerado
#             if w:
#                 print(f"   ⚠️  Warning capturado: {w[-1].message}")
#             else:
#                 print("   Nenhum warning gerado")
                
#         except Exception as e:
#             print(f"   ERRO: {e}")
        
#         # 2. Caracteres não-ASCII
#         print("\n20. CARACTERES NÃO-ASCII (deve gerar warning):")
#         try:
#             b20 = RegexBuilder()
#             b20.char_class("áéíóú")  # Caracteres acentuados
#             pattern20 = b20.build()
#             print(f"   Pattern: {pattern20}")
            
#             # Verificar warnings mais recentes
#             recent_warnings = [warning for warning in w if "Non-ASCII" in str(warning.message)]
#             if recent_warnings:
#                 print(f"   ⚠️  Warning capturado: {recent_warnings[-1].message}")
#             else:
#                 print("   Nenhum warning gerado")
                
#         except Exception as e:
#             print(f"   ERRO: {e}")
        
#         # 3. Range normal (não deve gerar warning)
#         print("\n21. RANGE NORMAL (não deve gerar warning):")
#         try:
#             b21 = RegexBuilder()
#             b21.char_range("a", "z")  # Range normal
#             pattern21 = b21.build()
#             print(f"   Pattern: {pattern21}")
#             print("   ✅ Nenhum warning esperado")
                
#         except Exception as e:
#             print(f"   ERRO: {e}")

# def test_warnings_in_detail():
#     print("\n" + "=" * 60)
#     print("DEMONSTRAÇÃO DETALHADA DE WARNINGS")
#     print("=" * 60)
    
#     import warnings
#     import sys
    
#     # Configurar para mostrar warnings no stdout
#     def show_warning(message, category, filename, lineno, file=None, line=None):
#         print(f"🔔 WARNING: {message}")
#         print(f"   Tipo: {category.__name__}")
#         print(f"   Local: {filename}:{lineno}")
    
#     old_showwarning = warnings.showwarning
#     warnings.showwarning = show_warning
    
#     print("\n22. VÁRIOS RANGES PROBLEMÁTICOS:")
    
#     # Ranges problemáticos
#     test_ranges = [
#         ("9", "A", "dígito para letra maiúscula"),
#         ("Z", "a", "letra maiúscula para minúscula"),  
#         ("z", "0", "letra para dígito"),
#         ("!", "9", "símbolo para dígito"),
#     ]
    
#     for start, end, description in test_ranges:
#         print(f"\n   Testando range '{start}-{end}' ({description}):")
#         try:
#             b = RegexBuilder()
#             b.char_range(start, end)
#             pattern = b.build()
#             print(f"   Pattern gerado: {pattern}")
#         except Exception as e:
#             print(f"   ERRO: {e}")
    
#     print("\n23. CARACTERES ESPECIAIS DE VÁRIAS ORIGENS:")
    
#     # Caracteres não-ASCII de diferentes origens
#     test_chars = [
#         ("áéíóú", "acentos portugueses"),
#         ("中文", "caracteres chineses"),
#         ("🚀🎯", "emojis"),
#         ("αβγ", "letras gregas"),
#         ("café", "palavra com acento"),
#     ]
    
#     for chars, description in test_chars:
#         print(f"\n   Testando chars '{chars}' ({description}):")
#         try:
#             b = RegexBuilder()
#             b.char_class(chars)
#             pattern = b.build()
#             print(f"   Pattern gerado: {pattern}")
#         except Exception as e:
#             print(f"   ERRO: {e}")
    
#     # Restaurar configuração original
#     warnings.showwarning = old_showwarning

# if __name__ == "__main__":
#     # test_character_classes()
#     # test_character_classes_edge_cases()
#     # test_character_classes_real_world()
#     # test_chaining()
#     test_warnings()
#     test_warnings_in_detail()

b2 = RegexBuilder()
b2.char_class_mixed(
    chars="._-",
    ranges=[("a", "z"), ("A", "Z"), ("0", "9")],
    escape_sequences=[r"\w", r"\d"]
)
print(b2.build())