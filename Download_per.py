from time import sleep
from tqdm import tqdm
import time

elapsed = []

def download_per(total, file_num):
    with tqdm(range(total)) as pbar:
        pbar.postfix = str(file_num)
        pbar.update(file_num*100)
