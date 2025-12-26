import streamlit as st
import time
import google.generativeai as genai
from questions import questions
from styles_data import styles_info
from stats_manager import add_study_time, load_stats, save_stats, add_task, toggle_task, delete_task
from pomodoro import render_pomodoro_timer
from mindmap import render_mind_map

# Page config
st.set_page_config(page_title="LearnFlow", page_icon="logo.png", layout="wide")

# Initialize Session Timer
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Function to update time on interaction
def track_time():
    now = time.time()
    elapsed = now - st.session_state.start_time
    # Only update if meaningful time passed (> 10s)
    if elapsed > 10:
        add_study_time(elapsed)
        st.session_state.start_time = now # Reset timer

# Language Selection
lang_options = {
    "Português": "pt",
    "English": "en",
    "Español": "es",
    "Deutsch": "de"
}

# Sidebar
with st.sidebar:
    st.header("Language / Idioma")
    selected_lang_name = st.selectbox("Select Language", list(lang_options.keys()))
    lang_code = lang_options[selected_lang_name]
    
    st.divider()
    
    st.divider()
    # API Key Input Removed by User Request

    # GAMIFICATION UI
    stats = load_stats()
    user_level = stats.get("level", 1)
    user_xp = stats.get("xp", 0)
    xp_needed = user_level * 100
    
    st.markdown(f"### 🛡️ Level {user_level}")
    st.progress(min(user_xp / xp_needed, 1.0))
    st.caption(f"XP: {user_xp} / {xp_needed}")
    
    st.divider()

    # RADIO WIDGET
    with st.expander("🎵 Study Radio", expanded=False):
        # Embed User Selection
        st.components.v1.iframe("https://www.youtube.com/embed/mM1dIwGO00w", height=200)
        st.caption("Note: Audio may stop if you switch pages.")

    st.divider()
    if st.button("🏠 Home / Início", use_container_width=True):
        st.session_state.app_mode = "home"
        st.session_state.page_title_override = None
        st.rerun()

import google.generativeai as genai

# ... (Previous imports remain, just removing Groq)

# Gemini Helpers
def get_ai_response(messages, model_name="gemini-2.5-flash"):
    # Retrieve API Key
    api_key = None
    if "api_key" in st.session_state and st.session_state.api_key:
        api_key = st.session_state.api_key
    elif "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    
    if not api_key:
        return "⚠️ Please configure your Gemini API Key in `.streamlit/secrets.toml` or provide it."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # Convert messages to Gemini format (simplification)
        # Gemini expects a prompt string or list of contents.
        # For simple chat, we can concatenate or just send the last user message if stateless, 
        # but for a "chat" we should construct history. 
        # For this specific helper which seems to be used for one-off tasks (like Tutor/Corrector), 
        # we'll constructing a single prompt if possible or standard chat.
        
        # 'messages' arg usually comes as list of dicts: [{"role": "user", "content": "..."}]
        # Let's flatten it for simplicity or use start_chat.
        
        full_prompt = ""
        for msg in messages:
             full_prompt += f"{msg['role'].upper()}: {msg['content']}\n"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# UI Text Translations
