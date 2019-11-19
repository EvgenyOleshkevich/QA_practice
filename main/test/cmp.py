import difflib
import sys
#prog, path1, path2  = sys.stdin.read().split() #split для удобства
_, path1, path2 = sys.argv.split() #split для удобства

file1 = open(path1, 'r')  # tyt nado ykazuvat to chto nakhoditsa pod somneniem
file2 = open(path2, 'r')  # tyt etalon
diff = difflib.ndiff(file1.readlines(), file2.readlines())
output(''.join(x for x in diff if x.startswith('- ')) == "")