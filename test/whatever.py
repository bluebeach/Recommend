__author__ = 'blue'

def test():
    return 0

if __name__ == '__main__':
    print('hahahahahahahaha')
    test_file_name = '../ml-100k/u.info'
    with open(test_file_name) as file:
        for line in file:
            print(line, end='')



