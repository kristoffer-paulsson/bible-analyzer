import csv

from bibleanalyzer.util.transliterator import KoineTransliterator

if __name__ == '__main__':
    tdnt_list = dict()

    for line in open("./corpus/meta/TDNT-wordlist.txt", "r"):
        try:
            line = line.strip()
            tdnt_list[KoineTransliterator.latinize(KoineTransliterator.normalize(line))] = line
        except KeyError:
            pass

    keys = tdnt_list.keys()
    tdnt = list()
    phrases = list()
    for row in csv.reader(open("./corpus/meta/wordlist.csv", "r")):
        try:
            lemma = KoineTransliterator.latinize(KoineTransliterator.normalize(row[0]))
            if lemma in keys:
                tdnt.append(tdnt_list[lemma])
                if len(tdnt) > 300:
                    break
            else:
                phrases.append(row[0])
        except KeyError:
            pass

    # tdnt_set = set(tdnt[:300])
    # phrases_set = set(phrases[:300])

    cnt = 0
    print("# Common Phrases")
    for word in phrases:
        cnt += 1
        print(word)
        if not cnt % 10:
            print("\n")

    cnt = 0
    print("# TDNT Phrases")
    for tdnt_word in tdnt:
        cnt += 1
        print(tdnt_word)
        if not cnt % 10:
            print("\n")


