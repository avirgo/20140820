import argparse
import ConfigParser
import sys

conf_parser = argparse.ArgumentParser(
        description=__doc__, # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Turn off help, so we print all options in response to -h
        add_help=False
        )
conf_parser.add_argument("-c", "--conf_file",
                        help="Specify config file", metavar="FILE")
conf_parser.add_argument("org",
                        help="Specify 'org' section in config file", type=str, default="Defaults")

conf_parser.parse_known_args(['-c', 'c', 'cms-poc'])
args, rem = conf_parser.parse_known_args(['-c', 'c', 'cms-poc'])
args
config = ConfigParser.SafeConfigParser()
config.read([args.conf_file])
dict(config.items(args.org))
parser = argparse.ArgumentParser( )
defs = dict(config.items(args.org))
parser.set_defaults(**defs)
parser.add_argument("--basicauth")
parser.add_argument("--server")
z = parser.parse_args(rem)
z
