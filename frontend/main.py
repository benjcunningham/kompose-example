import os

import requests
import streamlit as st


BASE_API_URL = os.environ["BASE_API_URL"]


def main():

    st.title("kompose-example")

    url = os.path.join(BASE_API_URL, "hello")
    res = requests.get(url)

    if res.ok:
        st.success(res.json())
    else:
        st.error("Cannot connect to backend")


if __name__ == "__main__":
    main()
