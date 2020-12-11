import ast
import astor
import astpretty

tree = astor.parse_file('pullupmethodclass.py')
astpretty.pprint(tree)

import FindHelper as fh

# print ([astor.to_source(x) for x in fh.find_all_fields(tree)])

code = "self.name = None"
astpretty.pprint(ast.parse(code))
