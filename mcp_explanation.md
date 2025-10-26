# Understanding MCP Client-Server Communication

## `async with stdio_client(server_params) as (read, write):`

This line:
1. Launches the server using the parameters you defined
2. Creates `read` and `write` streams to communicate with it
3. The `async with` ensures everything is cleaned up properly when done

Think of it like opening a pipe: one end reads from the server, the other writes to it.

---

## `if __name__ == "__main__": mcp.run(transport="stdio")`

This is a Python pattern that says: **"If this file is being run directly (not imported), start the MCP server using stdio transport."**

Breaking it down:
- `if __name__ == "__main__"`: Only runs if someone executes `python server.py` directly (not if another file imports it)
- `mcp.run(transport="stdio")`: Starts the FastMCP server and listens for commands on stdin/stdout

**The transport="stdio" part** means: "Communicate via standard input/output" — which matches what your client expects when it uses `stdio_client`.

---

## StdioServerParameters (Python)

In your Python code, you configure how to launch the server:

```python
server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
    env=None
)
```

This tells your client: "Start a Python process running `server.py` and communicate via stdin/stdout."

---

## MCP Configuration (Cursor IDE)

In Cursor's `mcp.json`, you configure the same thing:

```json
{
  "mcpServers": {
    "aie8-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "~/Documents/projects/repositories/learning/AIE8-MCP-Session",
        "run",
        "server.py"
      ]
    }
  }
}
```

This tells Cursor: "Use `uv` to navigate to this directory and run `server.py`." This allows Cursor to access your custom tools directly in the editor.

---

## How They Work Together

```
Python Client (main.py)
    ↓
stdio_client launches server.py as subprocess
    ↓
server.py starts: mcp.run(transport="stdio")
    ↓
ClientSession connects via read/write streams
    ↓
Client loads tools from server
    ↓
GPT-4o-mini agent uses tools to answer queries
```

---

## Alternative: Cursor IDE Integration

```
Cursor IDE reads mcp.json
    ↓
Launches server via: uv --directory ~/path run server.py
    ↓
server.py starts: mcp.run(transport="stdio")
    ↓
Cursor connects via read/write streams
    ↓
Cursor loads your tools (web_search, roll_dice, get_news)
    ↓
You can use these tools directly in the editor
```
