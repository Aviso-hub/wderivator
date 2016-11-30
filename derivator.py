#!/usr/bin/env python3
import argparse
import threading
import queue
import datetime


class Logger:
    def __init__(self, verbosity, quiet):
        self.verbosity = verbosity
        self.quiet = quiet

    def log(self, str, force=False):
        if (not self.quiet and self.verbosity) or force:
            print("{}".format(str))


class Derivator:
    def __init__(self, logger):
        self.log = logger.log

    def run(self):
        while True:
            self.w = q.get()
            self.log("- Starting derivation for '{}'".format(self.w))
            q.task_done()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--words", help="Strings to generate wordlist", nargs="+", required=True)
    parser.add_argument("-t", "--threads", help="Number of threads", default=1)
    parser.add_argument("-o", "--output", help="File to output wordlist", required=True)
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("-q", "--quiet", help="Quiet mode", action="store_true")
    args = parser.parse_args()

    logger = Logger(args.verbose, args.quiet)

    logger.log("----------------------------------------------------------", True)
    logger.log("- WDerivator v1.0", True)
    logger.log("- Author : Aviso", True)
    logger.log("- Last update : 12-2016", True)
    logger.log("- GitHub : https://github.com/Aviso-hub/wderivator", True)
    logger.log("----------------------------------------------------------\n", True)
    logger.log("+ Starting WDerivator with {} threads".format(args.threads), True)

    q = queue.Queue()
    logger.log("- Initializing queue")
    [q.put(_) for _ in args.words]
    logger.log("- Initializing done")

    start = datetime.datetime.now()
    logger.log("- Derivation start at {}".format(start.strftime('%H:%M:%S')), True)
    for thrd in range(args.threads):
        logger.log("- Starting thread {}".format(thrd))
        derivator = Derivator(logger)
        t = threading.Thread(target=derivator.run)
        t.daemon = True
        t.start()

    q.join()
    logger.log("+ Wordlist has been created in '{}'. It contain {} words".format(args.output, len(args.words) * 50), True)
    logger.log("+ WDerivator end at {} (time elapsed {})".format(datetime.datetime.now().strftime('%H:%M:%S'), datetime.datetime.now() - start), True)
