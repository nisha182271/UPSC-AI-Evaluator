import streamlit as st
import requests

st.set_page_config(
    page_title="UPSC AI Evaluator",
    page_icon="📝",
    layout="centered"
)

st.title("UPSC AI Evaluator")

st.write(
    "Upload a handwritten answer sheet to evaluate "
    "its content, structure, and presentation."
)

uploaded_file = st.file_uploader(
    "Choose an answer sheet image...",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Display uploaded image
    st.image(
        uploaded_file,
        caption="Uploaded Answer Sheet"
    )

    if st.button("Evaluate Answer"):

        with st.spinner(
            "Processing through pipeline "
            "(Preprocessing → OCR → AI Analysis)..."
        ):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/upload",
                    files=files,
                    timeout=900
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success("Evaluation Complete!")

                    st.subheader("Evaluation Result")

                    st.json(data)

                else:

                    st.error(
                        f"Backend Error ({response.status_code}): "
                        f"{response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI backend. "
                    "Make sure the backend is running on port 8000."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The backend took too long to respond. "
                    "The OCR/AI processing may still be running."
                )

            except Exception as e:

                st.error(f"Unexpected error: {e}")