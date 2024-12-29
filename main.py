import numpy as np
import tensorflow as tf
import streamlit as st
disease=None
diseases=['Apple___Apple_scab',
 'Apple___Black_rot',
 'Apple___Cedar_apple_rust',
 'Apple___healthy',
 'Blueberry___healthy',
 'Cherry_(including_sour)___Powdery_mildew',
 'Cherry_(including_sour)___healthy',
 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 'Corn_(maize)___Common_rust_',
 'Corn_(maize)___Northern_Leaf_Blight',
 'Corn_(maize)___healthy',
 'Grape___Black_rot',
 'Grape___Esca_(Black_Measles)',
 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 'Grape___healthy',
 'Orange___Haunglongbing_(Citrus_greening)',
 'Peach___Bacterial_spot',
 'Peach___healthy',
 'Pepper,_bell___Bacterial_spot',
 'Pepper,_bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Raspberry___healthy',
 'Soybean___healthy',
 'Squash___Powdery_mildew',
 'Strawberry___Leaf_scorch',
 'Strawberry___healthy',
 'Tomato___Bacterial_spot',
 'Tomato___Early_blight',
 'Tomato___Late_blight',
 'Tomato___Leaf_Mold',
 'Tomato___Septoria_leaf_spot',
 'Tomato___Spider_mites Two-spotted_spider_mite',
 'Tomato___Target_Spot',
 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato___Tomato_mosaic_virus',
 'Tomato___healthy'
 ]
