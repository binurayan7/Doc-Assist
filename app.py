import streamlit as st
from pathlib import Path

from services.zip_service import ZipService
from services.tree_service import TreeService
from services.file_service import FileService

from agents.analyst import AnalyzerAgent
from agents.planner import PlannerAgent
from agents.writer import WriterAgent
from agents.editor import EditorAgent

from renderer.renderer_service import RendererService

# --------------------------------------------------------
# Page Config
# --------------------------------------------------------

st.set_page_config(
    page_title="GenAI Documentation Assistant",
    page_icon="📁",
    layout="wide",
)

st.title("📚 GenAI Documentation Assistant")
st.write("Upload a ZIP file to generate documentation.")

# --------------------------------------------------------
# Session State
# --------------------------------------------------------

defaults = {
    "generated": False,
    "project": None,
    "analysis": None,
    "plan": None,
    "documentation": "",
    "markdown_path": "",
    "html_path": "",
    "pdf_path": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------------
# Services
# --------------------------------------------------------

zip_service = ZipService()
tree_service = TreeService()
file_service = FileService()

analyzer_agent = AnalyzerAgent()
planner_agent = PlannerAgent()
writer_agent = WriterAgent()
editor_agent = EditorAgent()

renderer = RendererService()

# --------------------------------------------------------
# Upload
# --------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Project (.zip)",
    type=["zip"],
)

# --------------------------------------------------------
# Generate Documentation (Runs ONLY Once)
# --------------------------------------------------------

if uploaded_file is not None and not st.session_state.generated:
    with st.spinner("Generating documentation..."):
        saved_path = zip_service.save_uploaded_file(uploaded_file)

        extracted_path = zip_service.extract_zip(saved_path)

        project = file_service.load_project(extracted_path)

        analysis = analyzer_agent.analyze(project)

        plan = planner_agent.plan(analysis)

        result = writer_agent.write(analysis, plan)

        documentation = result["content"]
        markdown_path = result["path"]

        html_path, pdf_path = renderer.render(markdown_path)

        st.session_state.project = project
        st.session_state.analysis = analysis
        st.session_state.plan = plan
        st.session_state.documentation = documentation
        st.session_state.markdown_path = markdown_path
        st.session_state.html_path = html_path
        st.session_state.pdf_path = pdf_path

        st.session_state.generated = True

# --------------------------------------------------------
# Display Everything
# --------------------------------------------------------

if st.session_state.generated:
    project = st.session_state.project

    st.success("Documentation generated successfully!")

    # -----------------------------------------
    # Project Information
    # -----------------------------------------

    st.subheader("📁 Project Information")

    st.write(f"**Project Name:** {project['project_name']}")

    st.write("### Project Statistics")

    st.write(f"Total Items: {project['stats']['total_items']}")
    st.write(f"Supported Files: {project['stats']['supported_files']}")
    st.write(f"Ignored Files: {project['stats']['ignored_files']}")

    # -----------------------------------------
    # Project Structure
    # -----------------------------------------

    st.subheader("📂 Project Structure")

    for item in project["tree"]:
        st.write(item)

    # -----------------------------------------
    # Tabs
    # -----------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🤖 Analysis",
            "📄 Markdown",
            "👀 Preview",
            "⬇ Downloads",
        ]
    )

    # -----------------------------------------
    # Analysis
    # -----------------------------------------

    with tab1:
        st.subheader("Project Analysis")
        st.json(st.session_state.analysis)

        st.subheader("Documentation Plan")
        st.json(st.session_state.plan)

    # -----------------------------------------
    # Markdown
    # -----------------------------------------

    with tab2:
        st.subheader("Generated Documentation")

        st.markdown(st.session_state.documentation)

        with st.expander("Raw Markdown"):
            st.code(
                st.session_state.documentation,
                language="markdown",
            )

    # -----------------------------------------
    # Preview
    # -----------------------------------------

    with tab3:
        with open(
            st.session_state.html_path,
            "r",
            encoding="utf-8",
        ) as file:
            html = file.read()

        st.components.v1.html(
            html,
            height=800,
            scrolling=True,
        )

    # -----------------------------------------
    # Downloads
    # -----------------------------------------

    with tab4:
        col1, col2 = st.columns(2)

        with col1:
            with open(
                st.session_state.markdown_path,
                "rb",
            ) as file:
                st.download_button(
                    "Download Markdown",
                    file,
                    file_name="documentation.md",
                    mime="text/markdown",
                )

        with col2:
            with open(
                st.session_state.pdf_path,
                "rb",
            ) as file:
                st.download_button(
                    "Download PDF",
                    file,
                    file_name="documentation.pdf",
                    mime="application/pdf",
                )

# -----------------------------------------
# AI Editor
# -----------------------------------------

st.divider()

st.subheader("✏ AI Editor")

instruction = st.text_input(
    "Enter an editing instruction",
    placeholder="Example: Rename the title to Smart Library System",
)

# Debug: Show current instruction
print(f"[DEBUG] Current instruction: '{instruction}'")

if st.button("Apply Changes"):
    print("\n" + "=" * 80)
    print("[DEBUG] Apply Changes button clicked")

    if instruction.strip():
        print(f"[DEBUG] Instruction received: {instruction}")

        with st.spinner("Applying changes..."):
            print("[DEBUG] About to call EditorAgent.edit()")

            updated_markdown = editor_agent.edit(
                st.session_state.documentation,
                instruction,
            )

            print("[DEBUG] Returned from EditorAgent.edit()")

            print(
                f"[DEBUG] Updated markdown length: {len(updated_markdown)} characters"
            )

            st.session_state.documentation = updated_markdown
            print("[DEBUG] Session state updated")

            print(f"[DEBUG] Writing markdown to: {st.session_state.markdown_path}")

            Path(st.session_state.markdown_path).write_text(
                updated_markdown,
                encoding="utf-8",
            )

            print("[DEBUG] Markdown file saved")

            print("[DEBUG] Calling RendererService.render()")

            html_path, pdf_path = renderer.render(st.session_state.markdown_path)

            print("[DEBUG] Renderer completed")
            print(f"[DEBUG] HTML Path: {html_path}")
            print(f"[DEBUG] PDF Path : {pdf_path}")

            st.session_state.html_path = html_path
            st.session_state.pdf_path = pdf_path

            print("[DEBUG] Session state paths updated")

        print("[DEBUG] Rerunning Streamlit app")
        st.success("Documentation updated!")
        st.rerun()

    else:
        print("[DEBUG] Instruction is empty")
        st.warning("Please enter an editing instruction.")
