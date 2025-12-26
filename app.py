import streamlit as st
import time
import openai
from questions import questions
from styles_data import styles_info

# Page config
st.set_page_config(page_title="LearnFlow", page_icon="logo.png", layout="wide")

# LOGO SETUP removed
# st.logo("logo.png", size="large")

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
    
    # API Key Input
    st.header("AI Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Get your key at platform.openai.com")
    if api_key:
        st.session_state.api_key = api_key
    
    st.divider()
    if st.button("🏠 Home / Início", use_container_width=True):
        st.session_state.app_mode = "home"
        st.session_state.page_title_override = None
        st.rerun()

# OpenAI Helpers
def get_ai_client():
    if "api_key" in st.session_state and st.session_state.api_key:
        return openai.OpenAI(api_key=st.session_state.api_key)
    return None

def get_ai_response(messages, model="gpt-3.5-turbo"):
    client = get_ai_client()
    if not client:
        return "⚠️ Please enter your OpenAI API Key in the sidebar to use AI features."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
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
    
    /* GLASSMORPHISM CARDS */
    .card-container {
        background: rgba(2, 62, 138, 0.4); /* Secondary Blue low opacity */
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(0, 180, 216, 0.2); /* Cyan border */
        padding: 30px 20px;
        text-align: center;
        margin-bottom: 25px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        /* EQUAL HEIGHT ENFORCEMENT */
        height: 280px; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .card-container:hover {
        transform: translateY(-5px);
        background: rgba(2, 62, 138, 0.6);
        box-shadow: 0 10px 20px rgba(0, 180, 216, 0.2); /* Cyan Glow */
        border: 1px solid rgba(0, 180, 216, 0.8); 
    }
    
    .emoji-icon {
        font-size: 60px;
        margin-bottom: 15px;
        filter: drop-shadow(0 0 10px rgba(0, 180, 216, 0.5));
    }
    
    .card-container h3 {
        font-weight: 700;
        margin-bottom: 10px;
        color: #CAF0F8; /* Light Cyan Text */
    }
    
    .card-container p {
        font-size: 0.9em;
        opacity: 0.9;
        margin-bottom: 20px;
        color: #ADE8F4;
    }
    
    /* CUSTOM BUTTONS */
    div.stButton > button {
        background: linear-gradient(135deg, #0077B6 0%, #00B4D8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0, 180, 216, 0.2);
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 12px rgba(0, 180, 216, 0.4);
        border: none;
        color: white;
    }
    
    /* STICKY FOOTER */
    .sticky-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(0, 18, 51, 0.95); /* Deep Navy */
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(0, 180, 216, 0.2);
        padding: 1rem 5rem;
        z-index: 1000;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
    }
    .sticky-footer .stButton > button {
        background: transparent;
        border: 1px solid #00B4D8;
        color: #00B4D8;
    }
     .sticky-footer .stButton > button:hover {
        background: #00B4D8;
        color: white;
    }
    
    /* CHAT BUBBLES */
    .stChatMessage {
        background-color: transparent;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }
    
    .stChatMessage[data-testid="stChatMessage"]:nth-child(2n) {
        background: rgba(0, 180, 216, 0.1); 
    }
    
    /* TEXT GRADIENT */
    .text-gradient {
        background: linear-gradient(to right, #4361EE 0%, #4CC9F0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        padding-bottom: 10px; /* Prevent clipping */
    }

</style>
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
            <div class="emoji-icon">🤖</div>
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
            <div class="emoji-icon">🧠</div>
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
            <div class="emoji-icon">📝</div>
            <h3>{current_ui['card3_title']}</h3>
            <p>{current_ui['card3_desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(current_ui['card3_btn'], key="btn_corrector", use_container_width=True):
            st.session_state.app_mode = "corrector"
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

# --- MAIN DISPATCHER ---

if "last_lang" not in st.session_state:
    st.session_state.last_lang = lang_code
elif st.session_state.last_lang != lang_code:
    st.session_state.app_mode = "home"
    st.session_state.last_lang = lang_code
    st.session_state.messages = [] 
    st.session_state.tutor_messages = []
    st.rerun()

if st.session_state.app_mode == "home":
    render_home()
elif st.session_state.app_mode == "analyzer":
    render_analyzer()
elif st.session_state.app_mode == "tutor":
    render_tutor()
elif st.session_state.app_mode == "corrector":
    render_corrector()
