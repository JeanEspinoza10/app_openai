import dotenv
import os
dotenv.load_dotenv()
import openai
import base64

api_key = os.getenv("OPENAI_API_KEY") 

client = openai.OpenAI(api_key = api_key)


def response_openai(file_path = "", ):
    try:
        
        # Codificar imagen en base64
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        base64_3 = encode_image(file_path)
        img_3 = f"data:image/jpeg;base64,{base64_3}"

        # Crear los mensajes
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": '''
                            Eres un experto en obtener las secuencias de las manos de poker. 
                        '''
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": '''
                                    Solamente analiza la parte de la imagen donde estan las acciones y dame el orden de las acciones preflop, flop, turn y river.
                                    Todo según el orden de la acción. Tener en cuenta las posiciones de lo jugadores según el orden de las acciones, preflop. Lo que esta en 
                                    recuadro de "p_vill" son los jugadores. EL jugador que esta en la parte central inferior es el jugador hero o "q_hero". 
                                    Las posiciones para mesa de 6 jugadores son: BTN - SB - BB - UTG - MP - CO
                                    Las posiciones para mesa de 8 jugadores son: BTN - SB - BB - UTG - UTG1 - MP - MP1 - CO
                                    El resumen debe estas de la siguiente manera, este es un ejemplo:
                                    {
                                        "players_position: [
                                            {
                                                "name": "",
                                                stack_incial :"" ,
                                                position : ""
                                            },
                                            {
                                                "name": "",
                                                stack_incial :"" ,
                                                position : ""
                                            }
                                        ],
                                        actions : [
                                            {
                                                "etapa": flop
                                                secuencia: ["juagdorA ::: bet ::: 3 bb" , "juagdorA ::: bet ::: 3 bb" , "juagdorA ::: bet ::: 3 bb"],
                                                pot_size: 0
                                            },
                                            {
                                                "etapa": turn
                                                secuencia: ["juagdorA ::: bet ::: 3 bb" , "juagdorA ::: bet ::: 3 bb" , "juagdorA ::: bet ::: 3 bb"],
                                                pot_size: 0
                                                
                                            }
                                        ],
                                        board: [A, T , Q , 5, 7]
                                    }
                                    
                                    
                                    
                                '''
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_3
                        }
                    }
                ]
            }

        ]

        # Enviar la solicitud al modelo
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0,          
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        # Obtener respuesta
        description = response.choices[0].message.content
        return description
    except Exception as err:
        print("Error in response of openai" , err)
        return None
    

