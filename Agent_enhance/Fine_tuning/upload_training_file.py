from openai import OpenAI

client = OpenAI(
  api_key="YOUR_API_KEY"
)

response = client.files.create(
    file=open("data/HAPS.jsonl", "rb"),
    purpose="fine-tune"
)

print(client.files.list())

# client.files.delete("file-5wenc6k87hUeQu8ab3iwMFA1")