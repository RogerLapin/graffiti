#!/usr/bin/env python

import argparse
import os
import time
import sys
from tqdm import trange
from graffiti import (Config,
                      Request,
                      Graph,
                      Report)

SPLASH = (''
          '                      _____  _____.__  __  .__\n'
          '   ________________ _/ ____\/ ____\__|/  |_|__|\n'
          '  / ___\_  __ \__  \\\\   __\\\\   __\|  \   __\  |\n'
          ' / /_/  >  | \// __ \|  |   |  |  |  ||  | |  |\n'
          ' \___  /|__|  (____  /__|   |__|  |__||__| |__|\n'
          '/_____/            \/\n\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Graffiti')
    parser.add_argument('--cfg', type=str, help='YAML configuration file')
    args = parser.parse_args()

    if not args.cfg:
        parser.print_help()
    elif (os.path.isfile(args.cfg)):
        sys.stdout.write(SPLASH)

        cfg = Config(args.cfg)
        report = Report()

        errors = []
        start = time.time()
        for i in trange(len(cfg.requests), desc='Requests'):
            req = Request.build(cfg.requests[i])
            req.run()

            if req.errors:
                errors += req.errors

            graph = Graph(req)
            graph.draw(cfg.imdir)

            report.add(graph)

        report.write(cfg.html, cfg.desc)

        # final log
        dur = round(time.time() - start, 1)
        n = 0
        for req in cfg.requests:
            n += req.iterations * len(req.hosts)

        if errors:
            errlog = os.path.join(cfg.logdir, 'errors.log')
            with open(errlog, 'w') as f:
                for error in errors:
                    f.write('--------\n')
                    f.write(error.tostr())

            sys.stdout.write('\nTerminated with some errors (see {}) in {} sec'
                             ' for {} requests!\n'
                             .format(errlog, dur, n))
            sys.exit(1)
        else:
            sys.stdout.write('\nTerminated without errors in {} sec for {} '
                             'requests!\n'
                             .format(dur, n))
    else:
        sys.stderr.write('Error: \'{}\' is not a valid configuration file.'
                         .format(args.cfg))
        sys.exit(1)

    sys.exit(0)
