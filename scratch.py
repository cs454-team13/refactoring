import ast
import astor
import astpretty

tree = astor.parse_file('method_level_move.py')
astpretty.pprint(tree)
# tree = astor.parse_file('simpleClass.py')
# astpretty.pprint(tree)
CountryClass = tree.body[0]
KoreaClass = tree.body[1]
SouthKoreaClass = tree.body[2]

KoreaField = find_all_fields(KoreaClass)
print (KoreaField)
move_field(KoreaClass, CountryClass, KoreaField[0])
aftertree = astor.to_source(tree)
with open('refactored_simpleClass.py', 'w') as f:
    f.write(aftertree)

astpretty.pprint(SouthKoreaClass)
KoreaMethod = find_all_methods(KoreaClass)
print (KoreaMethod)
move_method(KoreaClass, CountryClass, KoreaMethod[0])
aftertree = astor.to_source(tree)
with open('refactored_simpleClass.py', 'w') as f:
    f.write(aftertree)

