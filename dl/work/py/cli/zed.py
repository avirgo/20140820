Type "help", "copyright", "credits" or "license" for more information.
>>> import argparse
>>> import ConfigParser
>>> import sys
>>> 
>>> conf_parser = argparse.ArgumentParser(
...         description=__doc__, # printed with -h/--help
...         # Don't mess with format of description
...         formatter_class=argparse.RawDescriptionHelpFormatter,
...         # Turn off help, so we print all options in response to -h
...         add_help=False
...         )
>>> conf_parser.add_argument("-c", "--conf_file",
...                         help="Specify config file", metavar="FILE")
_StoreAction(option_strings=['-c', '--conf_file'], dest='conf_file', nargs=None, const=None, default=None, type=None, choices=None, help='Specify config file', metavar='FILE')
>>> conf_parser.add_argument("org",
...                         help="Specify 'org' section in config file", type=str, default="Defaults")
_StoreAction(option_strings=[], dest='org', nargs=None, const=None, default='Defaults', type=<type 'str'>, choices=None, help="Specify 'org' section in config file", metavar=None)
>>> 
>>> conf_parser.print_help
<bound method ArgumentParser.print_help of ArgumentParser(prog='', usage=None, description=None, version=None, formatter_class=<class 'argparse.RawDescriptionHelpFormatter'>, conflict_handler='error', add_help=False)>
>>> dir(conf_parser)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_action_groups', '_actions', '_add_action', '_add_container_actions', '_check_conflict', '_check_value', '_defaults', '_get_args', '_get_formatter', '_get_handler', '_get_kwargs', '_get_nargs_pattern', '_get_option_tuples', '_get_optional_actions', '_get_optional_kwargs', '_get_positional_actions', '_get_positional_kwargs', '_get_value', '_get_values', '_handle_conflict_error', '_handle_conflict_resolve', '_has_negative_number_optionals', '_match_argument', '_match_arguments_partial', '_mutually_exclusive_groups', '_negative_number_matcher', '_option_string_actions', '_optionals', '_parse_known_args', '_parse_optional', '_pop_action_class', '_positionals', '_print_message', '_read_args_from_files', '_registries', '_registry_get', '_remove_action', '_subparsers', 'add_argument', 'add_argument_group', 'add_help', 'add_mutually_exclusive_group', 'add_subparsers', 'argument_default', 'conflict_handler', 'convert_arg_line_to_args', 'description', 'epilog', 'error', 'exit', 'format_help', 'format_usage', 'format_version', 'formatter_class', 'fromfile_prefix_chars', 'get_default', 'parse_args', 'parse_known_args', 'prefix_chars', 'print_help', 'print_usage', 'print_version', 'prog', 'register', 'set_defaults', 'usage', 'version']
>>> conf_parser.print_help()
usage: [-c FILE] org

positional arguments:
  org                   Specify 'org' section in config file

optional arguments:
  -c FILE, --conf_file FILE
                        Specify config file
>>> conf_parser.parse_known_args(['-c', 'c', 'cms-poc'])
(Namespace(conf_file='c', org='cms-poc'), [])
>>> args, rem = conf_parser.parse_known_args(['-c', 'c', 'cms-poc'])
>>> args
Namespace(conf_file='c', org='cms-poc')
>>> args.conf_file
'c'
>>> args.org
'cms-poc'
>>> config = ConfigParser.SafeConfigParser()
>>> config.read([args.conf_file])
['c']
>>> config
<ConfigParser.SafeConfigParser instance at 0x7f297ec0b6c8>
>>> dir(config)
['OPTCRE', 'SECTCRE', '_KEYCRE', '__doc__', '__init__', '__module__', '_boolean_states', '_defaults', '_dict', '_get', '_interpolate', '_interpolate_some', '_interpolation_replace', '_interpvar_re', '_read', '_sections', 'add_section', 'defaults', 'get', 'getboolean', 'getfloat', 'getint', 'has_option', 'has_section', 'items', 'options', 'optionxform', 'read', 'readfp', 'remove_option', 'remove_section', 'sections', 'set', 'write']
>>> config.sections
<bound method SafeConfigParser.sections of <ConfigParser.SafeConfigParser instance at 0x7f297ec0b6c8>>
>>> config.sections.count
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'function' object has no attribute 'count'
>>> config.sections()
['cms-poc', 'ukcms-poc', 'cms-sandbox', 'Defaults']
>>> dict(config.items(args.org))
{'basicauth': 'YW50aG9ueS52aXJnb0BwZWFyc29uLmNvbUBjbXMtcG9jOlRvbnlfVmlyZzAyCg==', 'server': 'icd-mystack.pearson.com'}
>>> parser = argparse.ArgumentParser( parents=[conf_parser] )
>>> defs = dict(config.items(args.org))
>>> parser.set_defaults(**defs)
>>> parser.add_argument("--basicauth")
_StoreAction(option_strings=['--basicauth'], dest='basicauth', nargs=None, const=None, default='YW50aG9ueS52aXJnb0BwZWFyc29uLmNvbUBjbXMtcG9jOlRvbnlfVmlyZzAyCg==', type=None, choices=None, help=None, metavar=None)
>>> parser.add_argument("--server")
_StoreAction(option_strings=['--server'], dest='server', nargs=None, const=None, default='icd-mystack.pearson.com', type=None, choices=None, help=None, metavar=None)
>>> parser.parse_args(rem)
usage: [-h] [-c FILE] [--basicauth BASICAUTH] [--server SERVER] org
: error: too few arguments
