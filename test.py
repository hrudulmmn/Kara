import base64
from groq import Groq
import fitz
key = 'api'
client = Groq(api_key=key)
model = "meta-llama/llama-4-scout-17b-16e-instruct"
pgno =0
doc = fitz.open("mod2.pdf")

page = doc.load_page(0)
zmatrix = fitz.Matrix(1.0,1.0)
pix = page.get_pixmap(matrix=zmatrix)
png = pix.tobytes('png')

img = base64.b64encode(png).decode("utf-8")
prompt = "provide detailed description of the given page"
resp = client.chat.completions.create(
        model=model,
        messages=[{
            "role":"user",
            "content": [
                {"type": "text",
                 "text":prompt},{
                "type":"image_url",
                "image_url":{"url":f"data:image/png;base64,{img}"},
                 },
            ],
        }]

    )
response = resp.choices[0].message.content
print(response)
