# meeting-report-generator

## How to

```bash
# 依存ライブラリをインストール
pip install -r requirements.txt

# OpenAIのAPIキーを設定
export OPENAI_API_KEY=<Your API Key>

# 開発サーバーを起動
uvicorn main:app --reload

# 音声ファイルをアップロード
curl localhost:8000/api/files/ -F file=@./sample.wav
```

## クレジット表記

sample.wav

- VOICEVOX:四国めたん
