# opty-pn-classifier

## 参考サイト
- [functions-framework-python](https://github.com/GoogleCloudPlatform/functions-framework-python)

## 使い方
- ローカル実行するためにfunction-framework-pythonをインストール: `pip install functions-framework`
- ローカルからデプロイするためにGoogle Cloud SDKをインストール: [macOS用](https://cloud.google.com/sdk/docs/quickstart-macos?hl=ja)
- cloud function: [optimistic_analysis](TODO:)
- ローカル起動: `functions-framework --target=optimistic_analysis`
- ローカルテスト: `curl -X POST -H "Content-Type: application/json" -d '{"targets": ["text1", "text2", "text3", "..."]}' http://0.0.0.0:8080/`
  - サンプル: `curl -X POST -H "Content-Type: application/json" -d '{"targets": ["新型コロナウイルスが全国に感染を広げ、例えば、4月7日の時点で、東京都では感染者の累計が1,000人を超えるとともに、5日で2倍になるペースで感染者の増加が見られました。 また、感染経路が明らかにならない、いわゆる「孤発例」が増え、感染経路の", "いい天気だなぁ", "そうだねぇ", "楽しくない"]}' http://0.0.0.0:8080/`
- デプロイ: `gcloud functions deploy optimistic_analysis --runtime python37 --trigger-http --allow-unauthenticated --memory=128MB --env-vars-file=./env.yaml`

FIXME:
## 改善点
`楽しくない`がプラス判定になったりする
