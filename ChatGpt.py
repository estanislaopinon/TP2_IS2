from openai import OpenAI

client= OpenAI()

interaction_history=[]

def chat_with_chatgpt(userquery):
    
   context=" "

   usertask=" "

   response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=[
         {
            "role": "system",
            "content": context },
         {
            "role": "user",
            "content" : usertask },
         {
            "role": "user",
            "content": userquery }
      ],
      temperature=1,
      max_tokens=200,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
   )
   return response.choices[0].message.content

def main():

   while True:

      userquery= input("Ingrese la Consulta: ")
      if userquery.strip()== "":
         print("Ingrese una contraseña valida")
         continue

      print("YOU: ", userquery)

      answer = chat_with_chatgpt(userquery)
      print("chatGPT: ", answer)


main()

        
   

