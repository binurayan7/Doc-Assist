import streamlit as st
from pathlib import Path

from services.zip_service import ZipService
from services.tree_service import TreeService
from services.file_service import FileService
from agents.analyst import AnalyzerAgent

st.set_page_config(
    page_title="GenAI Documentation Assistant", page_icon="📁", layout="wide"
)

st.title("📚 GenAI Documentation Assistant")
st.write("Welcome! Upload a ZIP file to generate project documentation.")

uploaded_file = st.file_uploader(label="Upload your project (.zip)", type=["zip"])

if uploaded_file is not None:
    zip_service = ZipService()
    tree_service = TreeService()
    file_service = FileService()
    analyzer_agent = AnalyzerAgent()

    # Save ZIP
    saved_path = zip_service.save_uploaded_file(uploaded_file)

    # Extract ZIP
    extracted_path = zip_service.extract_zip(saved_path)

    # Generate project tree
    tree = tree_service.generate_tree(extracted_path)

    st.success("ZIP file uploaded successfully!")

    st.write("### File Information")
    st.write(f"**File Name:** {uploaded_file.name}")
    st.write(f"**Saved To:** {saved_path}")
    st.write(f"**Extracted To:** {extracted_path}")

    st.subheader("Project Structure")

    for item in tree:
        st.write(item)

    st.subheader("File Analysis")

    # for item in tree:
    #     path = Path(item)

    #     if path.is_file():
    #         file_data = file_service.read_file(path)
    #         st.write(type(file_data))
    #         st.write(file_data)

    #         if file_data is not None:
    #             # analysis = analyzer_agent.analyze(file_data)

    #             # st.write(analysis)

    #             st.write("TYPE:", type(file_data))
    #             st.write("VALUE:", file_data)
    import inspect

st.subheader("File Analysis (Debug)")

# Check which FileService is actually being used
st.write("### FileService Location")
st.code(inspect.getfile(FileService))

st.write("### read_file() Source Code")
# st.code(inspect.getsource(FileService.read_file))
with open(inspect.getfile(FileService), "r", encoding="utf-8") as f:
    st.code(f.read())

for item in tree:
    path = Path(item)

    if path.is_file():
        st.divider()
        st.write(f"### Checking: {path.name}")

        file_data = file_service.read_file(path)

        st.write("Python Type:")
        st.code(str(type(file_data)))

        if file_data is None:
            st.warning("Returned None")
            continue

        if isinstance(file_data, dict):
            st.success("Returned a Dictionary ✅")

            st.write("Keys:")
            st.write(list(file_data.keys()))

            st.write("Metadata:")
            st.json(
                {
                    "name": file_data["name"],
                    "path": file_data["path"],
                    "extension": file_data["extension"],
                }
            )

            st.write("Content Preview:")
            st.code(file_data["content"][:200])

        elif isinstance(file_data, str):
            st.error("Returned a STRING ❌")

            st.write("First 200 characters:")
            st.code(file_data[:200])

        else:
            st.error(f"Unexpected Type: {type(file_data)}")
            st.write(file_data)
