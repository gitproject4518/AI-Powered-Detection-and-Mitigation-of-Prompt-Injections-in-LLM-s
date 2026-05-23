import streamlit as st
import requests
import random

st.set_page_config(
    page_title="Secure AI Firewall",
    page_icon="🔐",
    layout="wide"
)

# -------------------
# Session Variables
# -------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if "role" not in st.session_state:
    st.session_state.role=""

if "messages" not in st.session_state:
    st.session_state.messages=[]


# -------------------
# Custom CSS
# -------------------

st.markdown("""

<style>

.main{
background-color:#0E1117;
}

.block-container{
padding-top:1rem;
}

.login-box{
padding:20px;
border-radius:15px;
background:#1E1E1E;
}

</style>

""",unsafe_allow_html=True)


# ======================
# LOGIN SCREEN
# ======================

if not st.session_state.logged_in:

    st.title("🔐 Secure AI Firewall Login")

    col1,col2,col3=st.columns([1,2,1])

    with col2:

        username=st.text_input(
            "Username"
        )

        password=st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            try:

                response=requests.post(
                    "http://127.0.0.1:8000/login",
                    json={
                        "username":username,
                        "password":password
                    }
                )

                result=response.json()

                if result["success"]:

                    st.session_state.logged_in=True
                    st.session_state.role=result["role"]

                    st.success(
                        "Login successful"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid credentials"
                    )

            except Exception as e:

                st.error(
                    f"Backend Error: {e}"
                )

    st.stop()


# ======================
# SIDEBAR
# ======================

with st.sidebar:

    if st.session_state.role=="admin":

        st.title(
            "🛡 Admin Dashboard"
        )

        st.metric(
            "Users",
            random.randint(100,500)
        )

        st.metric(
            "Active Sessions",
            random.randint(10,50)
        )

        st.metric(
            "Threats Detected",
            random.randint(0,20)
        )

        st.markdown("---")

        st.subheader(
            "Recent Threats"
        )

        st.error(
            "Prompt Injection"
        )

        st.warning(
            "Jailbreak Attempt"
        )

        st.info(
            "Suspicious Prompt"
        )

    else:

        st.title(
            "👤 User Dashboard"
        )

        st.metric(
            "My Sessions",
            random.randint(1,10)
        )


    st.markdown("---")

    if st.button("Logout"):

        st.session_state.logged_in=False
        st.session_state.role=""
        st.session_state.messages=[]

        st.rerun()


# ======================
# MAIN CHAT PAGE
# ======================

st.title(
    "🔐 AI Chatbot"
)

st.caption(
    "Self-Healing Prompt Injection Firewall"
)

col1,col2=st.columns([3,1])

# RIGHT PANEL

with col2:

    st.subheader(
        "Security Status"
    )

    risk=random.randint(0,100)

    st.progress(risk)

    st.write(
        f"Risk Score: {risk}%"
    )

    if risk<30:

        st.success(
            "Low Risk"
        )

    elif risk<70:

        st.warning(
            "Medium Risk"
        )

    else:

        st.error(
            "High Risk"
        )


# CHAT AREA

with col1:

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.write(
                msg["content"]
            )

    user_input=st.chat_input(
        "Type message..."
    )

    if user_input:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":user_input
            }
        )

        try:

            response=requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "message":user_input
                }
            )

            bot_reply=response.json()["response"]

        except Exception as e:

            bot_reply=f"Error: {e}"

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":bot_reply
            }
        )

        st.rerun()