#encoding:utf-8
"""Naval Fate.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.

"""
#from __future__ import unicode_literals
#__author__ = 'meng'
##from zhizhu.fs23 import Fs23
#
#
#import argparse
#
#
#def parse_arguments():
#    parse = argparse.ArgumentParser(description="小说爬虫的一个命令行工具",
#                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#
#    parse.add_argument('-c','--config',dest="config",action="store",help = "配置文件")
#
#    return parse.parse_args()
#
#def main():
#    args = parse_arguments()
#    print args
#
#
#from docopt import docopt
#
#
if __name__ == '__main__':
#    arguments = docopt(__doc__, version='Naval Fate 2.0')
#    print(arguments)
    import config
    print '22mt' in config.type