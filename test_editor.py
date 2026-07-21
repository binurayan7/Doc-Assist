from agents.editor import EditorAgent

markdown = """
# Library Management System

## Introduction

This project manages books.
"""

instruction = "Rename the title to Smart Library System."

editor = EditorAgent()

result = editor.edit(markdown, instruction)

print(result)
