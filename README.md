# 🤖 Chatbot Admin Kampus – Politeknik Insan Tazakka

Chatbot FAQ berbasis AI semantic similarity + context memory  
untuk menjawab pertanyaan resmi kampus secara otomatis.

## Fitur
- Intent detection berbasis Sentence-Transformers
- Dukungan Bahasa Indonesia
- Context memory (multi-turn)
- Dataset domain kampus
- Web integration (Flask)

## Tech Stack
- Python
- Flask
- Sentence-Transformers
- PyTorch
- YAML dataset

## Cara Menjalankan (Local)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
