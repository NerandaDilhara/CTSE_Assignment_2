import pytest
import os
from tools.task_router_tool import get_task_router_tool

def test_missing_file_path():
    state = {}
    tool = get_task_router_tool(state)
    result = tool("")
    assert "Missing file path" in result

def test_invalid_file_type():
    state = {}
    tool = get_task_router_tool(state)
    result = tool("dummy.txt")
    assert "Invalid file extension" in result

def test_valid_pdf_path(tmp_path):
    # create a dummy PDF file
    p = tmp_path / "dummy.pdf"
    p.write_text("dummy")
    
    state = {}
    tool = get_task_router_tool(state)
    result = tool(str(p))
    assert "Validation successful" in result
    assert state.get("file_path") == str(p)
    assert state.get("status") == "validated"
    assert state.get("next_agent") == "paper_reader_agent"
