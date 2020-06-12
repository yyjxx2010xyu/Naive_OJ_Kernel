from ctypes import *

a=input().split()
mem = create_string_buffer(1024*1024*1024)

print(int(a[0])+int(a[1]))