from flamemirror_sync import sync_memory_from_remote

# Replace this URL with a valid endpoint serving memory.json
sync_memory_from_remote(
    "https://goro-terminal.onrender.com/static/memory.json", overwrite=False)
