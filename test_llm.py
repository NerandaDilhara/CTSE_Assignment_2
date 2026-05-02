from main import run_workflow
try:
    res = run_workflow("nonexistent.pdf")
    print(res)
except Exception as e:
    import traceback
    traceback.print_exc()
