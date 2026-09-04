#!/usr/bin/env python3
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8010"))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        workers=2,
    )
