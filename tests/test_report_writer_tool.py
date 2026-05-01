import pytest
import os
import shutil
from tools.report_writer_tool import get_report_writer_tool

def test_report_file_creation():
    state = {
        "paper_title": "Test Creation",
        "objectives": ["Test"],
        "findings": ["Test OK"]
    }
    tool = get_report_writer_tool(state)
    
    # ensure outputs dir doesn't exist to test creation 
    # but be safe not to break actual dir in tests
    if os.path.exists("outputs"):
        shutil.rmtree("outputs")
        
    result = tool("generate")
    assert "successfully saved" in result
    assert os.path.exists("outputs/final_report.md")
    assert state.get("status") == "completed"

def test_missing_output_directory_handling():
    # Similar to above, check if it creates the directory automatically
    state = {}
    tool = get_report_writer_tool(state)
    
    if os.path.exists("outputs"):
        shutil.rmtree("outputs")
        
    tool("generate")
    assert os.path.exists("outputs")
    assert os.path.exists("outputs/final_report.md")
