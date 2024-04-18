"""
Gemini setup
"""

import google.generativeai as genai

genai.configure(api_key="AIzaSyBTm_9e7gLBHFdikwQwnXwRzx6ZS4r82Bs")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
])

# collecting answerscript from file

with open("output.txt", "r") as file:
    answer = file.read()

query = "assume yourself as a grammer checker and you dont have any knowledge other than grammer and spellings . add necessary fullstops.correct the para and dont change the meaning. Do not output anythinng otherthan the para."


convo.send_message(query+answer)
print(convo.last.text)

with open("output.txt", 'w') as file:
    file.write(convo.last.text)
