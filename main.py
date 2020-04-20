import MeCab
import pickle

def convert_to_basic_form(request):
    tagger = MeCab.Tagger()
    words = [value.split(',') for value in tagger.parse(request).split('\n')]
    basic_form = [value[6] for value in words if len(value) > 7]
    return basic_form

def make_pn_dict():
    tagger = MeCab.Tagger()
    pn_dict = {}

    # 用言ファイル読み込み
    path = 'pn.txt'
    with open(path) as f:
        pn_file = f.readlines()
    
    # 辞書に格納
    for line in pn_file:
        line = line.replace('\n','').replace(' ','').split('\t')
        basic_form = convert_to_basic_form(line[1])
        # 基本形が取得できない行については無視
        if not basic_form:
            continue
        key = basic_form[0]
        if key not in pn_dict:
            pn_dict[key] = []
        pn_dict[key].append([(',').join(basic_form), 1 if 'ポジ' in line[0] else - 1])
        
    # 名詞ファイル読み込み
    noun_path = 'pn_noun.txt'
    with open(noun_path) as f:
        pn_noun_file = f.readlines()

    # 辞書に格納
    for line in pn_noun_file:
        line = line.replace('\n', '').split('\t')
        if line[1] == 'e': # ポジティブでもネガティブでもない行は無視
            continue
        basic_form = convert_to_basic_form(line[0])
        # 基本形が取得できない行については無視
        if not basic_form:
            continue
        key = basic_form[0]
        if key not in pn_dict:
            pn_dict[key] = []
        pn_dict[key].append([(',').join(basic_form), 1 if line[1] == 'p' else - 1])

    print(pn_dict)
    pickle.dump(pn_dict, open('pn.pkl', 'wb'), protocol=2)

def main():
    request = "今日は楽しくて良い一日だった。ランチに行ったお店がとても美味しかった。"
    basic_form = convert_to_basic_form(request)
    print(basic_form)

    # PN判定：単語をkeyにして、登録されてる単語列とPN値を取得する
    # PN_DICT:key = 1文節目かつ助詞以外の単語、value = [[単語列(,で接続),pn]]
    pn_dict = pickle.load(open('pn.pkl', 'rb'))
    print(pn_dict)

if __name__ == "__main__":
    main()
    # make_pn_dict()