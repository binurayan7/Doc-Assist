import streamlit as st
from pathlib import Path

from services.zip_service import ZipService
from services.tree_service import TreeService
from services.file_service import FileService
from agents.analyst import AnalyzerAgent
from agents.planner import PlannerAgent
from agents.writer import WriterAgent
from renderer.renderer_service import RendererService

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
    planner_agent = PlannerAgent()
    writer_agent = WriterAgent()
    renderer = RendererService()
    # Save uploaded ZIP
    saved_path = zip_service.save_uploaded_file(uploaded_file)

    # Extract ZIP
    extracted_path = zip_service.extract_zip(saved_path)

    # Generate project tree
    tree = tree_service.generate_tree(extracted_path)

    # Load complete project
    project = file_service.load_project(extracted_path)

    st.success("ZIP file uploaded successfully!")

    # Project Information
    st.subheader("📁 Project Information")

    st.write(f"**Project Name:** {project['project_name']}")
    st.write(f"**Saved To:** {saved_path}")
    st.write(f"**Extracted To:** {extracted_path}")

    st.write("### Project Statistics")

    st.write(f"**Total Items:** {project['stats']['total_items']}")
    st.write(f"**Supported Files:** {project['stats']['supported_files']}")
    st.write(f"**Ignored Files:** {project['stats']['ignored_files']}")

    # Project Structure
    st.subheader("📂 Project Structure")

    for item in project["tree"]:
        st.write(item)

    # Prompt Preview (For Debugging)
    with st.expander("📝 Prompt Sent to Gemini"):
        st.text(analyzer_agent.build_prompt(project))

    # Analyze Project
    analysis = analyzer_agent.analyze(project)

    # Call Planner
    plan = planner_agent.plan(analysis)

    # Generate document
    documentation = writer_agent.write(analysis, plan)

    # Display Analysis
    st.subheader("🤖 Project Analysis")

    if "error" in analysis:
        st.error(analysis["error"])

        st.text_area(
            "Raw Gemini Response",
            analysis["raw_response"],
            height=400,
        )

    else:
        st.success("Project analyzed successfully!")

        st.json(analysis)
    st.subheader("📋 Documentation Plan")

    if "error" in plan:
        st.error(plan["error"])

        st.text_area(
            "Raw Planner Response",
            plan["raw_response"],
            height=400,
        )

    else:
        st.success("Documentation plan generated successfully!")

        st.json(plan)

    # display document
    st.subheader("📄 Generated Documentation")

    st.markdown(documentation)

    with st.expander("Raw Markdown"):
        st.code(documentation, language="markdown")

    # ---------------------------------------------------------
# Display Generated Documentation
# ---------------------------------------------------------

st.subheader("📄 Generated Documentation")

st.markdown(documentation)

with st.expander("Raw Markdown"):
    st.code(documentation, language="markdown")

# ---------------------------------------------------------
# Save Markdown
# ---------------------------------------------------------

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

markdown_path = output_dir / "documentation.md"

markdown_path.write_text(documentation, encoding="utf-8")

st.success(f"Markdown saved to {markdown_path}")

# ---------------------------------------------------------
# Render HTML & PDF
# ---------------------------------------------------------

st.subheader("📑 Rendering Documentation")

html_path, pdf_path = renderer.render(str(markdown_path))

st.success("HTML & PDF generated successfully!")

# ---------------------------------------------------------
# HTML Preview
# ---------------------------------------------------------

st.subheader("📖 HTML Preview")

with open(html_path, "r", encoding="utf-8") as file:
    html = file.read()

st.components.v1.html(html, height=800, scrolling=True)

# ---------------------------------------------------------
# Downloads
# ---------------------------------------------------------

st.subheader("⬇ Download Files")

col1, col2 = st.columns(2)

with col1:
    with open(markdown_path, "rb") as file:
        st.download_button(
            label="Download Markdown",
            data=file,
            file_name="documentation.md",
            mime="text/markdown",
        )

with col2:
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="Download PDF",
            data=file,
            file_name="documentation.pdf",
            mime="application/pdf",
        )
