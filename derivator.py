#!/usr/bin/env python3
import argparse
import threading
import queue
import itertools
import datetime


class Logger:
    def __init__(self, verbosity, quiet):
        self.verbosity = verbosity
        self.quiet = quiet

    def log(self, str, force=False):
        if (not self.quiet and self.verbosity) or force:
            print("{}".format(str))


class Derivator:
    def __init__(self, logger, filename, complexmode=False):
        self.log = logger.log
        self.filename = filename
        self.complex = complexmode
        self.leet = {"a": "4", "b": "8", "e": "3", "g": "6", "i": "1", "l": "1", "o": "0", "r": "2", "s": "5", "t": "7", "y": "7", "z": "2"}

    def run(self):
        """ Loop until queue is empty """
        while True:
            self.w = q.get()
            self.r = []
            self.log("- Starting derivation for '{}'".format(self.w))
            self.derivate()
            self.saveToFile()
            q.task_done()

    def saveToFile(self):
        mutex.acquire()
        try:
            with open(self.filename, 'a') as f:
                for item in self.r:
                    f.write("{}\n".format(item))
        finally:
            mutex.release()

    def extend(self, data):
        self.r.extend(data)
        self.r = list(set(self.r))

    def derivate(self):
        self.extend(self.getUpperLower(self.w))

        if self.complex:
            self.extend(self.getLeet(self.r))

        for w in self.r:
            self.extend(self.addUsualNumbers(w))
            data = self.addSomeChar(w)
            self.extend(data)
            for sw in data:
                self.extend(self.addUsualNumbers(sw))

    def getUpperLower(self, s):
        """ Return a dict containaing all uppercase and lowercase combinations """
        return list(map(''.join, itertools.product(*zip(s.upper(), s.lower()))))

    def getLeet(self, s):
        """ Return a dict with all leet combinations """
        ret = []
        for word in s:
            ret.extend([''.join(letters) for letters in itertools.product(*({c, self.leet.get(c, c)} for c in word))])
        return ret

    def addUsualNumbers(self, s):
        """ Add some numbers to string """
        ret = []
        ret.append(s + "1")
        ret.append(s + "123")
        ret.append(s + "123456")
        ret.append("1" + s)
        ret.append("123" + s)
        ret.append("123456" + s)
        return ret

    def addSomeChar(self, s):
        """ Add some char """
        ret = []
        ret.append(s + "!")
        ret.append(s + "@")
        ret.append(s + "#")
        ret.append("!" + s)
        ret.append("@" + s)
        ret.append("#" + s)
        return ret


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--words", help="Strings to generate wordlist", nargs="+", required=True)
    parser.add_argument("-t", "--threads", help="Number of threads", default=1, type=int)
    parser.add_argument("-o", "--output", help="File to output wordlist", required=True)
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("-c", "--complex", help="Generate complex passwords", action="store_true")
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
    mutex = threading.Lock()
    logger.log("- Initializing queue")
    [q.put(_) for _ in args.words]
    logger.log("- Initializing done")

    start = datetime.datetime.now()
    logger.log("- Derivation start at {}".format(start.strftime('%H:%M:%S')), True)
    for thrd in range(args.threads):
        logger.log("- Starting thread {}".format(thrd))
        derivator = Derivator(logger, args.output)
        t = threading.Thread(target=derivator.run)
        t.daemon = True
        t.start()

    q.join()
    logger.log("+ Wordlist has been created in '{}'".format(args.output), True)
    logger.log("+ WDerivator end at {} (time elapsed {})".format(datetime.datetime.now().strftime('%H:%M:%S'), datetime.datetime.now() - start), True)
