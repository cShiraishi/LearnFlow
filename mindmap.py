import streamlit as st
from groq import Groq
import os
from stats_manager import add_xp

# Helper to get AI client (reused from app.py logic essentially, or passed in)
# Since this is a separate module, we'll implement a simple client getter or rely on session state if available.
# Ideally app.py passes the client, but for simplicity we'll re-instantiate or check secrets.

def get_groq_client():
    api_key = None
    if "api_key" in st.session_state and st.session_state.api_key:
        api_key = st.session_state.api_key
    elif "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    
    if not api_key:
        return None
    return Groq(api_key=api_key)

def render_mind_map():
    st.markdown("<h2 class='text-gradient'>🕸️ AI Mind Map Creator</h2>", unsafe_allow_html=True)
    st.write("Enter a topic or paste your notes below. The AI will generate a visual mind map for you.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.text_area("Topic or Notes", height=200, placeholder="E.g., The Water Cycle, Photosynthesis, History of Rome...")
    
    with col2:
        st.info("💡 **Tip:** Be specific! For example, instead of 'Biology', try 'Cell Structure and Function'.")
        if st.button("Generate Mind Map 🚀", type="primary", use_container_width=True):
            if not user_input:
                st.warning("Please enter some text first.")
            else:
                client = get_groq_client()
                if not client:
                    st.warning("⚠️ API Key missing. Please enter it below:")
                    api_key_input = st.text_input("Groq API Key (Temporary)", type="password", key="mindmap_key_input")
                    if api_key_input:
                        st.session_state.api_key = api_key_input
                        st.success("Key saved! Click Generate again.")
                        # Ideally rerunning would be smoother but pressing the button again works too.
                else:
                    with st.spinner("Brainstorming connections..."):
                        try:
                            # Prompt for Graphviz DOT
                            prompt = f"""
                            Create a Graphviz DOT code for a mind map about the following text:
                            "{user_input}"
                            
                            Rules:
                            1. Return ONLY the valid DOT code inside a code block.
                            2. Use a modern, colorful style (nodes with filled colors).
                            3. Do not include any markdown styling like ```dot or ```graphviz, just the code. 
                            4. If the input is simple, expand on it with related concepts.
                            5. Use 'digraph G' and ensuring logic flow.
                            """
                            
                            completion = client.chat.completions.create(
                                messages=[
                                    {"role": "system", "content": "You are a data visualization expert capable of generating Graphviz DOT code. Return ONLY raw DOT code."},
                                    {"role": "user", "content": prompt}
                                ],
                                model="llama-3.3-70b-versatile",
                                temperature=0.5,
                            )
                            
                            dot_code = completion.choices[0].message.content
                            
                            # Clean up code blocks if the LLM adds them despite instructions
                            dot_code = dot_code.replace("```dot", "").replace("```graphviz", "").replace("```", "").strip()
                            
                            st.session_state.last_mindmap = dot_code
                            
                            # --- GAMIFICATION TRIGGER ---
                            new_xp, new_level, leveled_up = add_xp(20)
                            if leveled_up:
                                st.balloons()
                                st.success(f"🎉 LEVEL UP! You are now Level {new_level}!")
                            else:
                                st.toast(f"+20 XP! (Total: {new_xp})")
                                
                            st.success("Mind Map Generated!")
                            
                        except Exception as e:
                            st.error(f"Error generating map: {str(e)}")

    # Display Result
    if "last_mindmap" in st.session_state:
        st.write("---")
        st.subheader("Your Mind Map")
        try:
            st.graphviz_chart(st.session_state.last_mindmap)
            with st.expander("View DOT Code"):
                st.code(st.session_state.last_mindmap)
        except Exception as e:
            st.error(f"Error rendering graph: {e}. The AI might have produced invalid DOT code. Try again.")
