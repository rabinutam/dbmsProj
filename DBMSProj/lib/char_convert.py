
import binascii
import re


def ascii_to_binary(ascii_text):
    binary = bin(int(binascii.hexlify(ascii_text), 16))
    return binary

def binary_to_ascii(binary):
    n = int(binary, 2)
    #hex_format = hex(n)[2:] # take out 0x at start = <'%x' % n>
    hex_format = '%x' % n # this is more robust, take accoint of long
    ascii_text = binascii.unhexlify(hex_format)
    return ascii_text

def ascii_list_to_binary(ascii_list=None):
    '''
    **Example ascii_list**
        [ 
            'id, name, age, gender',
            '1, mike,  22, M',
            '2, rita,  24, F'
        ]
    '''
    datax = ascii_list
    binary = ascii_to_binary(datax[0])
    for di in datax[1:]:
        add_b = ascii_to_binary(di)
        if re.match('^\d.*', di):
            add_b = add_b[:2] + '0' + add_b[2:]
        add_b = re.sub('^0b', '0', add_b)
        binary += add_b
    return binary


if __name__ == '__main__':
    def test_conversion():
        # orig_text = 'hello'
        orig_text = 'cat domestic mammal|lion wild mammal'
        binary = ascii_to_binary(orig_text)
        print binary
        ascii_text = binary_to_ascii(binary)
        print ascii_text
        assert ascii_text == orig_text, '{0} != {1}'.format(ascii_text, orig_text)

    def test_mult_data():
        '''
        head = id, name, age, gender
        row1 =  1, mike,  22, M
        row2 =  2, rita,  24, F
        '''
        data = ['c', 'a', 't'] # works
        data = ['co', 'ba', 'lt'] # works
        data = ['coal, graphite', 'barn, farm', 'ltd, llc'] # works
        datax = [ # now works, does not work, if number in the beginnging
                'id, name, age, gender',
                '1, mike,  22, M',
                '2, rita,  24, F'
                ]
        data = [ # works without numbers
                'name, email',
                'rob, rob@gmail.com',
                'robi, robi@gmail.com',
                'robin, robin@gmail.com']
        data = [ # works without numbers at the beginning
                'name, email, age',
                'rob, rob@gmail.com, 22',
                'robi, robi@gmail.com, 24',
                'robin, robin@gmail.com, 26']

        binary = ascii_list_to_binary(datax)
        print binary
        ascii_text = binary_to_ascii(binary)
        print ascii_text


    #test_conversion()
    test_mult_data()
