import pytest
from tools.pdf_reader_tool import get_pdf_reader_tool

def test_missing_file_path():
    state = {}
    tool = get_pdf_reader_tool(state)
    result = tool("")
    assert "Missing file path" in result

def test_non_existing_file_path():
    state = {}
    tool = get_pdf_reader_tool(state)
    result = tool("non_existent_file.pdf")
    assert "Error reading PDF" in result
