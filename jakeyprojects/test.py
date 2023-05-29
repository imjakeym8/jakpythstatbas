import os
import threading
import time
from combotencodebot import GsheetEncoder

#THREADING DOESN'T WORK BECAUSE IT REACHES QUOTA LIMIT (FREE ACCOUNT)

starting = time.perf_counter()

dic_path = 'jakeyprojects/combot_communities'
file = os.listdir(dic_path)

def encode(path, sheet, worksheet, bool=False):
    ge = GsheetEncoder(path, sheet, worksheet, do_format=bool)
    ge.start(3,1, "monthly")

sheetnum = 3
for each_file in file:
    my_path = f"{dic_path}/{each_file}"
    encode(my_path, "TestingSheets", f"Sheet{sheetnum}")
    sheetnum += 1

#sheetnum = 3
#threads = []
#for each_file in file:
#    my_path = f"{dic_path}/{each_file}"
#    args = (my_path, "TestingSheets", f"Sheet{sheetnum}")
#    t = threading.Thread(target=encode, args=args)
#    threads.append(t)
#    sheetnum += 1
#
#for thread in threads:
#    thread.start()
#
#for thread in threads:
#    thread.join()

ending = time.perf_counter()
print(f"Elapsed time: {(ending-starting):.4f} seconds")