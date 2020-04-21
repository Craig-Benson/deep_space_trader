import os
import json

from deep_space_trader.utils import errorDialog, scores_encode, scores_decode


FILENAME = os.path.join(os.path.expanduser('~'), '.deep_space_trader_config.json')


SCORES_KEY = 'highscores'

config = {
    SCORES_KEY: []
}


def _malformed_config():
    errorDialog(None, "Error", message="Malformed config file: %s" % FILENAME)


def config_load():
    if not os.path.isfile(FILENAME):
        return

    try:
        with open(FILENAME, 'r') as fh:
            loaded = json.load(fh)
    except:
        _malformed_config()
        return

    try:
        if loaded[SCORES_KEY] == '':
            config[SCORES_KEY] = []
        else:
            data = scores_decode(loaded[SCORES_KEY]).decode('utf-8')
            config[SCORES_KEY] = json.loads(data)
    except:
        _malformed_config()
        return

def config_store():
    cfg = {}

    if config[SCORES_KEY]:
        string = json.dumps(config[SCORES_KEY])
        encoded = scores_encode(bytes(string, encoding='utf8')).decode('utf-8')
    else:
        encoded = ''

    cfg[SCORES_KEY] = encoded

    try:
        with open(FILENAME, 'w') as fh:
            json.dump(cfg, fh)
    except:
        errorDialog(None, "Error", message="Unable to write file %s" % FILENAME)

def add_highscore(name, score):
    config['highscores'].append([name, score])
    config['highscores'].sort(key=lambda x: x[1])
    config['highscores'].reverse()

def highscores():
    return config['highscores']