ui_text = {
    "pt": {
        "title": "LearnFlow",
        "home_title": "Bem-vindo ao LearnFlow",
        "home_subtitle": "Sua plataforma completa de potencialização de estudos.",
        "card1_title": "Studying AI",
        "card1_desc": "Tire dúvidas e estude qualquer assunto com IA.",
        "card1_btn": "Iniciar Chat",
        "card2_title": "Study Analyzer",
        "card2_desc": "Descubra seu estilo de aprendizagem (VARK).",
        "card2_btn": "Fazer Teste",
        "card3_title": "Answer Corrector",
        "card3_desc": "Corrija e melhore suas respostas escritas.",
        "card3_btn": "Corrigir Texto",
        "intro": "Olá! Sou seu assistente de produtividade. Vou te fazer 15 perguntas para descobrir qual é a sua melhor forma de aprender e trabalhar. Vamos começar?",
        "intro_restart": "Olá! Vamos descobrir seu estilo de aprendizagem novamente?",
        "choose": "Escolha uma opção:",
        "result_title": "**Análise Concluída!** 🎉",
        "result_predominant": "Seu estilo predominante é:",
        "meaning_title": "**O que isso significa?**",
        "tips_title": "**Dicas de Produtividade:**",
        "combo_title": "**💡 Super Combinação:**",
        "progress": "Pergunta {} de {}",
        "restart": "Reiniciar Teste",
        "tutor_intro": "Olá! Sou o Studying AI. Sobre qual assunto você quer estudar hoje?",
        "tutor_input": "Digite sua dúvida aqui...",
        "corrector_intro": "Cole sua resposta abaixo e eu vou corrigir e sugerir melhorias.",
        "corrector_input": "Cole seu texto aqui...",
        "corrector_btn": "Analisar e Corrigir",
        "corrector_result": "### Correção Sugerida",
        "corrector_system_prompt": "Você é um professor prestativo. Corrija o texto fornecido para erros gramaticales, clareza e estilo. Forneça o texto corrigido e uma breve explicação das melhorias.",
        "ai_recs_title": "### 🤖 Recomendações da IA",
        "ai_recs_loading": "Gerando estratégias de estudo personalizadas..."
    },
    "en": {
        "title": "LearnFlow",
        "home_title": "Welcome to LearnFlow",
        "home_subtitle": "Your complete study enhancement platform.",
        "card1_title": "Studying AI",
        "card1_desc": "Ask questions and study any topic with AI.",
        "card1_btn": "Start Chat",
        "card2_title": "Study Analyzer",
        "card2_desc": "Discover your learning style (VARK).",
        "card2_btn": "Take Test",
        "card3_title": "Answer Corrector",
        "card3_desc": "Correct and improve your written answers.",
        "card3_btn": "Correct Text",
        "intro": "Hello! I'm your productivity assistant. I'll ask you 15 questions to find your best way of learning. Shall we start?",
        "intro_restart": "Hello! Shall we discover your learning style again?",
        "choose": "Choose an option:",
        "result_title": "**Analysis Complete!** 🎉",
        "result_predominant": "Your predominant style is:",
        "meaning_title": "**What does this mean?**",
        "tips_title": "**Productivity Tips:**",
        "combo_title": "**💡 Super Combo:**",
        "progress": "Question {} of {}",
        "restart": "Restart Test",
        "tutor_intro": "Hello! I am Studying AI. What topic do you want to study today?",
        "tutor_input": "Type your question here...",
        "corrector_intro": "Paste your answer below and I'll correct and suggest improvements.",
        "corrector_input": "Paste your text here...",
        "corrector_btn": "Analyze and Correct",
        "corrector_result": "### Suggested Correction",
         "corrector_system_prompt": "You are a helpful teacher. Correct the provided text for grammatical errors, clarity, and style. Provide the corrected text and a brief explanation of improvements.",
         "ai_recs_title": "### 🤖 AI Recommendations",
         "ai_recs_loading": "Generating personalized study strategies..."
    },
    "es": {
        "title": "LearnFlow",
        "home_title": "Bienvenido a LearnFlow",
        "home_subtitle": "Tu plataforma completa para mejorar estudios.",
        "card1_title": "Studying AI",
        "card1_desc": "Haz preguntas y estudia cualquier tema con IA.",
        "card1_btn": "Iniciar Chat",
        "card2_title": "Study Analyzer",
        "card2_desc": "Descubre tu estilo de aprendizaje (VARK).",
        "card2_btn": "Hacer Test",
        "card3_title": "Answer Corrector",
        "card3_desc": "Corrige y mejora tus respuestas escritas.",
        "card3_btn": "Corregir Texto",
        "intro": "¿Hola! Soy tu asistente de productividad. Te haré 15 preguntas para descubrir tu mejor forma de aprender. ¿Empezamos?",
        "intro_restart": "¡Hola! ¿Vamos a descubrir tu estilo de aprendizaje de nuevo?",
        "choose": "Elige una opción:",
        "result_title": "**¡Análisis Completo!** 🎉",
        "result_predominant": "Tu estilo predominante es:",
        "meaning_title": "**¿Qué significa esto?**",
        "tips_title": "**Consejos de Productividad:**",
        "combo_title": "**💡 Super Combinación:**",
        "progress": "Pregunta {} de {}",
        "restart": "Reiniciar Prueba",
        "tutor_intro": "¡Hola! Soy Studying AI. ¿Qué tema quieres estudiar hoy?",
        "tutor_input": "Escribe tu duda aquí...",
        "corrector_intro": "Pega tu respuesta abajo y la corregiré.",
        "corrector_input": "Pega tu texto aquí...",
        "corrector_btn": "Analizar y Corregir",
        "corrector_result": "### Corrección Sugerida",
        "corrector_system_prompt": "Eres un profesor útil. Corrige el texto proporcionado por errores gramaticales, claridad y estilo. Proporciona el texto corregido y una breve explicación de las mejoras.",
        "ai_recs_title": "### 🤖 Recomendaciones de IA",
        "ai_recs_loading": "Generando estrategias de estudio personalizadas..."
    },
    "de": {
        "title": "LearnFlow",
        "home_title": "Willkommen bei LearnFlow",
        "home_subtitle": "Ihre komplette Lernplattform.",
        "card1_title": "Studying AI",
        "card1_desc": "Fragen Sie und lernen Sie jedes Thema mit KI.",
        "card1_btn": "Chat Starten",
        "card2_title": "Study Analyzer",
        "card2_desc": "Entdecken Sie Ihren Lernstil (VARK).",
        "card2_btn": "Test Starten",
        "card3_title": "Answer Corrector",
        "card3_desc": "Korrigieren und verbessern Sie Ihre Antworten.",
        "card3_btn": "Text Korrigieren",
        "intro": "Hallo! Ich bin Ihr Produktivitätsassistent. Ich stelle Ihnen 15 Fragen, um Ihren besten Lernstil zu finden. Wollen wir anfangen?",
        "intro_restart": "Hallo! Wollen wir Ihren Lernstil erneut entdecken?",
        "choose": "Wählen Sie eine Option:",
        "result_title": "**Analyse Abgeschlossen!** 🎉",
        "result_predominant": "Ihr vorherrschender Stil ist:",
        "meaning_title": "**Was bedeutet das?**",
        "tips_title": "**Produktivitätstipps:**",
        "combo_title": "**💡 Super-Kombination:**",
        "progress": "Frage {} von {}",
        "restart": "Test Neu Starten",
        "tutor_intro": "Hallo! Ich bin Studying AI. Welches Thema möchten Sie heute lernen?",
        "tutor_input": "Geben Sie Ihre Frage hier ein...",
        "corrector_intro": "Fügen Sie Ihre Antwort ein und ich korrigiere sie.",
        "corrector_input": "Fügen Sie Ihren Text hier ein...",
        "corrector_btn": "Analysieren und Korrigieren",
        "corrector_result": "### Vorgeschlagene Korrektur",
        "corrector_system_prompt": "Sie sind ein hilfreicher Lehrer. Korrigieren Sie den bereitgestellten Text auf Grammatikfehler, Klarheit und Stil. Geben Sie den korrigierten Text und eine kurze Erklärung der Verbesserungen an.",
        "ai_recs_title": "### 🤖 KI-Empfehlungen",
        "ai_recs_loading": "Generiere personalisierte Lernstrategien..."
    }
}

