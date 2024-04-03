"""
Este programa Python permite la interaccion con el modelo OpneAI.
Permite a los usuarios enviarles consultas y mostrar las respuestas obtenidas en pantalla
Incluye "modo de conversación" para mantener una conversacion fluida con el chatbot
contiene pylint como analizador estático, identificando posibles mejoras y sugerencias
para mantener un codigo limpio y legible 

Instrucciones:
 1. Ingrese sus consultas al usuario y presione Enter para enviarlas a chatGPT
 2. Utilice la tecla "cursor Up" para recuperar y editar la ultima consulta.
 3. Active el modo conversacion con el argumento "--convers" para mantener una conversacion continua
 4. Revise las sugerencias proporcionadas por pylint para mejorar la calidad de su código
"""
import argparse
from openai import OpenAI

client = OpenAI()  # Inicialización del cliente de OpenAI
interaction_history = []  # Buffer que almacena las consultas y respuestas

# Exepciones especificas a detectar
EXEPTIONS = (ConnectionError, TimeoutError, ValueError, TypeError)


def chat_with_chatgpt(userquery, conversation):
    """
    Interactua con el modelo de OpenAI (GPT-3.5) 
    para obtener respuestas a partir de la consulta del usuario

    Args:
      userquery(str):la consulta del usuario que se envia al modelo de chat
      conversation(bool): indicador booleano que indica si se esta usando el modo de conversacion.
      Si es True, significa que se esta manteniendo una conversacion continua.
      En caso contrario, se trata de una única consulta
    Returns:
      str: La respuesta generada por el modelo de chat
    """
    # userquery: consulta del usuario
    # conversation: indica si se esta utilizando el modo de conversacion
    context = "".join(interaction_history) if conversation else ""
    usertask = ""
    try:
        # Realiza una solicitud al modelo de chat de OpenAI para obtener la respuesta
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": usertask},
                {"role": "user", "content": userquery}
            ],
            temperature=1,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        if conversation:
            # Agrega la consulta y la respuesta al historial de interacciones
            interaction_history.append(userquery)
            interaction_history.append(response.choices[0].message.content)
        # Devuelve la respuesta generada
        return response.choices[0].message.content

    except EXEPTIONS as e:
        # En caso de error, devuelve un mensaje de error
        return f"Error en la solicitud: {e}"


def get_user_query():
    """
    Solicita al usuario una consulta y asegura que la consulta ingresada sea válida.

    Returns:
      str: La consulta ingresada por el usuario.
    """
    while True:
        user_query = input("Ingrese la Consulta: ")
        if user_query.strip() != "":
            return user_query
        print("Ingrese una consulta válida")


def main():
    """
    Función principal del programa.
    Esta función configura los argumentos de linea de comandos, solicita consultas al usuario
    y maneja la interacción con el model de chat de OpenAI
    """
    # Configuracion del parser de argumentospara aceptar el argumento "--convers"
    parser = argparse.ArgumentParser(
        description='ChatGPT - Chat with GPT-3.5 AI model.')
    parser.add_argument('--convers', action='store_true',
                        help='Activar el modo de conversación ')
    args = parser.parse_args()

    # Imprime el estado del modo de conversación
    print("Modo de conversación", ("activado" if args.convers else "desactivado"))
    while True:
        try:
            user_query = get_user_query()

            print("YOU: ", user_query)

            # Agrego la consulta a interaction_history
            interaction_history.append(user_query)

            # Obtengo la ultima consulta realizada y la almaceno en una variable
            lastquery = interaction_history[-1]

            # Realiza la interacción con chatGPT utilizando la ultima consulta
            answer = chat_with_chatgpt(lastquery, 1 if args.convers else 0)

            # Almaceno la respuesta en el buffer
            interaction_history.append(answer)
            # Se imprime la respuesta
            print("chatGPT: ", answer)
            # Interrupción del teclado (Ctrl+C) para salir del bucle de conversación
        except KeyboardInterrupt:
            print("\nSaliendo del programa")
            break
          # Cualquier error que pueda ocurrir durante la interacción con chatGPT
          # se informa que se produjo un error
        except EXEPTIONS as e:
            print(f"Se ha producido un error: {e}")


if __name__ == "__main__":
    main()
