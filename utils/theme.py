import streamlit as st


def initialize_theme():
    """Initialize theme in session state"""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"


def toggle_theme():
    """Toggle between light and dark theme"""
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"


def apply_theme():
    """Apply current theme using Streamlit's native theme"""
    theme = st.session_state.theme

    # Configure theme using Streamlit's config
    st.markdown(
        """
        <style>
        /* Base styles */
        .stApp {
            transition: all 0.3s ease-in-out;

            
        }

        /* Dark theme overrides */
        [data-theme="dark"] {
            --secondary-background-color: #262730;
            --text-color: #ffffft;
            --font: "Source Sans Pro", sans-serif;
        }

        /* Light theme overrides */
        [data-theme="light"] {
            --secondary-background-color: #ffffff;
            --text-color: #000000;
            --font: "Source Sans Pro", sans-serif;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Set theme
    st.markdown(
        f"""
        <script>
            document.body.setAttribute('data-theme', '{theme}');
        </script>
    """,
        unsafe_allow_html=True,
    )
