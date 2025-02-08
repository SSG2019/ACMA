from openai import OpenAI

client = OpenAI(
  api_key="YOUR_API_KEY"
)

client.fine_tuning.jobs.create(
  training_file="file-jyTl5PhGz4yy8q93oApy7mUI",
  model="gpt-4o-mini-2024-07-18",
  suffix="haps_llm",
  seed=10086
)