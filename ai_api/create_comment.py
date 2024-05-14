from openai import OpenAI
import json
import time


def CreateComment(diary):
    # api_key 불러오기
    with open("/home/test01/yykc/ai_api/api_key.json", 'r') as file:
        config = json.load(file)


    client = OpenAI(api_key=config["api_key"])
    assistant = client.beta.assistants.retrieve(config["assistant_id"])
    thread = client.beta.threads.create()


    query = diary + " 답변은 한글로 100글자 이내로 해줘."

    # print(f"prompt:{query}")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content= query
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while True:
        if run.status == "completed":
            break
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)

    msg = client.beta.threads.messages.list(thread_id=thread.id)

    return msg.data[0].content[0].text.value

