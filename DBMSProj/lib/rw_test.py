
from array import array


def write():
    output_file = open('testb.tbl', 'wb')
    float_array = array('d', [3.14, 2.7, 0.0, -1.0, 1.1])
    float_array.tofile(output_file)
    output_file.close()

def read():
    input_file = open('testb.tbl', 'r')
    float_array = array('d')
    float_array.fromstring(input_file.read())
    print float_array

write()
read()
