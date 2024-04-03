import argparse
from openai import OpenAI

client= OpenAI()
interaction_history=[]# Buffer que almacena las consultas y respuestas

def chat_with_chatgpt(userquery, conversation ):
    
   context=" ".join(interaction_history) if conversation else ""

   usertask=" "
   try:
      response = client.chat.completions.create(
         model="gpt-3.5-turbo-0125",
         messages=[
            {"role": "system", "content": context },
            {"role": "user", "content" : usertask },
            {"role": "user","content": userquery }
         ],
         temperature=1,
         max_tokens=200,
         top_p=1,
         frequency_penalty=0,
         presence_penalty=0
      )
      if conversation:
         interaction_history.append(userquery)
         interaction_history.append(response.choices[0].message.content)

      return response.choices[0].message.content
      
   except Exception as e:
      return f"Error en la solicitud: {e}"

   

def main():
   parser= argparse.ArgumentParser(description='ChatGPT - Chat with GPT-3.5 AI model.')
   parser.add_argument('--convers', action='store_true', help='Activar el modo de conversación ')
   args = parser.parse_args()
   
   while True:
      print("Modo de conversación" ,("activado" if args.convers else "desactivado"))
      
      while True:
         try:
            userquery= input("Ingrese la Consulta: ")
            if userquery.strip()== "":
               print("Ingrese una contraseña valida")
               continue

            print("YOU: ", userquery)

            interaction_history.append(userquery)#Agrego la consulta a interaction_history

            lastquery= interaction_history[-1]#Obtengo la ultima consulta realizada y la almaceno en una variable

            answer=chat_with_chatgpt(lastquery, 1 if args.convers else 0)#Realiza la interacción con chatGPT utilizando la ultima consulta

            #Almaceno la respuesta en el buffer
            interaction_history.append(answer)
            print("chatGPT: ", answer)
         except KeyboardInterrupt:
            print("\nSaliendo del programa")
            break
         except Exception as e:
            print(f"Se ha producido un error: {e}")
      


if __name__=="__main__":
   main()

        
   

