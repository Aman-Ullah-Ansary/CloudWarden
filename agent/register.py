import streamlit as st
from auth import Auth


def register():

    auth = Auth()

    st.title("📝 Create Account")

    username = st.text_input("Username")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        if not username or not email or not password:

            st.warning(
                "Please fill all fields."
            )

            return

        if password != confirm:

            st.error(
                "Passwords do not match."
            )

            return

        success, message = auth.register(
            username,
            email,
            password
        )

        if success:

            st.success(message)

        else:

            st.error(message)