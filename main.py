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
        # 基本形が取得できない行と基本形が1文字になる行については無視
        if not basic_form:
            continue
        elif len(basic_form) == 1 and len(basic_form[0]) == 1:
            continue
        key = basic_form[0]
        if key not in pn_dict:
            pn_dict[key] = {}
        pn_dict[key][(',').join(basic_form)] = 1 if 'ポジ' in line[0] else - 1
        
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
        # 基本形が取得できない行と基本形が1文字になる行については無視
        if not basic_form:
            continue
        elif len(basic_form) == 1 and len(basic_form[0]) == 1:
            continue
        key = basic_form[0]
        if key not in pn_dict:
            pn_dict[key] = {}
        pn_dict[key][(',').join(basic_form)] = 1 if line[1] == 'p' else - 1

    pickle.dump(pn_dict, open('pn.pkl', 'wb'), protocol=2)

# PN判定。リクエスト中の要素のPN値を足し合わせた値を返す。
def calc_pn(basic_form):
    pn_dict = pickle.load(open('pn.pkl', 'rb'))
    pn_values = [] # 文章内の各要素のPN判定の数値を格納
    pns = [] # debug用

    while basic_form:
        pn_value = 0
        del_num = 1  # リストから削除する件数
        beginning = basic_form[0] # 先頭の単語をkeyにする

        if beginning in pn_dict:
            for index, word in enumerate(basic_form):
                if word == "。" or word == "、":  #　文の句切れが来たら、中断する
                    break
                if index == 0:
                    joined_basic_forms = beginning
                else:
                    joined_basic_forms += ',' + word
                
                if joined_basic_forms in pn_dict[beginning]:
                    pn_value = pn_dict[beginning][joined_basic_forms]
                    del_num = index + 1

        pns.append(','.join(basic_form[0:del_num])+": "+str(pn_value))
        pn_values.append(pn_value)
        del basic_form[0:del_num]
    
    for v in pns:
        print(v)

    return sum(pn_values)

def main():
    request = "新型コロナウイルスが全国に感染を広げ、例えば、4月7日の時点で、東京都では感染者の累計が1,000人を超えるとともに、5日で2倍になるペースで感染者の増加が見られました。 また、感染経路が明らかにならない、いわゆる「孤発例」が増え、感染経路の"
    basic_form = convert_to_basic_form(request)
    pn = calc_pn(basic_form)
    print('PN = '+str(pn))

if __name__ == "__main__":
    main()