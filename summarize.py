import openai
import streamlit as st
from bs4 import BeautifulSoup
import requests

openai.api_key = "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"

def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.get_text()
        return texts.strip()
    except:
        return None

def summarize(url):
    website_text = fetch_text_from_url(url)
    if not website_text:
        return "Gagal mengambil konten dari URL."

    messages = [
    {
        "role": "system",
        "content": (
            "Kamu adalah asisten AI yang merangkum halaman web dalam format Markdown. "
            "Gunakan struktur seperti:\n\n"
            "## Judul Ringkasan\n\n"
            "Paragraf pembuka\n\n"
            "### Ringkasan Berita Utama:\n"
            "- Point 1\n"
            "- Point 2\n"
            "- Point 3\n\n"
            "Tulis seolah kamu menulis artikel ringkasan untuk dibaca manusia. Jangan gunakan tanda bintang (*) di mana pun."
        )
    },
    {
        "role": "user",
        "content": (
            f"Tolong ringkas konten halaman berikut ini:\n\n{website_text}\n\n"
            "Tampilkan hasilnya dalam format markdown yang jelas dan rapi, tanpa menggunakan tanda * sama sekali."
        )
    }
]

    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages
    )

    return response.choices[0].message.content

st.set_page_config(page_title="Web Summarizer", layout="centered")
st.image("logo.png", width=150)
st.title("Web Summarizer")
st.markdown("Masukkan URL halaman yang mau diringkas:")

url_input = st.text_input("URL Website", placeholder="https://contoh.com")

if st.button("Summarize"):
    if url_input.startswith("http://") or url_input.startswith("https://"):
        with st.spinner("Lagi proses..."):
            summary = summarize(url_input)
            st.markdown(summary, unsafe_allow_html=True)
    else:
        st.error("Masukkan URL yang valid (harus diawali http:// atau https://)")