treatment_plan={
    "Apple___Apple_scab": {
        "en": "Use fungicides like captan or myclobutanil. Ensure proper pruning to improve air circulation.",
        "hi": "कैप्टन या माइक्लोबुटानिल जैसे फफूंदनाशकों का उपयोग करें। हवा परिसंचरण सुधारने के लिए उचित छंटाई सुनिश्चित करें।"
    },
    "Apple___Black_rot": {
        "en": "Apply fungicides such as thiophanate-methyl. Remove and destroy infected fruits and branches.",
        "hi": "थायोफेनेट-मिथाइल जैसे फफूंदनाशकों का उपयोग करें। संक्रमित फलों और शाखाओं को हटा दें और नष्ट करें।"
    },
    "Apple___Cedar_apple_rust": {
        "en": "Use fungicides like myclobutanil. Avoid planting apple trees near junipers.",
        "hi": "माइक्लोबुटानिल जैसे फफूंदनाशकों का उपयोग करें। सेब के पेड़ों को जुनिपर के पास लगाने से बचें।"
    },
    "Apple___healthy": {
        "en": "No treatment needed. Maintain general plant health through regular care.",
        "hi": "कोई उपचार आवश्यक नहीं। नियमित देखभाल के माध्यम से सामान्य पौधे की सेहत बनाए रखें।"
    },
    "Blueberry___healthy": {
        "en": "No treatment needed. Ensure proper irrigation and soil health.",
        "hi": "कोई उपचार आवश्यक नहीं। उचित सिंचाई और मिट्टी की सेहत सुनिश्चित करें।"
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "en": "Apply sulfur-based fungicides or neem oil. Prune to improve air circulation.",
        "hi": "गंधक आधारित फफूंदनाशकों या नीम के तेल का उपयोग करें। हवा परिसंचरण सुधारने के लिए छंटाई करें।"
    },
    "Cherry_(including_sour)___healthy": {
        "en": "No treatment needed. Maintain overall plant health.",
        "hi": "कोई उपचार आवश्यक नहीं। समग्र पौधे की सेहत बनाए रखें।"
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "en": "Use fungicides like azoxystrobin. Practice crop rotation and use resistant varieties.",
        "hi": "एज़ॉक्सीस्ट्रोबिन जैसे फफूंदनाशकों का उपयोग करें। फसल चक्र का पालन करें और प्रतिरोधी किस्मों का उपयोग करें।"
    },
    "Corn_(maize)___Common_rust_": {
        "en": "Apply fungicides like propiconazole. Use rust-resistant varieties.",
        "hi": "प्रोपिकोनाज़ोल जैसे फफूंदनाशकों का उपयोग करें। जंग प्रतिरोधी किस्मों का उपयोग करें।"
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "en": "Use fungicides such as mancozeb or chlorothalonil. Practice crop rotation.",
        "hi": "मैंकोज़ेब या क्लोरोथालोनिल जैसे फफूंदनाशकों का उपयोग करें। फसल चक्र का पालन करें।"
    },
    "Corn_(maize)___healthy": {
        "en": "No treatment needed. Maintain proper irrigation and nutrient management.",
        "hi": "कोई उपचार आवश्यक नहीं। उचित सिंचाई और पोषक तत्व प्रबंधन बनाए रखें।"
    },
    "Grape___Black_rot": {
        "en": "Apply fungicides like myclobutanil or copper-based products. Remove infected leaves and fruits.",
        "hi": "माइक्लोबुटानिल या तांबा आधारित उत्पादों जैसे फफूंदनाशकों का उपयोग करें। संक्रमित पत्तियों और फलों को हटा दें।"
    },
    "Grape___Esca_(Black_Measles)": {
        "en": "Remove and destroy infected wood. Apply fungicides like tebuconazole.",
        "hi": "संक्रमित लकड़ी को हटा दें और नष्ट करें। टेबुकोनाज़ोल जैसे फफूंदनाशकों का उपयोग करें।"
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "en": "Use fungicides such as mancozeb or copper oxychloride. Prune affected areas.",
        "hi": "मैंकोज़ेब या तांबा ऑक्सीक्लोराइड जैसे फफूंदनाशकों का उपयोग करें। प्रभावित क्षेत्रों की छंटाई करें।"
    },
    "Grape___healthy": {
        "en": "No treatment needed. Ensure good vineyard management practices.",
        "hi": "कोई उपचार आवश्यक नहीं। अच्छी अंगूर बाग प्रबंधन प्रथाएं सुनिश्चित करें।"
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "en": "Remove infected trees. Use disease-free planting material and control vector populations.",
        "hi": "संक्रमित पेड़ों को हटा दें। रोग मुक्त रोपण सामग्री का उपयोग करें और वाहक आबादी को नियंत्रित करें।"
    },
    "Peach___Bacterial_spot": {
        "en": "Apply copper-based bactericides. Remove and destroy infected leaves and fruits.",
        "hi": "तांबा आधारित बैक्टीरिसाइड्स का उपयोग करें। संक्रमित पत्तियों और फलों को हटा दें और नष्ट करें।"
    },
    "Peach___healthy": {
        "en": "No treatment needed. Maintain proper plant care and pruning.",
        "hi": "कोई उपचार आवश्यक नहीं। उचित पौधे की देखभाल और छंटाई सुनिश्चित करें।"
    },
    "Pepper,_bell___Bacterial_spot": {
        "en": "Apply copper-based bactericides. Avoid overhead watering.",
        "hi": "तांबा आधारित बैक्टीरिसाइड्स का उपयोग करें। ऊपरी सिंचाई से बचें।"
    },
    "Pepper,_bell___healthy": {
        "en": "No treatment needed. Ensure proper plant spacing and nutrition.",
        "hi": "कोई उपचार आवश्यक नहीं। उचित पौधे की दूरी और पोषण सुनिश्चित करें।"
    },
    "Potato___Early_blight": {
        "en": "Use fungicides like chlorothalonil. Avoid overcrowding and ensure proper drainage.",
        "hi": "क्लोरोथालोनिल जैसे फफूंदनाशकों का उपयोग करें। भीड़भाड़ से बचें और उचित जल निकासी सुनिश्चित करें।"
    },
    "Potato___Late_blight": {
        "en": "Apply fungicides like metalaxyl. Use certified seeds and practice crop rotation.",
        "hi": "मेटालैक्सिल जैसे फफूंदनाशकों का उपयोग करें। प्रमाणित बीजों का उपयोग करें और फसल चक्र का पालन करें।"
    },
    "Potato___healthy": {
        "en": "No treatment needed. Maintain good field practices.",
        "hi": "कोई उपचार आवश्यक नहीं। अच्छे खेत प्रथाओं को बनाए रखें।"
    },
    "Raspberry___healthy": {
        "en": "No treatment needed. Ensure regular care and pruning.",
        "hi": "कोई उपचार आवश्यक नहीं। नियमित देखभाल और छंटाई सुनिश्चित करें।"
    }
}
def predict_image(img):
    model=tf.keras.models.load_model('model.h5')
    image=tf.keras.preprocessing.image.load_img(img,target_size=(128,128))
    input_array=tf.keras.preprocessing.image.img_to_array(image)
    input_array=np.array([input_array])
    predictions=model.predict(input_array)
    result_idx=np.argmax(predictions)
    return diseases[result_idx]

