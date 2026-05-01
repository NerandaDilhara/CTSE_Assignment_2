import pytest
import json
from tools.research_insight_tool import get_research_insight_tool

def test_empty_extracted_text():
    state = {}
    tool = get_research_insight_tool(state)
    result = tool('{"paper_title": "Test Title"}')
    assert "empty extracted text" in result

def test_normal_sample_returns_required_fields():
    state = {"extracted_text": "Sample valid text"}
    tool = get_research_insight_tool(state)
    json_input = json.dumps({
        "paper_title": "AI Research",
        "objectives": ["Identify AI limitations"],
        "methodology": "Literature review",
        "findings": ["AI is good"],
        "limitations": ["Requires data"],
        "research_gaps": ["More focus needed"],
        "future_work": ["Better models"]
    })
    
    result = tool(json_input)
    assert "Insights successfully saved" in result
    assert state.get('paper_title') == "AI Research"
    assert len(state.get('objectives')) == 1
    assert state.get('methodology') == "Literature review"
    assert state.get('next_agent') == "report_generator_agent"
