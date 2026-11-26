"""
Практическая работа № 5, часть 2, вариант 3.
Анализатор рекурсивного спуска для последовательностей «побитовых» выражений.

Лексемы:
  NUM  - целое число: десятичное (123), двоичное (0b101) или троичное (0t1202)
  ID   - имя переменной из 1-2 латинских букв
  ~ & + ^ = ( ) ;  - знаки операций, скобки и разделитель
Результат работы: Accepted или Rejected.

Грамматика (LL(1)):
  P -> E R
  R -> ; E R | ε
  E -> ID N | ~ U Y X | ( E ) Y X | NUM Y X
  N -> = E | Y X
  X -> + T X | ^ T X | ε
  T -> U Y
  Y -> & U Y | ε
  U -> ~ U | F
  F -> ID | NUM | ( E )
"""
import re
import sys

SYMBOLS = "~&+^=();"
RE_BIN = re.compile(r"0b[01]+")
RE_TER = re.compile(r"0t[0-2]+")
RE_DEC = re.compile(r"[0-9]+")
RE_ID = re.compile(r"[A-Za-z]{1,2}")


class SyntaxErr(Exception):
    pass


def tokenize(text):
    """Лексер: возвращает список пар (тип, значение), в конце - ('$', '$')."""
    tokens, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
        elif c in SYMBOLS:
            tokens.append((c, c))
            i += 1
        elif c.isalnum() and c.isascii():
            j = i
            while j < n and text[j].isalnum() and text[j].isascii():
                j += 1
            word = text[i:j]          # максимальная буквенно-цифровая цепочка
            if RE_BIN.fullmatch(word) or RE_TER.fullmatch(word) or RE_DEC.fullmatch(word):
                tokens.append(("NUM", word))
            elif RE_ID.fullmatch(word):
                tokens.append(("ID", word))
            else:
                raise SyntaxErr("недопустимая лексема " + word)
            i = j
        else:
            raise SyntaxErr("недопустимый символ " + c)
    tokens.append(("$", "$"))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.t = tokens
        self.pos = 0

    @property
    def cur(self):
        return self.t[self.pos][0]

    def eat(self, kind):
        if self.cur != kind:
            raise SyntaxErr("ожидалось %s, найдено %s" % (kind, self.cur))
        self.pos += 1

    # P -> E R
    def program(self):
        self.expression()
        self.rest()
        self.eat("$")

    # R -> ; E R | ε
    def rest(self):
        while self.cur == ";":
            self.eat(";")
            self.expression()

    # E -> ID N | ~ U Y X | ( E ) Y X | NUM Y X
    def expression(self):
        if self.cur == "ID":
            self.eat("ID")
            self.after_id()
        elif self.cur == "~":
            self.unary()
            self.mult_tail()
            self.add_tail()
        elif self.cur == "(":
            self.eat("(")
            self.expression()
            self.eat(")")
            self.mult_tail()
            self.add_tail()
        elif self.cur == "NUM":
            self.eat("NUM")
            self.mult_tail()
            self.add_tail()
        else:
            raise SyntaxErr("ожидалось выражение, найдено " + self.cur)

    # N -> = E | Y X
    def after_id(self):
        if self.cur == "=":
            self.eat("=")
            self.expression()
        else:
            self.mult_tail()
            self.add_tail()

    # X -> + T X | ^ T X | ε
    def add_tail(self):
        while self.cur in ("+", "^"):
            self.eat(self.cur)
            self.term()

    # T -> U Y
    def term(self):
        self.unary()
        self.mult_tail()

    # Y -> & U Y | ε
    def mult_tail(self):
        while self.cur == "&":
            self.eat("&")
            self.unary()

    # U -> ~ U | F
    def unary(self):
        if self.cur == "~":
            self.eat("~")
            self.unary()
        else:
            self.factor()

    # F -> ID | NUM | ( E )
    def factor(self):
        if self.cur in ("ID", "NUM"):
            self.eat(self.cur)
        elif self.cur == "(":
            self.eat("(")
            self.expression()
            self.eat(")")
        else:
            raise SyntaxErr("ожидался операнд, найдено " + self.cur)


def check(text):
    try:
        Parser(tokenize(text)).program()
        return "Accepted"
    except SyntaxErr:
        return "Rejected"


# Тестовые цепочки
tests = [
    "a=101",
    "ab=0b1011+7",
    "x=0t1202&y;z=~x",
    "a=b=c",
    "a=(b=c)^1",
    "ab=~(cd+0b1)&~~5",
    "a=1;b=2;c=a+b",
    "a=0b102",
    "a=0t3",
    "abc=1",
    "a=1;",
    "a+b=c",
    "a=1+",
    "a=(b",
]


def run_tests():
    print("Результаты распознавания методом рекурсивного спуска:\n")
    for i, word in enumerate(tests, start=1):
        print(f"{str(i) + '.':<4}{word:20} - {check(word)}")


def main():
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "-e":
        print(check(args[1]))
    elif len(args) == 1:
        with open(args[0], encoding="utf-8") as f:
            print(check(f.read()))
    else:
        run_tests()


if __name__ == "__main__":
    main()
