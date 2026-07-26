import json
import sys

sys.path.insert(0, r"C:\AI\mcp")
import comfyui_mcp as m

print("status:", json.dumps(m.api_status(), indent=2)[:500])
print("queue:", m.queue_remaining())
print("recent:", json.dumps(m.recent_outputs(3), indent=2)[:400])
print("MCP TOOL FUNCTIONS OK")
