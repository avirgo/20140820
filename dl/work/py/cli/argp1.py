import argparse
import ConfigParser
import sys

# Parse any conf_file specification
# We make this parser with add_help=False so that
# it doesn't parse -h and print help.
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
                        help="Specify org section in config file", type=str, default="Defaults")
args = conf_parser.parse_args()

args

if args.conf_file:
        config = ConfigParser.SafeConfigParser()
        config.read([args.conf_file])
        defaults = dict(config.items("Defaults"))
else:
        defaults = { "option":"default" }
dir(defaults)
dir(args)
dir()
