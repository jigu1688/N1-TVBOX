import re

code = open('tools/re_tools/tvsettings_decompiled/smali/com/android/tv/settings/display/OutputUiManager.smali', encoding='utf-8').read()
start = code.find('<clinit>')
end = code.find('.end method', start)
clinit = code[start:end]

strings = re.findall(r'const-string(?:/jumbo)?\s+[vp]\d+,\s+"([^"]+)"', clinit)
print("=== Clinit strings in OutputUiManager ===")
for s in strings:
    print(s)
