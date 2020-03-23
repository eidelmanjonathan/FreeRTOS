#!/usr/bin/env python3
import json
import logging
import os
import subprocess

RECURSIVE_CHECKOUT_FAILED_MSG = "Failed to do a git checkout --recurse-submodules. Possible reason: submodule " \
                                "missing from this branch, or commit no longer exists"

def run_command(cmd, cwd=None):
    logging.info('Running "%s" in "%s"', ' '.join(cmd), cwd or '.')
    kwds = {'capture_output': True}
    if cwd:
        kwds['cwd'] = cwd
    result = subprocess.run(cmd, **kwds)
    debug = subprocess_data(cmd, cwd, result.stdout, result.stderr)
    logging.info(debug_json('subprocess', debug))
    result.check_returncode()

def checkout_recurse_submodules(srcdir, checkout):
    cmd = ['git', 'checkout', '--recurse-submodules', checkout]
    try:
        run_command(cmd, srcdir)
    except subprocess.CalledProcessError:
        logging.info(RECURSIVE_CHECKOUT_FAILED_MSG)
        return False
    return True

def subprocess_data(cmd, cwd, stdout, stderr):
    debug = {'cmd': ' '.join(cmd),
             'cwd': cwd,
             'stdout': stdout.decode("utf-8").splitlines(),
             'stderr': stderr.decode("utf-8").splitlines()
             }
    return debug

def debug_json(action, body):
    debug = {'script': os.path.basename(__file__),
             'action': action,
             'body': body}
    return json.dumps(debug)

if __name__ == "__main__":
    print("running!")