current_ui = ui_text[lang_code]

# MODERN CSS & THEME
st.markdown("""
<style>
    /* Global Clean Up */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Layout Spacing */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 6rem;
    }
    
    /* ANIMATIONS */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 40px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Apply animation to main container */
    .block-container {
        animation-duration: 0.8s;
        animation-fill-mode: both;
        animation-name: fadeInUp;
    }

    /* GLOBAL BACKGROUND - VISIBLE CALM WAVES */
    .stApp {
        /* Enhanced Visibility Palette: Deep Navy -> Bright Calm Blue -> Royal Blue -> Deep Navy */
        /* Increased contrast to make waves visible, but kept blue spectrum */
        background: linear-gradient(-45deg, #0d1b2a, #415a77, #1b4965, #0d1b2a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite; /* 15s for visible movement */
        height: 100vh;
        position: relative; /* For the glow overlay */
    }

    /* MOUSE GLOW OVERLAY */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none; /* Let clicks pass through */
        z-index: 1; /* Above background, below content */
        /* Radial gradient following the mouse CSS vars - Large Ambient Glow */
        background: radial-gradient(600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(72, 191, 227, 0.1), transparent 40%);
    }
    
    /* CURSOR RING ANIMATION */
    @keyframes cursorSpin {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    
    .stApp::after {
        content: "";
        position: fixed;
        top: var(--mouse-y, -100px);
        left: var(--mouse-x, -100px);
        width: 50px;
        height: 50px;
        border: 2px dashed rgba(255, 255, 255, 0.5); /* Dashed to make rotation visible */
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999; /* Topmost overlay */
        animation: cursorSpin 5s linear infinite; /* Slow consistent rotation */
        box-shadow: 0 0 15px rgba(72, 191, 227, 0.3);
    }

    /* SIDEBAR STYLING - SERENE */
    section[data-testid="stSidebar"] {
        background: linear-gradient(-45deg, #0d1b2a, #415a77, #1b4965, #0d1b2a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        border-right: 1px solid rgba(55, 90, 127, 0.3);
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label {
        color: #dbe9f4 !important; /* Soft White/Blue */
        font-family: 'Outfit', sans-serif;
    }

    /* Force Radio/Expander Header White */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] p,
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    /* IMPORT MODERN FONT */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    
    /* GLASSMORPHISM CARDS */
    .card-container {
        font-family: 'Outfit', sans-serif; 
        background: rgba(31, 58, 95, 0.4); /* Muted Blue Glass */
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(72, 191, 227, 0.2); 
        padding: 30px 20px;
        text-align: center;
        margin-bottom: 25px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        /* EQUAL HEIGHT ENFORCEMENT */
        height: 280px; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        z-index: 10; /* Ensure cards are above glow */
    }
    
    .card-container:hover {
        transform: translateY(-5px);
        background: rgba(31, 58, 95, 0.6);
        box-shadow: 0 10px 20px rgba(72, 191, 227, 0.2); 
        border: 1px solid rgba(72, 191, 227, 0.6); 
    }
    
    .emoji-icon {
        font-size: 60px;
        margin-bottom: 15px;
        filter: drop-shadow(0 0 10px rgba(72, 191, 227, 0.5));
        position: relative; /* For tooltip positioning */
        cursor: help;
    }
    
    /* TOOLTIP HOVER EFFECT */
    .emoji-icon:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(15, 28, 46, 0.95);
        border: 1px solid rgba(72, 191, 227, 0.5);
        color: #edf6f9;
        padding: 5px 12px;
        border-radius: 8px;
        white-space: nowrap;
        font-size: 0.8rem;
        font-family: 'Outfit', sans-serif;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        margin-bottom: 8px;
        z-index: 1000;
        opacity: 0;
        animation: tooltipFadeIn 0.3s forwards;
    }
    
    @keyframes tooltipFadeIn {
        from { opacity: 0; transform: translate(-50%, 5px); }
        to { opacity: 1; transform: translate(-50%, 0); }
    }
    
    .card-container h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        margin-bottom: 10px;
        color: #edf6f9; /* Soft White */
    }
    
    .card-container p {
        font-family: 'Outfit', sans-serif;
        font-size: 0.9em;
        opacity: 0.9;
        margin-bottom: 20px;
        color: #dbe9f4;
    }
    
    /* CUSTOM BUTTONS */
    div.stButton > button {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #375a7f 0%, #1f3a5f 100%); /* Muted Blue Gradient */
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 12px rgba(72, 191, 227, 0.3);
        border: none;
        color: white;
    }
    
    /* STICKY FOOTER */
    .sticky-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(15, 28, 46, 0.95); /* Deep Slate */
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(72, 191, 227, 0.2);
        padding: 1rem 5rem;
        z-index: 1000;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
    }
    .sticky-footer .stButton > button {
        background: transparent;
        border: 1px solid #375a7f;
        color: #375a7f;
    }
     .sticky-footer .stButton > button:hover {
        background: #375a7f;
        color: white;
    }
    
    /* CHAT BUBBLES */
    .stChatMessage {
        background-color: transparent;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        font-family: 'Outfit', sans-serif;
    }
    
    .stChatMessage[data-testid="stChatMessage"]:nth-child(2n) {
        background: rgba(72, 191, 227, 0.1); 
    }
    
    /* FORCE HIGH CONTRAST TEXT */
    h1, h2, h3, h4, h5, h6, .stMarkdown p, .stMarkdown li, .stText {
        color: #e0fbfc !important; /* Light text for readability */
    }
    
    /* Chat Message Specifics */
    .stChatMessage p {
        color: #e0fbfc !important;
    }
    
    /* Fix Input Labels */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
        color: #dbe9f4 !important;
    }
    
    /* TEXT GRADIENT - SERENE */
    .text-gradient {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(120deg, #dbe9f4 0%, #a2d2ff 50%, #bde0fe 100%); /* Soft Paste Blue */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-transform: uppercase; 
        font-size: 4.5rem; 
        letter-spacing: -3px; 
        padding-bottom: 20px; 
        text-shadow: 0 10px 30px rgba(72, 191, 227, 0.2); 
    }

    /* SOCIALS FOOTER */
    .social-footer {
        margin-top: 100px;
        padding: 50px 20px;
        background: rgba(15, 28, 46, 0.6); /* Semi-transparent Deep Slate */
        border-top: 1px solid rgba(72, 191, 227, 0.2);
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(5px);
    }
    
    .social-links {
        display: flex;
        gap: 30px;
        margin-top: 20px;
    }
    
    .social-icon {
        color: #dbe9f4;
        font-size: 24px;
        text-decoration: none;
        transition: all 0.3s ease;
        padding: 10px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.05);
        width: 50px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .social-icon:hover {
        color: #fff;
        background: rgba(72, 191, 227, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 0 15px rgba(72, 191, 227, 0.5);
    }
    
    .footer-text {
        font-family: 'Outfit', sans-serif;
        color: #8da9c4;
        margin-top: 20px;
        font-size: 0.9rem;
    }

</style>

<!-- LOAD FONTAWESOME FOR ICONS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<!-- JAVASCRIPT FOR MOUSE TRACKING -->
<script>
    const doc = window.parent.document;
    doc.addEventListener('mousemove', function(e) {
        const x = e.clientX;
        const y = e.clientY;
        document.documentElement.style.setProperty('--mouse-x', x + 'px');
        document.documentElement.style.setProperty('--mouse-y', y + 'px');
    });
</script>
""", unsafe_allow_html=True)


