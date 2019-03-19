#!/usr/bin/env python3
import argparse
import threading
import queue
import itertools
import datetime
import logging


class Derivator:
    def __init__(self, filename, complexmode):
        self.filename = filename
        self.complex = complexmode
        self.leet = {"a": "4", "b": "8", "e": "3", "g": "6", "i": "1", "l": "1", "o": "0", "r": "2", "s": "5", "t": "7", "y": "7", "z": "2"}

    def run(self):
        """ Loop until queue is empty """
        while True:
            self.w = q.get()
            self.r = []
            logging.info("Starting derivation for '{}'".format(self.w))
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
            wnumber = self.addUsualNumbers(w)
            self.extend(wnumber)
            wchar = self.addSomeChar(w)
            self.extend(wchar)

            for wc in wchar:
                self.extend(self.addUsualNumbers(wc))

            for wn in wnumber:
                self.extend(self.addSomeChar(wn))

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

    if args.quiet:
        loglevel = logging.FATAL
    else:
        loglevel = logging.DEBUG if args.verbose else logging.INFO

    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    logging.info("----------------------------------------------------------")
    logging.info("WDerivator v1.0")
    logging.info("Author : Aviso")
    logging.info("Last update : 12-2016")
    logging.info("GitHub : https://github.com/Aviso-hub/wderivator")
    logging.info("----------------------------------------------------------")
    logging.info("Starting WDerivator with {} threads".format(args.threads))

    q = queue.Queue()
    mutex = threading.Lock()
    logging.debug("Initializing queue")
    [q.put(_) for _ in args.words]
    logging.debug("Initializing done")

    start = datetime.datetime.now()
    for thrd in range(args.threads):
        logging.debug("Starting thread {}".format(thrd))
        derivator = Derivator(args.output, args.complex)
        t = threading.Thread(target=derivator.run)
        t.daemon = True
        t.start()

    q.join()
    logging.info("WDerivator end (time elapsed {})".format(datetime.datetime.now() - start))
