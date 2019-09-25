import os
from configparser import ConfigParser
from optparse import OptionParser
from core.utils import load_json_file


def parse_args():
    usage = "usage: %prog [options] args"
    parser = OptionParser(usage)
    parser.add_option("-c", "--config", dest="configFile",
                      help="read data from configuration file")

    # parser.add_option("-n", "--number", dest="procNumber",
    #                   help="process number")

    (options, args) = parser.parse_args()
    ret = 0
    err_msg = ''
    if options.configFile is None:
        ret = -1
        err_msg = 'missing config file'

    return ret, err_msg, options, args


class Config:
    def __init__(self, config):
        self.config_file = config
        self.cfgMap = {}
        return

    def parse(self):
        cfg = ConfigParser()
        if os.path.exists(self.config_file):
            cfg.read(self.config_file, encoding='utf8')

        # build properties map for each section
        sections = cfg.sections()
        for section in sections:
            _props = {}
            for k, v in cfg.items(section):
                _props[k] = v
            self.cfgMap[section] = _props

        return self.cfgMap
