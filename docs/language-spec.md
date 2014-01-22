# Introduction

This is the reference manual for the wlvlang programming language.  wlvlang is a dynamically typed, high-level interpreted language designed with first-class concurrency support.

Programs are constructed from modules and can be compiled and linked or you can define an entry point with a given `WLVLANGPATH` environment variable for module lookup.


# Notation

The syntax is specified using an EBNF notation.  Note the [regular expression for quoted elements](https://bitbucket.org/pypy/pypy/src/c051852e3f7da50aeeabcca0e27af882d33ad3f0/rpython/rlib/parsing/ebnfparse.py?at=default#cl-16 "Regular Expressions defined for quoted elements in the RPython rlib default EBNF format")  is omitted here for simplicity's sake.

```ANTLR
NONTERMINALNAME: "([a-z]|_)[a-z0-9_]*";
SYMBOLNAME: "_*[A-Z]([A-Z]|_)*";
QUOTED: # Any double quote '"' enclosed string or character
file: list EOF;
list: element+;
element: <regex> | <production>;
regex: SYMBOLNAME ":" QUOTE ";";
production: NONTERMINALNAME ":" body? ";";
body: (expansion ["|"])* expansion;
expansion: decorated+;
decorated: enclosed "*" |
           enclosed "+" |
           enclosed "?" |
           <enclosed>;
enclosed: "[" expansion "]" |
          ">" expansion "<" |
          "<" primary ">" |
          "(" <expansion> ")" |
          <primary>;
primary: NONTERMINALNAME | SYMBOLNAME | QUOTE;
```
