import pickle

def load():
    try:
        with open("bot_info.pkl", 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

info = load()

def store():
    global info
    print(info)
    with open("bot_info.pkl", 'wb') as f:
        pickle.dump(info, f)


