import re

#1) Match 'a' followed by zero or more 'b'
pattern1 = r"ab*"
print(re.fullmatch(pattern1, "abbb"))
print()

#2) Match 'a' followed by two to three 'b'
pattern2 = r"ab{2,3}"
print(re.fullmatch(pattern2, "abb"))
print(re.fullmatch(pattern2, "abbb"))
print(re.fullmatch(pattern2, "abbbb"))
print()

#3) Find lowercase words joined with underscore
text3 = "hello_world test_variable invalid-name"
pattern3 = r"[a-z]+_[a-z]+"
print(re.findall(pattern3, text3))
print()

#4) Find uppercase letter followed by lowercase letters
text4 = "Hello world Python Programming"
pattern4 = r"[A-Z][a-z]+"
print(re.findall(pattern4, text4))
print()

#5) Match 'a' followed by anything, ending in 'b'
pattern5 = r"a.*b"
print(re.fullmatch(pattern5, "axxxb"))
print(re.fullmatch(pattern5, "ab"))
print()

#6) Replace space, comma, or dot with colon
text6 = "Python is fun, and powerful."
result6 = re.sub(r"[ ,.]", ":", text6)
print(result6)
print()

#7) Convert snake_case to camelCase
def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

print(snake_to_camel("hello_world_example"))
print()

#8) Split string at uppercase letters
text8 = "SplitThisStringAtUppercase"
result8 = re.split(r"(?=[A-Z])", text8)
print(result8)
print()

#9) Insert spaces between words starting with capital letters
text9 = "InsertSpacesBetweenWords"
result9 = re.sub(r"(?<!^)(?=[A-Z])", " ", text9)
print(result9)
print()

#10) Convert camelCase to snake_case
def camel_to_snake(text):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()

print(camel_to_snake("camelCaseStringExample"))
print()