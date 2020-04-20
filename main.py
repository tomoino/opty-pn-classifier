import os
import yaml
import flask
import MeCab
import pickle


# yamlの読み込み
try:
    # local
    with open('./env.yaml') as f:
        os.environ.update(yaml.load(f))
except FileNotFoundError as e:
    # Google Cloud Functions
    pass

# 環境変数
FOO = os.getenv('FOO') # FIXME: サンプルです


def optimistic_analysis(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    targets = request_json['targets']
    scores = analyze(targets)
    return flask.jsonify({'scores': scores})

def analyze(targets):
    scores = []
    for target in targets:
        target_basic_formed = convert_to_basic_form(target)
        pn = calc_pn(target_basic_formed)
        scores.append(pn)
    return scores

def convert_to_basic_form(request):
    tagger = MeCab.Tagger()
    words = [value.split(',') for value in tagger.parse(request).split('\n')]
    basic_form = [value[6] for value in words if len(value) > 7]
    return basic_form

def make_pn_dict():
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

# PN判定。リクエスト中の要素のPN値の平均を返す。
def calc_pn(basic_form):
    pn_dict = pickle.load(open('pn.pkl', 'rb'))
    pn_values = [] # 文章内の各要素のPN判定の数値を格納

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

                if word == "ない" and del_num == index: # ポジネガ反転が必要
                    print('reverse')
                    pn_value *= -1
                    del_num = index + 1

                if joined_basic_forms in pn_dict[beginning]:
                    pn_value = pn_dict[beginning][joined_basic_forms]
                    del_num = index + 1

        pn_values.append(pn_value)
        del basic_form[0:del_num]

    return sum(pn_values) / len(pn_values)