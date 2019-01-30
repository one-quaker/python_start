import os
import sys


# print(os.listdir())
if sys.platform == 'darwin':
    print('Hello Mac!')
elif sys.platform == 'win32':
    print('Dude, install linux or mac :)')
elif 'linux' in sys.platform:
    print('Linux rulez! pew pew')
else:
    print('Unknown operating system')


current_dir = os.getcwd()


for i in range(20):
    newdir_path = os.path.join(current_dir, 'test_{0:02d}'.format(i))
    # print(current_dir, newdir_path)
    if not os.path.isdir(newdir_path):
        os.mkdir(newdir_path)


for path in os.listdir(current_dir):
    if os.path.isdir(path) and 'test_' in path:
        print(path)
