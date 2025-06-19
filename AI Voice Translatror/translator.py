import streamlit as st
from googletrans import Translator
from gtts import gTTS
language_dict={"English":"en","Tamil":"ta","Hindi":"hi","french":"fr","Japanese":"ja","Spanish":"es","German":"de"}
st.set_page_config(page_title="🎙️AI Voice Translator",layout="centered")
st.title("🎙️AI Voice Translator")
st.markdown("Hi! Hello Welcome😊")
text=st.text_input("Enter Your Text:")
language_names=st.selectbox("Choose Your Translated Language:",list(language_dict.keys()))
dest=language_dict[language_names]
translator=Translator()
if text and dest:
    try:
        translated=translator.translate(text,dest=dest,src="en")
        trans_text=translated.text
        st.write("**Translated Text**:",trans_text)
        tts=gTTS(text=trans_text,lang=dest)
        tts.save("voice.mp3")
        st.audio("voice.mp3")
    except Exception as e:
        st.write(f'Error:{e}')