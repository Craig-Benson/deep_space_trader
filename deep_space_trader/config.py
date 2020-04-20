import os
import json

from deep_space_trader.utils import errorDialog


FILENAME = os.path.join(os.path.expanduser('~'), '.deep_space_trader_config.json')


config = {
    'highscores': []
}


def _malformed_config():
    errorDialog(None, "Error", message="Malformed config file: %s" % FILENAME)

def config_is_valid(loaded, expected):
    # Check that all attribute names and data types match expected
    if len(loaded) != len(expected):
        return False

    for attrname in loaded:
        if attrname not in expected:
            return False

        if type(loaded) != type(expected):
            return False

    return True

def config_load():
    if not os.path.isfile(FILENAME):
        return

    try:
        with open(FILENAME, 'r') as fh:
            loaded = json.load(fh)
    except:
        _malformed_config()
        return

    if not config_is_valid(loaded, config):
        _malformed_config()
        return

    config.clear()
    config.update(loaded)

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
