from time import sleep
import time
from tqdm import tqdm
import sys

elapsed = []

def download_per(pbar, repo,total, file_num):
    pbar.set_postfix({"file_num": file_num}, refresh=True)
    pbar.n = file_num*100
    pbar.refresh()