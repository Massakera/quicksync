import uvicorn


def main():
    """Run the server."""
    uvicorn.run(
        "quicksync.src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()