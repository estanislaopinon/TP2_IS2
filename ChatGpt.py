import argparse
from openai import OpenAI

client= OpenAI()#Inicialización del cliente de OpenAI
interaction_history=[]# Buffer que almacena las consultas y respuestas

#Función para interactuar con el modelo de chat de OpenAI y obtener respuestas
def chat_with_chatgpt(userquery, conversation ):
   #userquery: consulta del usuario
   #conversation: indica si se esta utilizando el modo de conversacion
   context = " ".join(interaction_history) if conversation else ""
   usertask = " "
   try:
      #Realiza una solicitud al modelo de chat de OpenAI para obtener la respuesta
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
         #Agrega la consulta y la respuesta al historial de interacciones
         interaction_history.append(userquery)
         interaction_history.append(response.choices[0].message.content)
      #Devuelve la respuesta generada
      return response.choices[0].message.content
      
   except Exception as e:
      #En caso de error, devuelve un mensaje de error
      return f"Error en la solicitud: {e}"

def get_user_query():# Función responsable de solicitar al usuario una consulta y asegurarse de que esta sea valida
   while True:
      user_query= input("Ingrese la Consulta: ")
      if user_query.strip() != "":
            return user_query
      print("Ingrese una consulta válida")  

def main():#Funcion principal del programa
   #Configuracion del parser de argumentospara aceptar el argumento "--convers"
   parser= argparse.ArgumentParser(description='ChatGPT - Chat with GPT-3.5 AI model.')
   parser.add_argument('--convers', action='store_true', help='Activar el modo de conversación ')
   args = parser.parse_args()
   
   print("Modo de conversación" ,("activado" if args.convers else "desactivado"))#Imprime el estado del modo de conversación
   while True:
      try:
         user_query= get_user_query()

         print("YOU: ", user_query)

         interaction_history.append(user_query)#Agrego la consulta a interaction_history

         lastquery= interaction_history[-1]#Obtengo la ultima consulta realizada y la almaceno en una variable

         answer=chat_with_chatgpt(lastquery, 1 if args.convers else 0)#Realiza la interacción con chatGPT utilizando la ultima consulta

         #Almaceno la respuesta en el buffer
         interaction_history.append(answer)
         #Se imprime la respuesta
         print("chatGPT: ", answer)
      except KeyboardInterrupt:# Interrupción del teclado (Ctrl+C) para salir del bucle de conversación
         print("\nSaliendo del programa")
         break
      except Exception as e:#Cualquier error que pueda ocurrir durante la interacción con chatGPT, se informa que se produjo un error
         print(f"Se ha producido un error: {e}")
      


if __name__=="__main__":
   main()

        
   

