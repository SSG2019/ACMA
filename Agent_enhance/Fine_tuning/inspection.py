from openai import OpenAI

client = OpenAI(
  api_key="YOUR_API_KEY"
)


# List 10 fine-tuning jobs
print(client.fine_tuning.jobs.list(limit=10))

print(client.fine_tuning.jobs.retrieve("ftjob-XNXCqhhUgMUekMEIjjZkatnF"))
print(client.fine_tuning.jobs.retrieve("ftjob-agcebxhMRewG5q25eCoQnyyT"))

# client.fine_tuning.jobs.cancel("ftjob-XNXCqhhUgMUekMEIjjZkatnF")


