#Copy and Run in COLAB
!pip install openai
!pip install gradio  
!pip install youtube_dl
!pip install youtube_transcript_api

from openai import OpenAI

client = OpenAI(
    api_key="*************************",  #put your Open AI key here in place of '**..."
)

def get_assistant_response(messages):
  r = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role":m["role"], "content": m["content"]} for m in messages],
  )
  response = r.choices[0].message.content
  return response

# @title Prompt
content = {
"JirayaGPT"   : """consider Your name is JirayaGPT, a personal tutor that has the personality of Jiraya from Naruto. you specialize in coding.
           you are generally light-hearted and gregarious, making jokes at his own expense and giving a mirthful laugh about it afterwards.
           In your interactions with me, you like to pretend to be smug or selfish, upsetting me so that you can further rile me up with your humour.""",

"SherlockGPT" : """consider Your name is SherlockGPT, a personal tutor that has the personality of Sherlock Holmes, the world famous detective. My name is Watson.
           Firstly wish me in an informal way.
           You should analyse and describe every question like a detective, find the solution and explain it neatly.
           Use diaogues like  'You know my methods, Watson.' , 'They were the footprints of a gigantic hound!',etc..""",

"BrahmiGPT"   : """consider your name is Brahmigpt, a personal tutor, specialized in social, that has the personality of Brahmanandam Gaaru from the movie Adhurs.
           Don't mention this while introducing yourself.
           My name is 'chaari', start introducing yourself, treat me like an amatuer in everything, yell back at me and scold me here and there.
           Your catchphrase is "Ye ra Chaari..?" but don't use it everytime you answer.""",

"StarkGPT"    : """consider your name is Starkgpt, a personal tutor, specialized in Science that has the personality of Tony Stark from avengers movies.
           when I say hi ,address me as 'kid' and start intoducing yourself in a attitude manner .
           Treat me like i know the basics of everything and keep every answer short and staright to the point. """
}

messages = [{"role": "assistant", "content":"Follow what the user says."}]

import re

from youtube_transcript_api import YouTubeTranscriptApi
def trans(message, chat_history):
  message = message.split()
  youtube_url = message[1]

  match = re.search(r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?', youtube_url)

  if match:
    video_id = match.group(1)

  else:
    raise ValueError("Invalid YouTube URL")

  transcript = YouTubeTranscriptApi.get_transcript(video_id)

  transcript_text = ""

  for segment in transcript:

    transcript_text += segment["text"] + " "

  return(transcript_text)


def respond(message, chat_history):
  try:
    if message == "hi" or message == "HI" or message == "Hi":

      response_hi = """Hello! Your personalised AI tutor is up and ready. To load a Tutor Enter the Tutor's name.

      Tutors Available = ['JirayaGPT' , 'BrahmiGPT' , 'StarkGPT' , "SherlockGPT"]

      After loading your Tutor, you can ask any question and the Tutor will try to explain it to you in their style.
      To transcibe and create short notes from a recorded class video, Enter 'Transcribe' followed by the youtube URL.
      To end the chat enter 'END' """

      chat_history.append((message, response_hi))
      return "", chat_history

    elif (message.split())[0] == 'Transcribe' or (message.split())[0] == 'transcribe':

      transcript = trans(message, chat_history)

      inputfortutor = transcript + "Summarize this youtube transcibed text in the tutor style."

      messages.append({"role": "user", "content": inputfortutor})
      assistant_response = get_assistant_response(messages)
      messages.append({"role": "assistant", "content": assistant_response})

      chat_history.append((message, assistant_response))
      return "", chat_history

    elif (message.split())[0] == 'Load' or (message.split())[0] == 'load':

      model = message.split()[1]

      messages.append({"role": "user", "content": content[model]})
      assistant_response = get_assistant_response(messages)
      messages.append({"role": "assistant", "content": assistant_response})

      chat_history.append((message, assistant_response))


      return "", chat_history

    else:

      user_input = message

      messages.append({"role": "user", "content":  user_input})
      assistant_response = get_assistant_response(messages)
      messages.append({"role": "assistant", "content": assistant_response})

      chat_history.append((message, assistant_response))
      return "", chat_history
  except Exception as ex:
    assistant_response = "The Tutor requested is not Available!."
    chat_history.append((message, assistant_response))
    return "", chat_history

#----------------------------------------------------------------- UI -----------------------------------------------------------------#
import gradio as gr
import random
import time

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(debug=True)
