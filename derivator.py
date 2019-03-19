#!/usr/bin/env python3
import argparse
import itertools
import datetime
import logging
import multiprocessing


def derivate_case(word):
    """
    Return a dict containaing all uppercase and lowercase combinations
    """
    logging.debug("Adding all uppercase and lowercase combinations for '{}'".format(word))
    return list(map(''.join, itertools.product(*zip(word.upper(), word.lower()))))


def derivate_leet(word):
    """
    Return a dict with all leet combinations
    """
    leet = {"a": "4", "b": "8", "e": "3", "g": "6", "i": "1", "l": "1", "o": "0", "r": "2", "s": "5", "t": "7", "y": "7", "z": "2"}
    return [''.join(letters) for letters in itertools.product(*({c, leet.get(c, c)} for c in word))]


def derivate_numbers(words):
    """
    Add usual numbers to strings
    """
    data = []

    for word in words:
        logging.debug("Adding usual numbers to '{}'".format(word))
        data.extend([
            word + "1",
            word + "123",
            word + "123456",
            "1" + word,
            "123" + word,
            "123456" + word
        ])

    return data


def derivate_chars(words):
    """
    Add usual characters to strings
    """
    data = []

    for word in words:
        logging.debug("Adding usual characters to '{}'".format(word))
        data.extend([
            word + "!",
            word + "@",
            word + "#",
            "!" + word,
            "@" + word,
            "#" + word
        ])

    return data


def derivate_date(word):
    """
    Add usual dates
    """
    logging.debug("Adding usual dates to '{}'".format(word))
    data = []

    for y in range(1950, datetime.datetime.now().year):
        data.extend([
            word + str(y),
            str(y) + word
        ])

    return data


class Derivator:
    def __init__(self, threads):
        self.data = list()
        self.thrds = list()
        self.pool = multiprocessing.Pool(threads)

    def extend(self, data):
        self.data.extend(data)

    def schedule(self, function, args, callback=None):
        self.thrds.append(self.pool.apply_async(function, args=args, callback=callback))

    def derivate(self, word, leet=False, date=False):
        self.data = list()
        logging.info("Starting derivation for '{}'".format(word))
        self.extend(derivate_case(word))

        if leet:
            self.extend(derivate_leet(word))

        if date:
            self.extend(derivate_date(word))

        for w in self.data:
            self.schedule(derivate_numbers, ([w],), callback=self.on_derivate_numbers_finished)
            self.schedule(derivate_chars, ([w],), callback=self.on_derivate_chars_finished)

        for thrd in self.thrds:
            self.extend(thrd.get())

        return list(set(self.data))

    def on_derivate_numbers_finished(self, data):
        for w in data:
            self.schedule(derivate_chars, ([w],))

    def on_derivate_chars_finished(self, data):
        for w in data:
            self.schedule(derivate_numbers, ([w],))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--words", help="Strings to generate wordlist", nargs="+", required=True)
    parser.add_argument("-o", "--output", help="File to output wordlist", required=True)
    parser.add_argument("-t", "--threads", help="Number of threads", default=5, type=int)
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("--leet", help="Generate leet passwords", action="store_true")
    parser.add_argument("--date", help="Add date to passwords", action="store_true")
    parser.add_argument("-q", "--quiet", help="Quiet mode", action="store_true")
    args = parser.parse_args()

    if args.quiet:
        loglevel = logging.FATAL
        logformat = None
    else:
        if args.verbose:
            loglevel = logging.DEBUG
            logformat = "%(asctime)s [%(threadName)-12.12s] [%(funcName)-18.18s] [%(levelname)-5.5s] %(message)s"
        else:
            loglevel = logging.INFO
            logformat = "%(asctime)s %(message)s"

    logging.basicConfig(
        level=loglevel,
        format=logformat,
        handlers=[
            logging.StreamHandler()
        ]
    )

    logging.info("----------------------------------------------------------")
    logging.info("WDerivator v1.1")
    logging.info("Author : Aviso")
    logging.info("Last update : 03-2019")
    logging.info("GitHub : https://github.com/Aviso-hub/wderivator")
    logging.info("----------------------------------------------------------")
    logging.info("Starting WDerivator with {} threads".format(args.threads))

    start = datetime.datetime.now()
    derivator = Derivator(args.threads)

    for w in args.words:
        data = derivator.derivate(w, args.leet, args.date)
        with open(args.output, 'a') as f:
            for item in data:
                f.write("{}\n".format(item))

        logging.info("{} password derivated.".format(len(data)))

    logging.info("WDerivator end (time elapsed {})".format(datetime.datetime.now() - start))
