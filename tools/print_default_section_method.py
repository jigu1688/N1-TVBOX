p = "tools/re_tools/atv_decompiled/smali/y1/h.smali"

with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = 300
end = 400
for i in range(330, 0, -1):
    if lines[i].startswith('.method '):
        start = i
        break

for i in range(335, len(lines)):
    if lines[i].startswith('.end method'):
        end = i + 1
        break

print(f"Method lines {start+1} to {end}:")
print("".join(lines[start:end]))
