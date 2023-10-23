from io import BytesIO
from fastapi import FastAPI, UploadFile
import openai

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/files/")
async def process_audio_file(file: UploadFile):
    # 文字起こし
    audio_file = await file.read()
    audio_file_buffer = BytesIO(audio_file)
    audio_file_buffer.name = file.filename
    transcript = openai.Audio.transcribe("whisper-1", audio_file_buffer)

    # 議事録サマリ
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""
                会議の発言データから、会議のサマリーを作成してください
                会議の発言データ
                {transcript.text}

                サマリー:
                """,
            },
        ],
    )

    summary = response.choices[0].message.content

    # ToDo作成
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"""
                会議の発言データから、次回以降のTODOを作成してください。期待するフォーマットに沿って出力してください

                会議の発言データ
                {transcript.text}

                期待するフォーマット
                - 一つ目のTODO
                - 二つ目のTODO""",
            },
        ],
    )

    todo_list = response.choices[0].message.content

    # 議事録作成
    report = f"""
    # 議事録

    ## サマリ

    {summary}

    ## ToDo

    {todo_list}
    """

    return {"report": report}