# Initialize Session State
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "home"

# --- MODES ---

def render_home():
    # Centered Header with Logo
    col1, col2, col3 = st.columns([1, 2, 1]) 
    with col2:
        # Logo removed
        st.markdown(f"<h1 class='text-gradient' style='text-align: center;'>LearnFlow</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #90E0EF; font-size: 1.2rem;'>{current_ui['home_subtitle']}</p>", unsafe_allow_html=True)
    
    st.write("---")
    st.write("") 
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="card-container">
            <div class="emoji-icon" data-tooltip="Ask questions & get explanations">🤖</div>
            <h3>{current_ui['card1_title']}</h3>
            <p>{current_ui['card1_desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(current_ui['card1_btn'], key="btn_tutor", use_container_width=True):
            st.session_state.app_mode = "tutor"
            st.rerun()

    with col2:
        st.markdown(f"""
        <div class="card-container">
            <div class="emoji-icon" data-tooltip="Discover your learning style">🧠</div>
            <h3>{current_ui['card2_title']}</h3>
            <p>{current_ui['card2_desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(current_ui['card2_btn'], key="btn_analyzer", use_container_width=True):
            st.session_state.app_mode = "analyzer"
            st.rerun()

    with col3:
        st.markdown(f"""
        <div class="card-container">
            <div class="emoji-icon" data-tooltip="Check your answers automatically">📝</div>
            <h3>{current_ui['card3_title']}</h3>
            <p>{current_ui['card3_desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(current_ui['card3_btn'], key="btn_corrector", use_container_width=True):
            st.session_state.app_mode = "corrector"
            st.rerun()

    # --- ROW 2 (SCROLL DOWN) ---
    st.write("") 
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card-container">
            <div class="emoji-icon" data-tooltip="Create tests from your notes">🧩</div>
            <h3>Quiz Generator</h3>
            <p>Generate tests from your notes.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Quiz Gen 🧠", use_container_width=True):
            st.session_state.app_mode = "quiz_gen"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card-container">
            <div class="emoji-icon" data-tooltip="Track streaks & study habits">📊</div>
            <h3>Profile & Stats</h3>
            <p>Track your streaks and habits.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Dashboard 📈", use_container_width=True):
            st.session_state.app_mode = "dashboard"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="card-container">
            <div class="emoji-icon" data-tooltip="Manage tasks & priorities">📌</div>
            <h3>Study Planner</h3>
            <p>Priority To-Do List.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open To-Do List", use_container_width=True):
            st.session_state.app_mode = "todo"
            st.rerun()

    # --- ROW 3 (POMODORO) ---
    st.write("")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card-container">
            <div class="emoji-icon" data-tooltip="25min Focus / 5min Break">🍅</div>
            <h3>Pomodoro Focus</h3>
            <p>Timer for deep work sessions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Focus ⏱️", use_container_width=True):
            st.session_state.app_mode = "pomodoro"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card-container">
            <div class="emoji-icon" data-tooltip="Visualize topics with AI">🕸️</div>
            <h3>Mind Map</h3>
            <p>Visual diagrams from notes.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Map 🗺️", use_container_width=True):
            st.session_state.app_mode = "mindmap"
            st.rerun()

def render_analyzer():
    st.markdown(f"### {current_ui['card2_title']}")
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "finished" not in st.session_state:
        st.session_state.finished = False
    
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.session_state.messages = [{"role": "assistant", "content": current_ui["intro"]}]

    avatars = {"assistant": "🤖", "user": "👤"}
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=avatars.get(message["role"])):
            st.write(message["content"])

    def handle_answer(style, option_text):
        st.session_state.messages.append({"role": "user", "content": option_text})
        st.session_state.answers.append(style)
        st.session_state.current_question += 1
        
        if st.session_state.current_question >= len(questions[lang_code]):
            st.session_state.finished = True
            show_result()
        else:
            next_q = questions[lang_code][st.session_state.current_question]
            st.session_state.messages.append({"role": "assistant", "content": next_q["text"]})
            st.rerun()

    def show_result():
        scores = {"Visual": 0, "Auditivo": 0, "Leitura/Escrita": 0, "Cinestésico": 0}
        for ans in st.session_state.answers:
            scores[ans] += 1
        winner_key = max(scores, key=scores.get)
        
        result_text = f"{current_ui['result_title']}\n\n{current_ui['result_predominant']} **{winner_key}**."
        st.session_state.messages.append({"role": "assistant", "content": result_text})
        
        details = styles_info[lang_code][winner_key]
        tips_text = f"{current_ui['meaning_title']}\n{details['definition']}\n\n{current_ui['tips_title']}\n"
        for tip in details['tips']:
            tips_text += f"- {tip}\n"
        tips_text += f"\n{current_ui['combo_title']} {details['productivity_combo']}"
        st.session_state.messages.append({"role": "assistant", "content": tips_text})

        # --- AI RECOMMENDATIONS ---
        client = get_ai_client()
        if client:
             with st.spinner(current_ui["ai_recs_loading"]):
                prompt = f"The user has been identified as a {winner_key} learner based on the VARK model (Language: {lang_code}). Provide 5 specific, creative, and highly effective study techniques for this specific style. Return the response in {lang_code}."
                messages = [{"role": "system", "content": "You are an expert educational psychologist."}, {"role": "user", "content": prompt}]
                ai_tips = get_ai_response(messages)
                
                ai_output = f"{current_ui['ai_recs_title']} ({winner_key})\n\n{ai_tips}"
                st.session_state.messages.append({"role": "assistant", "content": ai_output})
        
        st.rerun()

    if not st.session_state.finished:
        q_data = questions[lang_code][st.session_state.current_question]
        last_msg = st.session_state.messages[-1]
        if last_msg["role"] == "assistant" and last_msg["content"] == current_ui["intro"]:
             st.session_state.messages.append({"role": "assistant", "content": q_data["text"]})
             st.rerun()

        with st.container():
            st.write("---")
            st.markdown('<div class="sticky-footer">', unsafe_allow_html=True)
            total_q = len(questions[lang_code])
            progress = (st.session_state.current_question / total_q)
            st.progress(progress, text=current_ui["progress"].format(st.session_state.current_question + 1, total_q))
            st.write(f"**{current_ui['choose']}**")
            col1, col2 = st.columns(2)
            options = q_data["options"]
            with col1:
                if st.button(options[0]["text"], key=f"q{st.session_state.current_question}_o0", use_container_width=True):
                    handle_answer(options[0]["style"], options[0]["text"])
                if st.button(options[2]["text"], key=f"q{st.session_state.current_question}_o2", use_container_width=True):
                    handle_answer(options[2]["style"], options[2]["text"])
            with col2:
                if st.button(options[1]["text"], key=f"q{st.session_state.current_question}_o1", use_container_width=True):
                    handle_answer(options[1]["style"], options[1]["text"])
                if st.button(options[3]["text"], key=f"q{st.session_state.current_question}_o3", use_container_width=True):
                    handle_answer(options[3]["style"], options[3]["text"])
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown('<div class="sticky-footer">', unsafe_allow_html=True)
            if st.button(current_ui["restart"], type="primary", use_container_width=True):
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.finished = False
                st.session_state.messages = [{"role": "assistant", "content": current_ui["intro_restart"]}]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

def render_tutor():
    st.markdown(f"### {current_ui['card1_title']}")
    
    if "tutor_messages" not in st.session_state:
        st.session_state.tutor_messages = [{"role": "assistant", "content": current_ui["tutor_intro"]}]

    for msg in st.session_state.tutor_messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.write(msg["content"])

    if prompt := st.chat_input(current_ui["tutor_input"]):
        st.session_state.tutor_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing..."):
                response_text = get_ai_response(st.session_state.tutor_messages)
                st.write(response_text)
                
        st.session_state.tutor_messages.append({"role": "assistant", "content": response_text})

def render_corrector():
    st.markdown(f"### {current_ui['card3_title']}")
    st.write(current_ui["corrector_intro"])
    
    text_input = st.text_area(current_ui["corrector_input"], height=200, key="corrector_text")
    
    if st.button(current_ui["corrector_btn"], type="primary"):
        if text_input:
            with st.spinner("Analyzing..."):
                system_prompt = current_ui.get("corrector_system_prompt", "You are a helpful teacher.")
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_input}
                ]
                response_text = get_ai_response(messages)
            
            st.success("Analysis Complete!")
            st.markdown(current_ui["corrector_result"])
            st.markdown(response_text)
        else:
            st.warning("Please enter some text.")

def render_quiz_generator():
    st.markdown(f"<h2 class='text-gradient'>Quiz & Tasks Generator 🧠</h2>", unsafe_allow_html=True)
    st.write("Transform your notes or text into a study quiz or learning tasks instantly.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        source_text = st.text_area("Paste your notes/text here:", height=300, placeholder="Paste a chapter summary, article, or your own notes...")
    
    with col2:
        st.markdown("### Configuration")
        quiz_type = st.selectbox("Type", ["Multiple Choice Quiz", "Learning Tasks / Open Questions", "True/False Test"])
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=5)
        difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard"], value="Medium")
        
        generate_btn = st.button("Generate Quiz 🚀", use_container_width=True)
    
    if generate_btn:
        if not source_text:
            st.warning("Please paste some text first!")
            return
        
        with st.spinner(f"Generating {difficulty} {quiz_type}..."):
            prompt = (
                f"Act as a strict teacher. Generate a {difficulty} {quiz_type} with {num_questions} questions based PROPERLY and ONLY on the following text.\n"
                f"Language: {lang_code}.\n\n"
                f"TEXT:\n{source_text}\n\n"
                f"FORMAT REQUIREMENTS:\n"
            )
            
            if quiz_type == "Multiple Choice Quiz":
                prompt += "Format: Question, 4 Options (A,B,C,D), and then the Correct Answer hidden at the very end."
            elif quiz_type == "True/False Test":
                prompt += "Format: Statement, True/False option, and correct answer at the end."
            else:
                prompt += "Format: Open-ended questions or actionable learning tasks."
            
            messages = [{"role": "user", "content": prompt}]
            response = get_ai_response(messages)
            
            st.divider()
            st.markdown("### 📝 Generated Quiz")
            st.write(response)


def render_dashboard():
    # Update stats before showing
    track_time()
    stats = load_stats()
    
    st.markdown(f"<h2 class='text-gradient'>Profile & Stats 📊</h2>", unsafe_allow_html=True)
    
    # METRICS
    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Streak", f"{stats['current_streak']} days")
    col2.metric("⏳ Total Study Time", f"{int(stats['total_seconds'] / 60)} min")
    col3.metric("📅 Last Session", stats['last_study_date'] if stats['last_study_date'] else "Today")
    
    st.divider()
    
    # CHARTS (Weekly Activity)
    st.subheader("Weekly Activity (Minutes)")
    weekly_data = stats.get("weekly_activity", {})
    st.bar_chart(weekly_data)
    
    st.divider()
    
    # SETTINGS
    st.subheader("Settings ⚙️")
    reminders = st.toggle("Enable Push Reminders 🔔", value=stats.get("reminders_enabled", False))
    if reminders != stats.get("reminders_enabled", False):
        stats["reminders_enabled"] = reminders
        save_stats(stats)
        if reminders:
            st.toast("✅ Reminders Enabled! We'll notify you.")
        else:
            st.toast("🔕 Reminders Disabled.")

def render_todo_list():
    st.markdown(f"<h2 class='text-gradient'>Study Planner & Tasks 📌</h2>", unsafe_allow_html=True)
    
    # --- ADD TASK FORM ---
    with st.form("new_task"):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            task_text = st.text_input("New Task", placeholder="Read Chapter 4...")
        with col2:
            priority = st.selectbox("Priority", ["High 🔴", "Medium 🟠", "Low 🔵"])
        with col3:
            st.write("") # Spacer to align button
            st.write("") 
            add_btn = st.form_submit_button("Add Task ➕")
    
    if add_btn and task_text:
        add_task(task_text, priority)
        st.success("Task Added!")
        st.rerun()

    # --- TASK LIST ---
    st.write("")
    stats = load_stats()
    tasks = stats.get("tasks", [])
    
    if not tasks:
        st.info("No tasks yet. Add one above to get organized!")
        return

    # Sort: High > Medium > Low (Custom Sort Key)
    priority_map = {"High 🔴": 0, "Medium 🟠": 1, "Low 🔵": 2}
    sorted_tasks = sorted(enumerate(tasks), key=lambda x: (priority_map.get(x[1]['priority'], 99), x[1]['created_at']))
    
    st.subheader("Your Tasks")
    
    for original_index, task in sorted_tasks:
        col_mark, col_text, col_del = st.columns([0.5, 4, 0.5])
        
        # Determine Color based on Priority
        color_style = "color: #ADE8F4;"
        if "High" in task['priority']: color_style = "color: #FF6B6B; font-weight: bold;"
        elif "Medium" in task['priority']: color_style = "color: #FFD93D;"
        
        # Strikethrough if done
        display_text = task['text']
        if task['done']:
            display_text = f"<s>{display_text}</s>"
            color_style = "color: gray;"
            
        with col_mark:
            if st.button("✅" if not task['done'] else "Undo", key=f"toggle_{original_index}"):
                toggle_task(original_index)
                st.rerun()
                
        with col_text:
            st.markdown(f"<span style='font-size: 1.1rem; {color_style}'>{task['priority']} | {display_text}</span>", unsafe_allow_html=True)
            
        with col_del:
            if st.button("🗑️", key=f"del_{original_index}"):
                delete_task(original_index)
                st.rerun()

# --- MAIN DISPATCHER ---

if "last_lang" not in st.session_state:
    st.session_state.last_lang = lang_code
elif st.session_state.last_lang != lang_code:
    track_time() # Save on exit
    st.session_state.app_mode = "home"
    st.session_state.last_lang = lang_code
    st.session_state.messages = [] 
    st.session_state.tutor_messages = []
    st.rerun()

if st.session_state.app_mode == "home":
    track_time()
    render_home()
elif st.session_state.app_mode == "analyzer":
    track_time()
    render_analyzer()
elif st.session_state.app_mode == "tutor":
    track_time()
    render_tutor()
elif st.session_state.app_mode == "corrector":
    track_time()
    render_corrector()
elif st.session_state.app_mode == "quiz_gen":
    track_time()
    render_quiz_generator()
elif st.session_state.app_mode == "dashboard":
    render_dashboard()
elif st.session_state.app_mode == "todo":
    render_todo_list()
elif st.session_state.app_mode == "pomodoro":
    render_pomodoro_timer()
elif st.session_state.app_mode == "mindmap":
    render_mind_map()

# --- SOCIALS FOOTER ---
st.markdown("""
<div class="social-footer">
    <div class="social-links">
        <a href="https://github.com/cShiraishi" target="_blank" class="social-icon">
            <i class="fab fa-github"></i>
        </a>
        <a href="https://linkedin.com/in/carlos-shiraishi" target="_blank" class="social-icon"> <!-- Placeholder based on name -->
            <i class="fab fa-linkedin-in"></i>
        </a>
        <a href="mailto:contact@example.com" class="social-icon">
            <i class="fas fa-envelope"></i>
        </a>
    </div>
    <p class="footer-text">Built with 💙 by Carlos Shiraishi • © 2025 LearnFlow</p>
</div>
""", unsafe_allow_html=True)
