import streamlit as st
from pathlib import Path

from services.zip_service import ZipService
from services.tree_service import TreeService
from services.file_service import FileService
from agents.analyst import AnalyzerAgent

st.set_page_config(
    page_title="GenAI Documentation Assistant",
    page_icon="📁",
    layout="wide",
)

st.title("📚 GenAI Documentation Assistant")
st.write("Welcome! Upload a ZIP file to generate project documentation.")

uploaded_file = st.file_uploader(
    label="Upload your project (.zip)",
    type=["zip"],
)

if uploaded_file is not None:
    # Create service objects
    zip_service = ZipService()
    tree_service = TreeService()
    file_service = FileService()
    analyzer_agent = AnalyzerAgent()

    # Save uploaded ZIP
    saved_path = zip_service.save_uploaded_file(uploaded_file)

    # Extract ZIP
    extracted_path = zip_service.extract_zip(saved_path)

    # Generate project tree
    tree = tree_service.generate_tree(extracted_path)

    st.success("ZIP file uploaded successfully!")

    # Project information
    st.subheader("Project Information")

    st.write(f"**File Name:** {uploaded_file.name}")
    st.write(f"**Saved To:** {saved_path}")
    st.write(f"**Extracted To:** {extracted_path}")

    # Project structure
    st.subheader("Project Structure")

    for item in tree:
        st.write(item)

    # File analysis
    st.subheader("File Analysis")

    for item in tree:
        path = Path(item)

        if path.is_file():
            file_data = file_service.read_file(path)

            # Skip unsupported files
            if file_data is None:
                continue

            # Analyze file
            analysis = analyzer_agent.analyze(file_data)

            # Display analysis
            with st.expander(f"📄 {analysis['name']}"):
                st.write(f"**Path:** {analysis['path']}")
                st.write(f"**Extension:** {analysis['extension']}")
                st.markdown(analysis["documentation"])
