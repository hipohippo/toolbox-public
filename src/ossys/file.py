import glob

def search(keyword:str):
    return glob.glob(fr"f:\books\*\*{keyword}*.epub", recursive=True)