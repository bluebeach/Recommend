__author__ = 'blue'
import time

def test():
    return 0

if __name__ == '__main__':
    start = time.clock()
    # print('hahahahahahahaha')
    # test_file_name = '../ml-100k/u.info'
    # with open(test_file_name) as file:
    #     for line in file:
    #         print(line, end='')
    time.sleep(2)
    end = time.clock()
    print('pass : ', round(end - start, 1))