st.title("Plant Disease Detection")
st.sidebar.title("Dashboard")
page=st.sidebar.selectbox("Select page",["Home","Disease Prediction","Chatbot"])
if(page=="Home"):
    st.write("Welcome to Plant Disease Detection")
    st.image("home.jpg",use_container_width=True)
    st.markdown("""
    Welcome to the Plant Disease Recognition System! 🌿🔍
    
    Our mission is to help in identifying plant diseases efficiently. Upload an image of a plant, and our system will analyze it to detect any signs of diseases. Together, let's protect our crops and ensure a healthier harvest!

    ### How It Works
    1. **Upload Image:** Go to the **Disease Recognition** page and upload an image of a plant with suspected diseases.
    2. **Analysis:** Our system will process the image using advanced algorithms to identify potential diseases.
    3. **Results:** View the results and recommendations for further action.

    ### Why Choose Us?
    - **Accuracy:** Our system utilizes state-of-the-art machine learning techniques for accurate disease detection.
    - **User-Friendly:** Simple and intuitive interface for seamless user experience.
    - **Fast and Efficient:** Receive results in seconds, allowing for quick decision-making.

    ### Get Started
    Click on the **Disease Recognition** page in the sidebar to upload an image and experience the power of our Plant Disease Recognition System!

    ### About Us
    Learn more about the project, our team, and our goals on the **About** page.
    """)
elif(page=="Disease Prediction"):
    st.write("Disease Prediction")
    uploaded_file=st.file_uploader("Choose an image...",type="jpg")
    if uploaded_file is not None:
        image=uploaded_file
        st.image(image,caption="Uploaded Image",use_container_width=True)
        # st.button("Predict")
        if(st.button("Predict")):
            st.write("Classifying...")
            label=predict_image(uploaded_file)
            disease=label
            st.write(f"Prediction: {label}")
            st.write("Treatment: ")
            if label in treatment_plan:
                st.write(treatment_plan[label]['en'])
                st.write(treatment_plan[label]['hi'])
            else:
                st.write("No treatment plan available for this disease.")
else:
    import streamlit as st
    import subprocess
    import sys
    from dotenv import load_dotenv
    from langchain.chains import ConversationChain
    from langchain.chains.conversation.memory import ConversationBufferMemory
    from langchain_groq import ChatGroq

    # Install required packages
    def install_packages():
        required_packages = [
            "streamlit",
            "groq",
            "langchain",
            "langchain_groq",
            "python-dotenv"
        ]
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    install_packages()

    # Load environment variables
    load_dotenv()

    # Replace with your Groq API key
    groq_api_key = ''

    # Chatbot Function
    def main():
        st.title("Farmer's Crop Treatment Chatbot")
        st.sidebar.title('Options')

        # Dropdown for language selection
        language = st.sidebar.selectbox('Select Language', ['English', 'Hindi'])
        language_code = 'en' if language == 'English' else 'hi'

        # Conversational memory length slider
        conversational_memory_length = st.sidebar.slider('Conversational Memory Length', 1, 10, 5)
        user_question = st.text_area(f'Ask me something about crop treatment in {language}')

        # Conversation memory setup
        memory = ConversationBufferMemory(k=conversational_memory_length)

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            st.session_state.language = language_code
            st.session_state.language_instruction_sent = False

        # Send language preference to chatbot
        if not st.session_state.language_instruction_sent or st.session_state.language != language_code:
            instruction = f"Answer all my questions in {'English' if language_code == 'en' else 'Hindi'}."
            try:
                groq_chat = ChatGroq(api_key=groq_api_key, model_name='mixtral-8x7b-32768')
                conversation = ConversationChain(llm=groq_chat, memory=memory)
                conversation.run(instruction)
                st.session_state.language_instruction_sent = True
                st.session_state.language = language_code
            except Exception as e:
                st.error(f"Error setting language preference: {e}")

        # Process user question with GroqBot
        if user_question:
            try:
                groq_chat = ChatGroq(api_key=groq_api_key, model_name='mixtral-8x7b-32768')
                conversation = ConversationChain(llm=groq_chat, memory=memory)

                # Get bot response for the user question
                response = conversation.run(user_question)

                # Append current interaction to the chat history
                message = {'human': user_question, 'bot': response}
                st.session_state.chat_history.append(message)

                # Display the bot's response
                st.write(f"Bot: {response}")
            except Exception as e:
                st.error(f"Error processing your question: {e}")

        # Display chat history
        st.subheader("Chat History")
        for message in st.session_state.chat_history:
            st.write(f"**Human**: {message['human']}")
            st.write(f"**Bot**: {message['bot']}")

    if __name__ == "__main__":
        main()

