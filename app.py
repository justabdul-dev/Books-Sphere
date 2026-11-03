import streamlit as st
from pypdf import PdfReader
from summarizer import summarize_text

# Page configuration
st.set_page_config(
    page_title="Books Sphere",
    page_icon="📚",
    layout="wide"
)

# Application title
st.title("📚 Welcome to Books Sphere")
st.subheader("Your AI-Powered Reading Companion")

st.write("Discover smarter reading with artificial intelligence.")

# Initialize session state
if "book_text" not in st.session_state:
    st.session_state["book_text"] = ""

# Sidebar navigation
st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Choose a section",
    [
        "Home",
        "My Library",
        "AI Book Assistant",
        "Reading Progress"
    ]
)

# HOME PAGE
if menu == "Home":

    st.header("Welcome, Reader!")

    st.info("Your personal reading journey starts here.")

    st.write(
        "Upload books, explore summaries, "
        "and interact with your AI reading companion."
    )


# MY LIBRARY PAGE
elif menu == "My Library":

    st.header("📖 My Library")

    uploaded_file = st.file_uploader(
        "Upload your PDF book",
        type=["pdf"]
    )

    if uploaded_file is not None:

        try:

            pdf_reader = PdfReader(uploaded_file)

            total_pages = len(pdf_reader.pages)

            st.success("PDF uploaded successfully!")

            st.write("Total pages:", total_pages)

            # Extract PDF text
            extracted_text = ""

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:

                    extracted_text += page_text + "\n"

            # Store extracted text
            st.session_state["book_text"] = extracted_text

            if extracted_text.strip():

                st.success("Your book has been read successfully!")

                # Display extracted content
                st.subheader("📄 Extracted Book Content")

                st.text_area(
                    "PDF Text",
                    extracted_text,
                    height=300
                )

                # BOOK SUMMARIZATION
                st.subheader("📚 Book Summary")

                if st.button("Generate Summary"):

                    with st.spinner("Analyzing your book..."):

                        summary = summarize_text(
                            extracted_text,
                            sentence_count=5
                        )

                    st.success("Summary generated successfully!")

                    st.write(summary)

            else:

                st.warning(
                    "No readable text found. "
                    "This PDF might contain scanned images."
                )

        except Exception as e:

            st.error(f"Error reading PDF: {e}")


# AI BOOK ASSISTANT PAGE
elif menu == "AI Book Assistant":

    st.header("🤖 AI Book Assistant")

    st.write(
        "Ask questions about your uploaded PDF book."
    )

    # Check whether a book has been uploaded
    if not st.session_state["book_text"].strip():

        st.warning(
            "Please upload a readable PDF in My Library first."
        )

    else:

        question = st.text_input(
            "Ask a question about your book:"
        )

        if st.button("Find Answer"):

            if question.strip():

                book_text = st.session_state["book_text"]

                # Divide book into smaller passages
                paragraphs = book_text.split("\n")

                relevant_paragraphs = []

                # Search for matching words
                question_words = set(
                    question.lower().split()
                )

                for paragraph in paragraphs:

                    paragraph_words = set(
                        paragraph.lower().split()
                    )

                    matching_words = (
                        question_words & paragraph_words
                    )

                    if len(matching_words) >= 1:

                        relevant_paragraphs.append(
                            paragraph
                        )

                # Display matching passages
                if relevant_paragraphs:

                    st.success("Relevant passages found!")

                    for passage in relevant_paragraphs[:5]:

                        st.write(passage)

                else:

                    st.warning(
                        "No relevant passages found. "
                        "Try using different keywords."
                    )

            else:

                st.warning("Please enter a question.")


# READING PROGRESS PAGE
elif menu == "Reading Progress":

    st.header("📊 Reading Progress")

    st.info(
        "Reading progress tracking will be added in a future update."
    )