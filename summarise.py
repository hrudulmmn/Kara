from groq import Groq
import render

key = 'api'
client = Groq(api_key=key)
model = "meta-llama/llama-4-scout-17b-16e-instruct"

def pagesummarise(doc,page,conts):
    
    prompt = ("Summarise the following PDF page.\n\n"
    "TEXT CONTENT:\n" + conts + "\n\n"
     + "\n\n"
    +"Image description:\n" +  + "\n\n"+"Give a compact,detailed, easy to understand summary with definitions.")

    resp = client.chat.completions.create(
    model = model,
    messages =[{'role':'user','content':prompt}]
    )
    response = resp.choices[0].message.content
    return response


