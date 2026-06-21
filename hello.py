import os
from google import genai
from dotenv import load_dotenv

# 1. Cargar la llave desde el archivo oculto .env
load_dotenv()

# 2. Inicializar el cliente de Gemini usando la librería oficial de Google
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def leer_contexto_local():
    """Función para leer el archivo de texto con tus propios datos"""
    try:
        with open("datos.txt", "r", encoding="utf-8") as archivo:
            return archivo.read()
    except FileNotFoundError:
        return "No se encontró el archivo de datos local. Por favor, crea datos.txt"

def chat_con_asistente():
    contexto_documento = leer_contexto_local()
    
    print("🤖 ¡Asistente de IA (Gemini Gratis) Inicializado! Escribe 'salir' para terminar.\n")
    
    while True:
        usuario_input = input("Tú: ")
        if usuario_input.lower() == "salir":
            print("🤖 ¡Hasta luego!")
            break
            
        # Unir el contenido de tu txt con la pregunta del usuario
        prompt_completo = f"""
        Actúa como un asistente experto. Responde a la pregunta del usuario basándote únicamente en la siguiente información local:
        
        --- INICIO DE DATOS LOCALES ---
        {contexto_documento}
        --- FIN DE DATOS LOCALES ---
        
        Pregunta del usuario: {usuario_input}
        """
        
        try:
            # Llamar al modelo rápido y gratuito gemini-2.5-flash
            respuesta = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_completo,
            )
            
            print(f"\nAsistente IA: {respuesta.text}\n")
            
        except Exception as e:
            print(f"\n❌ Error al conectar con la API de Google: {e}\n")

if __name__ == "__main__":
    chat_con_asistente()