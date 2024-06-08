import os

# App settings
title= "Face Recognition"
host = "127.0.0.1"    
port = int(os.environ.get("PORT", 8050))
debug = True

## File system
root        = os.path.dirname(os.path.dirname(__file__)) + "/"