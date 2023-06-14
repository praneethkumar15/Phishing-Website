__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = ('GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, '
 'Skip Montanaro, Raymond Hettinger, Trent Nelson, '
 'Michael Foord')
from builtins import open as _builtin_open
from codecs import lookup, BOM_UTF8
import collections
from io import TextIOWrapper
from itertools import chain
import itertools as _itertools
import re
import sys
from token import *
cookie_re = re.compile(r'^[ \t\f]*#.*?coding[:=][ \t]*([-\w.]+)', re.ASCII)
blank_re = re.compile(br'^[ \t\f]*(?:[#\r\n]|$)', re.ASCII)
import token
__all__ = token.__all__ + ["tokenize", "detect_encoding",
 "untokenize", "TokenInfo"]
del token
EXACT_TOKEN_TYPES = {
 '(': LPAR,
 ')': RPAR,
 '[': LSQB,
 ']': RSQB,
 ':': COLON,
 ',': COMMA,
 ';': SEMI,
 '+': PLUS,
 '-': MINUS,
 '*': STAR,
 '/': SLASH,
 '|': VBAR,
 '&': AMPER,
 '<': LESS,
 '>': GREATER,
 '=': EQUAL,
 '.': DOT,
 '%': PERCENT,
 '{': LBRACE,
 '}': RBRACE,
 '==': EQEQUAL,
 '!=': NOTEQUAL,
 '<=': LESSEQUAL,
 '>=': GREATEREQUAL,
 '~': TILDE,
 '^': CIRCUMFLEX,
 '<<': LEFTSHIFT,
 '>>': RIGHTSHIFT,
 '**': DOUBLESTAR,
 '+=': PLUSEQUAL,
 '-=': MINEQUAL,
 '*=': STAREQUAL,
 '/=': SLASHEQUAL,
 '%=': PERCENTEQUAL,
 '&=': AMPEREQUAL,
 '|=': VBAREQUAL,
 '^=': CIRCUMFLEXEQUAL,
 '<<=': LEFTSHIFTEQUAL,
 '>>=': RIGHTSHIFTEQUAL,
 '**=': DOUBLESTAREQUAL,
 '//': DOUBLESLASH,
 '//=': DOUBLESLASHEQUAL,
 '...': ELLIPSIS,
 '->': RARROW,
 '@': AT,
 '@=': ATEQUAL,
}
class TokenInfo(collections.namedtuple('TokenInfo', 'type string start end line')):
 def __repr__(self):
 annotated_type = '%d (%s)' % (self.type, tok_name[self.type])
 return ('TokenInfo(type=%s, string=%r, start=%r, end=%r, line=%r)' %
 self._replace(type=annotated_type))
 @property
 def exact_type(self):
 if self.type == OP and self.string in EXACT_TOKEN_TYPES:
 return EXACT_TOKEN_TYPES[self.string]
 else:
 return self.type
