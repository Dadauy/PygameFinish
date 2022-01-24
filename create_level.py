level = ["." for i in range(125)]
print("".join(level))
for x in range(15):
    print("".join(["."] + ["_" for y in range(123)] + ["."]))
    print("".join(["."] + ["_" for b in range(123)] + ["."]))
    print("".join(["."] + ["_" for q in range(123)] + ["."]))
    print("".join(["."] + ["_" for q in range(123)] + ["."]))
    print("".join(["."] + ["_" for t in range(123)] + ["."]))
    print("".join(["."] + ["_" for l in range(123)] + ["."]))
    print("".join(["."] + ["_" for m in range(123)] + ["."]))
    print("".join([".", "_"] + ["." for c in range(122)] + ["."]))
print("".join(level))
