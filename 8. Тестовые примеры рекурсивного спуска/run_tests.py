from recursive_descent import check

TESTS = [
    ("a=101",              "Accepted"),
    ("ab=0b1011+7",        "Accepted"),
    ("x=0t1202&y;z=~x",    "Accepted"),
    ("a=b=c",              "Accepted"),
    ("a=(b=c)^1",          "Accepted"),
    ("ab=~(cd+0b1)&~~5",   "Accepted"),
    ("a=1;b=2;c=a+b",      "Accepted"),
    ("a=0b102",            "Rejected"),
    ("a=0t3",              "Rejected"),
    ("abc=1",              "Rejected"),
    ("a=1;",               "Rejected"),
    ("a+b=c",              "Rejected"),
    ("a=1+",               "Rejected"),
    ("a=(b",               "Rejected"),
]

ok = 0
for i, (s, expected) in enumerate(TESTS, 1):
    got = check(s)
    ok += got == expected
    print(f"{i:2}. {s:<20} {got:<9}")
