from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
import streamlit as st
import vertexai

vertexai.init(project="portofolio-zein", location="us-central1")
@st.cache_resource(show_spinner=False)
def LLM_init():
    template = """
    Kamu adalah ensiklopedia dunia, kamu tidak boleh memberikan fakta palsu atau menyebarkan hoax. Namamu adalah Zein AI Assistant. Kamu diciptakan oleh Ahmad Habib Hasan Zein pada Tanggal 4 Desember 2023 dan hingga saat ini masih dalam tahap pengembangan.
    Kamu tidak berafiliasi dengan perusahaan manapun, kamu adalah AI yang dibuat oleh Ahmad Habib Hasan Zein untuk membantu manusia dalam mencari informasi.
    Kamu harus selalu mengutamakan kebenaran dan kejujuran dalam memberikan informasi.
    Kamu dilengkapi dengan fitur google translate yang dapat menerjemahkan bahasa apapun ke bahasa apapun, dan menjawab menggunakan bahasa apapun sesuai dengan bahasa yang digunakan oleh pengguna.
    {chat_history}
        Human: {human_input}
        Chatbot:"""

    promptllm = PromptTemplate(template=template, input_variables=["chat_history", "human_input"])
    memory = ConversationBufferMemory(memory_key="chat_history")

    llm_chain = LLMChain(
        prompt=promptllm,
        llm=VertexAI(),
        memory=memory,
        verbose=True
    )

    return llm_chain


st.set_page_config(page_title="Zein AI Assistant", page_icon="🦜")
st.title('🤖 Zein AI Assistant 🤖')

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi my name is Jarvis and I am your private assistant, how can I help you?"}]

# "st.session_state:", st.session_state.messages

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # with st.spinner('Preparing'):
    llm_chain = LLM_init()
    msg = llm_chain.predict(human_input=prompt)

    # st.write(msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
###