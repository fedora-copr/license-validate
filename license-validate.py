#!/usr/bin/python3

class SolveBoolean:
   def solve(self, sentence, LICENSES):
      stack = []
      #debug_stack = []
      op = {
         "or": lambda x, y: x or y,
         "and": lambda x, y: x and y,
      }
      # FIXME this cause problem to e.g. "BSD with advertising"
      for word in sentence.split():
         count_trailing_parenthesis = word.count(")")
         if word[0] == "(":
            stack.append(word[word.count("(") :] in LICENSES)
            #debug_stack.append(word[count_trailing_parenthesis :])
         elif count_trailing_parenthesis > 0:
            stack.append(word[:-count_trailing_parenthesis] in LICENSES)
            #debug_stack.append(word[:-count_trailing_parenthesis])
            for _ in range(count_trailing_parenthesis):
               right = stack.pop()
               operator = stack.pop()
               left = stack.pop()
               stack.append(operator(left, right))
               #debug_stack.pop(); debug_stack.pop(); debug_stack.pop();
               #debug_stack.append(operator(left, right))
         elif word in op.keys():
            stack.append(op[word])
            #debug_stack.append("op_"+word)
         else:
            stack.append(word in LICENSES)
            #debug_stack.append(word)

      if len(stack) > 1:
         for i in range(0, len(stack) - 1, 2):
            stack[i + 2] = stack[i + 1](stack[i], stack[i + 2])
         return stack[-1]

      return stack[0]

GOOD_LICENSES = []

# TODO get the name of file from config and/or command line param
# keep this as default so we can run from checkout
with open('approved-licenses.txt','r') as fh:
     for curline in fh:
         if not curline.startswith("#"):
            curline = curline.rstrip()
            if curline: # skip whitespace lines
               GOOD_LICENSES.append(curline.rstrip())

print(GOOD_LICENSES)
ob = SolveBoolean()

# TODO read from command line using argparse
# TODO create testing set from all Fedora spec files
s = "MIT and (GPLv1 or BadOne)"
result = ob.solve(s, GOOD_LICENSES)

if not result:
   # not approved licesne
   sys.exit(1)

# TODO print something user friendly with -v 