52
def group(*choices): return '(' + '|'.join(choices) + ')'
def any(*choices): return group(*choices) + '*'
def maybe(*choices): return group(*choices) + '?'
# Note: we use unicode matching for names ("\w") but ascii matching for
# number literals.
Whitespace = r'[ \f\t]*'
Comment = r'#[^\r\n]*'
Ignore = Whitespace + any(r'\\\r?\n' + Whitespace) + maybe(Comment)
Name = r'\w+'
Hexnumber = r'0[xX](?:_?[0-9a-fA-F])+'
Binnumber = r'0[bB](?:_?[01])+'
Octnumber = r'0[oO](?:_?[0-7])+'
Decnumber = r'(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = r'[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = group(r'[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?',
 r'\.[0-9](?:_?[0-9])*') + maybe(Exponent)
Expfloat = r'[0-9](?:_?[0-9])*' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group(r'[0-9](?:_?[0-9])*[jJ]', Floatnumber + r'[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)
# Return the empty string, plus all of the valid string prefixes.
def _all_string_prefixes():
 # The valid string prefixes. Only contain the lower-case versions,
 # and don't contain any permuations (include 'fr', but not
 # 'rf'). The various permutations will be generated.
 _valid_string_prefixes = ['b', 'r', 'u', 'f', 'br', 'fr']
 # if we add binary f-strings, add: ['fb', 'fbr']
 result = {''}
 for prefix in _valid_string_prefixes:
 for t in _itertools.permutations(prefix):
 # create a list with upper and lower versions of each
 # character
 for u in _itertools.product(*[(c, c.upper()) for c in t]):
 result.add(''.join(u))
 return result
def _compile(expr):
 return re.compile(expr, re.UNICODE)
# Note that since _all_string_prefixes includes the empty string,
# StringPrefix can be the empty string (making it optional).
StringPrefix = group(*_all_string_prefixes())
# Tail end of ' string.
Single = r"[^'\\]*(?:\\.[^'\\]*)*'"
# Tail end of " string.
Double = r'[^"\\]*(?:\\.[^"\\]*)*"'
# Tail end of ''' string.
Single3 = r"[^'\\]*(?:(?:\\.|'(?!''))[^'\\]*)*'''"
# Tail end of """ string.
Double3 = r'[^"\\]*(?:(?:\\.|"(?!""))[^"\\]*)*"""'
Triple = group(StringPrefix + "'''", StringPrefix + '"""')
# Single-line ' or " string.
String = group(StringPrefix + r"'[^\n'\\]*(?:\\.[^\n'\\]*)*'",
 StringPrefix + r'"[^\n"\\]*(?:\\.[^\n"\\]*)*"')
# Because of leftmost-then-longest match semantics, be sure to put the
# longest operators first (e.g., if = came before ==, == would get
# recognized as two instances of =).
Operator = group(r"\*\*=?", r">>=?", r"<<=?", r"!=",
 r"//=?", r"->",
 r"[+\-*/%&@|^=<>]=?",
 r"~")
Bracket = '[][(){}]'
Special = group(r'\r?\n', r'\.\.\.', r'[:;.,@]')
Funny = group(Operator, Bracket, Special)
PlainToken = group(Number, Funny, String, Name)
Token = Ignore + PlainToken
# First (or only) line of ' or " string.
ContStr = group(StringPrefix + r"'[^\n'\\]*(?:\\.[^\n'\\]*)*" +
 group("'", r'\\\r?\n'),
 StringPrefix + r'"[^\n"\\]*(?:\\.[^\n"\\]*)*' +
 group('"', r'\\\r?\n'))
PseudoExtras = group(r'\\\r?\n|\Z', Comment, Triple)
PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
# For a given string prefix plus quotes, endpats maps it to a regex
# to match the remainder of that string. _prefix can be empty, for
# a normal single or triple quoted string (with no prefix).
endpats = {}
for _prefix in _all_string_prefixes():
 endpats[_prefix + "'"] = Single
 endpats[_prefix + '"'] = Double
 endpats[_prefix + "'''"] = Single3
 endpats[_prefix + '"""'] = Double3
# A set of all of the single and triple quoted string prefixes,
# including the opening quotes.
single_quoted = set()
triple_quoted = set()
for t in _all_string_prefixes():
 for u in (t + '"', t + "'"):
 single_quoted.add(u)
 for u in (t + '"""', t + "'''"):
 triple_quoted.add(u)
tabsize = 8
class TokenError(Exception): pass
class StopTokenizing(Exception): pass
class Untokenizer:
 def __init__(self):
 self.tokens = []
 self.prev_row = 1
 self.prev_col = 0
 self.encoding = None
 def add_whitespace(self, start):
 row, col = start
 if row < self.prev_row or row == self.prev_row and col < self.prev_col:
 raise ValueError("start ({},{}) precedes previous end ({},{})"
 .format(row, col, self.prev_row, self.prev_col))
 row_offset = row - self.prev_row
 if row_offset:
 self.tokens.append("\\\n" * row_offset)
 self.prev_col = 0
 col_offset = col - self.prev_col
 if col_offset:
 self.tokens.append(" " * col_offset)
 def untokenize(self, iterable):
 it = iter(iterable)
 indents = []
 startline = False
 for t in it:
 if len(t) == 2:
 self.compat(t, it)
 break
 tok_type, token, start, end, line = t
 if tok_type == ENCODING:
 self.encoding = token
 continue
 if tok_type == ENDMARKER:
 break
 if tok_type == INDENT:
 indents.append(token)
 continue
 elif tok_type == DEDENT:
 indents.pop()
 self.prev_row, self.prev_col = end
 continue
 elif tok_type in (NEWLINE, NL):
 startline = True
 elif startline and indents:
 indent = indents[-1]
 if start[1] >= len(indent):
 self.tokens.append(indent)
 self.prev_col = len(indent)
 startline = False
 self.add_whitespace(start)
 self.tokens.append(token)
 self.prev_row, self.prev_col = end
 if tok_type in (NEWLINE, NL):
 self.prev_row += 1
 self.prev_col = 0
 return "".join(self.tokens)
 def compat(self, token, iterable):
 indents = []
 toks_append = self.tokens.append
 startline = token[0] in (NEWLINE, NL)
 prevstring = False
 for tok in chain([token], iterable):
 toknum, tokval = tok[:2]
 if toknum == ENCODING:
 self.encoding = tokval
 continue
 if toknum in (NAME, NUMBER):
 tokval += ' '
 # Insert a space between two consecutive strings
 if toknum == STRING:
 if prevstring:
 tokval = ' ' + tokval
 prevstring = True
 else:
 prevstring = False
 if toknum == INDENT:
 indents.append(tokval)
 continue
 elif toknum == DEDENT:
 indents.pop()
 continue
 elif toknum in (NEWLINE, NL):
 startline = True
 elif startline and indents:
 toks_append(indents[-1])
 startline = False
 toks_append(tokval)
def tokenize(readline):
 # This import is here to avoid problems when the itertools module is not
 # built yet and tokenize is imported.
 from itertools import chain, repeat
 encoding, consumed = detect_encoding(readline)
 rl_gen = iter(readline, b"")
 empty = repeat(b"")
 return _tokenize(chain(consumed, rl_gen, empty).__next__, encoding)
def _tokenize(readline, encoding):
 lnum = parenlev = continued = 0
 numchars = '0123456789'
 contstr, needcont = '', 0
 contline = None
 indents = [0]
 while True: # loop over lines in stream
 try:
 # We capture the value of the line variable here because
 # readline uses the empty string '' to signal end of input,
 # hence `line` itself will always be overwritten at the end
 # of this loop.
 last_line = line
 line = readline()
 except StopIteration:
 line = b''
 if encoding is not None:
 line = line.decode(encoding)
 lnum += 1
 pos, max = 0, len(line)
 elif parenlev == 0 and not continued: # new statement
 if not line: break
 column = 0
 while pos < max: # measure leading whitespace
 if line[pos] == ' ':
 column += 1
 elif line[pos] == '\t':
 column = (column//tabsize + 1)*tabsize
 elif line[pos] == '\f':
 column = 0
 else:
 break
 pos += 1
 if pos == max:
 break
 if column > indents[-1]: # count indents or dedents
 indents.append(column)
 yield TokenInfo(INDENT, line[:pos], (lnum, 0), (lnum, pos), line)
 while column < indents[-1]:
 if column not in indents:
 raise IndentationError(
 "unindent does not match any outer indentation level",
 ("<tokenize>", lnum, pos, line))
 indents = indents[:-1]
 yield TokenInfo(DEDENT, '', (lnum, pos), (lnum, pos), line)
 else: # continued statement
 if not line:
 raise TokenError("EOF in multi-line statement", (lnum, 0))
 continued = 0
 while pos < max:
 pseudomatch = _compile(PseudoToken).match(line, pos)
 if pseudomatch: # scan for tokens
 start, end = pseudomatch.span(1)
 spos, epos, pos = (lnum, start), (lnum, end), end
 if start == end:
 continue
 token, initial = line[start:end], line[start]
 if (initial in numchars or # ordinary number
 (initial == '.' and token != '.' and token != '...')):
 yield TokenInfo(NUMBER, token, spos, epos, line)
 elif initial in '\r\n':
 if parenlev > 0:
 yield TokenInfo(NL, token, spos, epos, line)
 else:
 yield TokenInfo(NEWLINE, token, spos, epos, line)
 elif initial == '#':
 assert not token.endswith("\n")
 yield TokenInfo(COMMENT, token, spos, epos, line)
 elif token in triple_quoted:
 endprog = _compile(endpats[token])
 endmatch = endprog.match(line, pos)
 if endmatch: # all on one line
 pos = endmatch.end(0)
 token = line[start:pos]
 yield TokenInfo(STRING, token, spos, (lnum, pos), line)
 else:
 strstart = (lnum, start) # multiple lines
 contstr = line[start:]
 contline = line
 break
def main():
 import argparse
 # Helper error handling routines
 def perror(message):
 print(message, file=sys.stderr)
 def error(message, filename=None, location=None):
 if location:
 args = (filename,) + location + (message,)
 perror("%s:%d:%d: error: %s" % args)
 elif filename:
 perror("%s: error: %s" % (filename, message))
 else:
 perror("error: %s" % message)
 sys.exit(1)
