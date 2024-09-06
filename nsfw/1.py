import pathlib

# На Windows путь будет что-то вроде:
# D:\\user\\images
path = pathlib.Path("/home/consy/Neko-bot/nsfw/")
for i, path in enumerate(path.glob('*.jpg')):
    new_name = str(i) + '.jpg'
    path.rename(new_name)
