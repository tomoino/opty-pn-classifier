import MeCab

def main():
    sentence = "今日は楽しくて良い一日だった。ランチに行ったお店がとても美味しかった。"

    result = MeCab.Tagger()
    words = [value.split(',') for value in result.parse(sentence).split('\n')]
    basic_form = [value[6] for value in words if len(value) > 7]
    print(basic_form)

if __name__ == "__main__":
    main()