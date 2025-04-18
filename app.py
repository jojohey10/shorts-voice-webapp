import streamlit as st
import openai
import requests
import os

# 최신 OpenAI 클라이언트 설정
client = openai.OpenAI(api_key=st.secrets["api"]["openai_key"])

st.set_page_config(page_title="AI 음성 생성기", layout="centered")

st.title("🎙️ AI 음성 생성기 (GPT + ElevenLabs)")
st.markdown("주제를 입력하면 GPT가 대사를 만들고 mp3로 변환해줍니다.")

eleven_key = st.secrets["api"]["elevenlabs_key"]
voice_id = st.secrets["api"]["voice_id"]

topic = st.text_input("주제를 입력하세요")
if st.button("🎧 mp3 생성"):
    if topic.strip() == "":
        st.warning("주제를 입력해주세요.")
    else:
        with st.spinner("대사 생성 중..."):
            prompt = f"Create a short, emotional 5-second monologue about: {topic}"
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            script = response.choices[0].message.content.strip()

        with st.spinner("음성 생성 중..."):
            headers = {
                "xi-api-key": eleven_key,
                "Content-Type": "application/json"
            }
            json_data = {
                "text": script,
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
            }
            tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            audio_response = requests.post(tts_url, headers=headers, json=json_data)

            if audio_response.status_code == 200:
                audio_path = "output.mp3"
                with open(audio_path, "wb") as f:
                    f.write(audio_response.content)
                st.audio(audio_path)
                st.success("✅ 생성 완료!")
                st.download_button("📥 mp3 다운로드", audio_response.content, file_name="voice.mp3")
            else:
                st.error("❌ 음성 생성 실패. API 키를 확인해주세요.")
