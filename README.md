# POC Python Realtime API o1 assistant
> This is a proof of concept that expands on IndyDevDan's project that uses OpenAI's [Realtime API](https://openai.com/index/introducing-the-realtime-api/) to chain tools, call o1-preview & o1-mini, [structure output](https://openai.com/index/introducing-structured-outputs-in-the-api/) responses, and glimpse into the future of **AI assistant powered engineering**.

This iteration adds functionalities that allow the AI to take actions on the user's computer using PythonAutoGUI to click the mouse.
A screenshot of the user's screen is sent to GPT-4o with a prompt for consideration, GPT-4o maps coordinates to the screen based on the user's request, and finally, the mouse is clicked at those coordinates using PythonAutoGUI.


## Setup
- [Install uv](https://docs.astral.sh/uv/), the hyper modern Python package manager.
- Setup environment `cp .env.sample .env` add your `OPENAI_API_KEY`
- Update `personalization.json` to fit your setup
- Install dependencies `uv sync`
- Run the realtime assistant `uv run main`

## Try This

Here are some voice commands you can try with the assistant:

1. "Hey Sage, How are you?"
2. "What's the current time?"
3. "Generate a random number."
4. "Open Amazon."
5. "Search Amazon for Groceries."
6. "Click the Celery, Add to cart."

## Code Breakdown

### Main Script (`main.py`)
The `main.py` script serves as the entry point for the application. It sets up the WebSocket connection, handles audio input/output, and manages the interaction between the user and the AI assistant.

### Environment and Personalization Setup
The application uses environment variables (loaded from a `.env` file) and a `personalization.json` file to customize the assistant's behavior and store API keys.

### Function Definitions
Several functions are defined to handle various tasks:
- `get_current_time()`: Returns the current time.
- `get_random_number()`: Generates a random number between 1 and 100.
- `open_browser()`: Opens specified URLs in the browser.
- `create_file()`: Creates a new file with generated content.
- `update_file()`: Updates an existing file's content.
- `delete_file()`: Deletes a specified file.

These functions can be called by the AI assistant to perform actions based on user requests.

### AsyncMicrophone Class
The `AsyncMicrophone` class manages asynchronous audio input, allowing for real-time speech capture and processing.

### WebSocket Connection and Event Handling
The application establishes a WebSocket connection with the OpenAI Realtime API. It handles various events such as `response.created`, `response.done`, and function calls, enabling real-time interaction with the AI assistant.

### Audio Processing
Audio data is captured, encoded in base64, and sent over the WebSocket. The `play_audio()` function handles playback of the assistant's audio responses.

### Runtime Logging and Decorators
The `timeit_decorator` is used to log execution times of functions. Runtime information is logged to `runtime_time_table.jsonl` for performance analysis.

### Entry Point (`main()` Function)
The `main()` function initializes the application, sets up the WebSocket connection, and manages the main event loop for user interaction.

### Additional Resources and Utilities
The codebase includes various utility functions for tasks such as structured output prompts, chat prompts, and audio encoding/decoding.

## Improvements
> Up for a challenge? Here are some ideas on how to improve the experience:

- Organize code.
- Add interruption handling. Current version prevents it for simplicity.
- Add transcript logging.
- Make personalization.json a pydantic type.
- Let tools run in parallel.
- Fix audio randomly cutting out near the end.

## Resources
- https://openai.com/index/introducing-the-realtime-api/
- https://openai.com/index/introducing-structured-outputs-in-the-api/
- https://platform.openai.com/docs/guides/realtime/events
- https://platform.openai.com/docs/api-reference/realtime-client-events/response-create
- https://platform.openai.com/playground/realtime
- https://github.com/Azure-Samples/aoai-realtime-audio-sdk/blob/main/README.md
- https://docs.astral.sh/uv/
