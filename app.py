import requests 
import streamlit as st 

# Définition de la clé API et de l'URL de Dify
dify_api_key = "app-b5ki6sHRgZeUVf6cLXtmtAQk"
url = "http://localhost/v1/chat-messages"

# Titre de l'application
st.title("Dify Streamlit Chatbot App")

# Initialisation des variables de session pour stocker l'ID de conversation et les messages
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages de la conversation précédente
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Saisie de la question de l'utilisateur
prompt = st.chat_input("Enter your question")

# Si l'utilisateur saisit un message
if prompt: 
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Réponse de l'assistant
    with st.chat_message("assistant"):  # <=== Ici, l'indentation est corrigée
        message_placeholder = st.empty()

        headers = {
            'Authorization': f'Bearer {dify_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "conversation_id": st.session_state.conversation_id,
            "user": "aianytime",
            "files": []
        }

        try:
            # Envoi de la requête à Dify
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()

            # Récupération de la réponse et mise à jour de l'ID de conversation
            full_response = response_data.get('answer', '')
            new_conversation_id = response_data.get('conversation_id', st.session_state.conversation_id)
            st.session_state.conversation_id = new_conversation_id

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            full_response = "An error occurred while fetching the response."

        # Affichage de la réponse de l'assistant
        message_placeholder.markdown(full_response)
