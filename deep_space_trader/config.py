import os
import json

from deep_space_trader.utils import errorDialog


FILENAME = os.path.join(os.path.expanduser('~'), '.deep_space_trader_config.json')


config = {
    'highscores': []
}


def config_load():
    if not os.path.isfile(FILENAME):
        return

    try:
        with open(FILENAME, 'r') as fh:
            cfg = json.load(fh)
    except:
        errorDialog(None, "Error", message="Malformed config file: %s" % FILENAME)
        return

    config.clear()
    config.update(cfg)

def config_store():
    try:
        with open(FILENAME, 'w') as fh:
            json.dump(config, fh)
    except:
        errorDialog(None, "Error", message="Unable to write file %s" % FILENAME)

def add_highscore(name, score):
    config['highscores'].append([name, score])
    config['highscores'].sort(key=lambda x: x[1])
    config['highscores'].reverse()

def highscores():
    return config['highscores']
