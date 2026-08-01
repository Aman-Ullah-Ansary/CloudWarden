import streamlit as st
from auth import Auth
from register import register


def login():

    auth = Auth()

    tab1, tab2 = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    with tab1:

        st.title("CloudWarden Login")

        username = st.text_input(
            "Username",
            key="login_user"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        if st.button("Login"):

            if auth.login(
                username,
                password
            ):

                st.session_state["login"] = True

                st.session_state["user"] = username

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    with tab2:

        register()