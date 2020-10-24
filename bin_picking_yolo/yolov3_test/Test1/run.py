#import getMongodb
import re


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

str = 'C:\\Users\david9613\Desktop\OE\MasterThesis\\bin_picking_project-development_0206\\bin_picking_project-development\\PythonClient\\image_set\\2020_02_06_15_47_54.jpg'
vmi = re.search("david9613",str)
beg='image_set\\'
#print(begIndex)
end='.jpg'
#print(endIndex)
#print(len(str))
#print(str[begIndex,endIndex,endIndex-begIndex])
out = find_between(str, beg, end)
print(out)
