from tqdm import tqdm


def download_per(total, file_num):
    with tqdm(total=total, initial=file_num*100, postfix=str(file_num)) as pbar:
        pass