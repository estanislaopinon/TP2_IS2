from openai import OpenAI

client= OpenAI()

interaction_history=[]

def chat_with_chatgpt(userquery):
    
   context=" "

   usertask=" "
   try:
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
   
   except Exception as e:
      print(f"Error en la solicitud: {e}")

   

def main():

   while True:
      try:
         userquery= input("Ingrese la Consulta: ")
         if userquery.strip()== "":
            print("Ingrese una contraseña valida")
            continue

         print("YOU: ", userquery)

         answer = chat_with_chatgpt(userquery)
         print("chatGPT: ", answer)
      except KeyboardInterrupt:
         print("\nSaliendo del programa")
      except Exception as e:
         print(f"Se ha producido un error: {e}")


main()

        
   

