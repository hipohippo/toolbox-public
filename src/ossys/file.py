import glob


def search(keyword: str):
    return glob.glob(rf"f:\books\*\*{keyword}*.epub", recursive=True)
