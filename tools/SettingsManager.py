import yaml
import sys


class SettingsManager(object):
    """
    Settings manager.
    """

    def loadSettings(self):
        """
        Loading settings file.

        :param path:
            The path.

        :return:
        """
        stream = open(sys.path[0] + "/settings.yml", "r")
        return yaml.load(stream)
