#!/usr/bin/env python

import sys
import argparse
import json
import datetime
import certifi

try:
    from urllib import urlencode
    from urllib2 import Request, urlopen, HTTPError, URLError
except:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen, HTTPError, URLError


def main():
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50),
                                     description='Get or refresh an access token for your Tesla car.')

    parser.add_argument("-o", "--output", metavar='FILE', default=None, help="Write to file FILE (json format)")
    parser.add_argument("-u", "--username", metavar='USER', default=None, help="Username for your MyTesla account")
    parser.add_argument("-p", "--password", metavar='PASS', default=None, help="Password for your MyTesla account")
    parser.add_argument("-r", "--refresh", metavar='REFRESH_TOKEN', default=None, help="Refresh token for an access token")
    parser.add_argument("-q", "--quiet", action='store_true', help="Do not print token to stdout")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        exit(1)

    if args.quiet and args.output is None:
        error('--quiet can only be combined with --output')

    resp = urlopen(Request('https://pastebin.com/raw/YiLPDggh'), cafile = certifi.where()).read()
    client_data = json.loads(b'{'+resp.rstrip(b',')+b'}')

    headers = {'client_id': client_data['OWNERAPI_CLIENT_ID']}

    if args.username and args.password:
        headers.update({'grant_type': 'password', 'email': args.username, 'password': args.password})
        headers.update({'client_secret': client_data['OWNERAPI_CLIENT_SECRET']})
    elif args.refresh:
        headers.update({'grant_type': 'refresh_token', 'refresh_token': args.refresh})
    else:
        error('Either username/password or refresh token must be provided.')

    try:
        request = Request('https://owner-api.teslamotors.com/oauth/token', data=urlencode(headers).encode('utf-8'))
        response = json.loads(urlopen(request, cafile = certifi.where()).read())
    except HTTPError as err:
        error('An HTTP error occurred during authorization: %d: %s' % (err.code, err.msg))
    except URLError as err:
        error('An URL error occurred during authorization: %s' % err.reason)

    if not args.quiet:
        print('\n')
        print(' Access Token: %s' % response['access_token'])
        print('Refresh Token: %s' % response['refresh_token'])
        print(' Requested at: %s' % readable_time(response['created_at']))
        print('   Expires at: %s' % readable_time((response['created_at'] + response['expires_in'])))

    if args.output:
        with open(args.output, 'w') as outfile:
            json.dump(response, outfile, sort_keys=True, indent=2)
        print('\nAccess token written to %s' % args.output)


def readable_time(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


def error(msg):
    print('ERROR: %s' % msg)
    exit(1)

if __name__ == "__main__":
    main()
