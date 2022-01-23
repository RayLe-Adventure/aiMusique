import os
import openai
import requests

openai.api_key = os.environ["GPT_API"]
model = "ada:ft-personal-2022-01-15-23-50-46"
model2 = "curie:ft-personal-2022-01-16-19-48-30"
pr = " \n\n###\n\n"

# Completion request
"""
response = openai.Completion.create(
    model=model,
    prompt="Appuie bien les coups que tu donnes\nLes coups et les messages\nElle voulait que je sois un homme\nToujours prêt au combat\nTiens tes bras, protège-toi, le quitte pas\nFrappe droit quand sa garde baissera\n\nJusqu’à mort où c’est tout comme\nLe sang et les messages\nJe connaissais pas le bonhomme\nElle me l’avait montré du doigt\nJ’ai cogné, j’ai crié, il est tombé\nEt par terre, près des pierres son regard\nS’est vidé, s’est vidé\n\nJ’étais devenu un homme\nMeurtre ou assassinat\nPauvre type, elle m’a dit cet homme\nJe l’aimais plus que toi\nJ’ai cogné, j’ai crié, il est tombé\nEt par terre, près des pierres son regard\nS’est vidé, s’est vidé\n\nJ’étais devenu un homme\nMeurtre ou assassinat\nPauvre type, elle m’a dit cet homme\nJe l’aimais plus que toi \n\n###\n\n",
    stop=" END",
    temperature=0.9,
)
print(response['choices'][0]['text'])
"""

response = openai.Completion.create(
    model=model2,
    prompt="",
    stop=" END",
    temperature=1,
    max_tokens=150,
    echo=True
)
print(response['choices'][0]['text'])


"""
# Finding text
response = {"text":response["choices"][0]["text"],
            "finish":response["choices"][0]["finish_reason"],
            }
print(response["text"])
"""

# Search request
"""
search = openai.Engine("ada").search(
  documents=["White House", "hospital", "school"],
  query="the president"
)
print(search)
"""

# Classification request
"""
classify = openai.Classification.create(
  search_model="ada",
  model="curie",
  examples=[
    ["A happy moment", "Positive"],
    ["I am sad.", "Negative"],
    ["I am feeling awesome", "Positive"]
  ],
  query="It is a book",
  labels=["Positive", "Negative", "Neutral"],
)

print(classify)
"""

# Answer request
"""
answer = openai.Answer.create(
  search_model="ada",
  model="curie",
  question="which puppy is happy?",
  documents=["Puppy A is happy.", "Puppy B is sad."],
  examples_context="In 2017, U.S. life expectancy was 78.6 years.",
  examples=[["What is human life expectancy in the United States?","78 years."]],
  max_tokens=5,
  stop=["\n", "<|endoftext|>"],
)

print(answer)
"""
