import argparse
import logging
import time
import re
import pandas as pd  # For more sophisticated data analysis and reporting (if needed)

try:
    import pyperclip  # Requires installing: pip install pyperclip
except ImportError:
    print("Pyperclip module not found. Please install it: pip install pyperclip")
    exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Monitors the system clipboard for sensitive data and alerts the user."
    )

    # Add arguments here if needed.  Example:
    # parser.add_argument(
    #     "--log-level",
    #     choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    #     default="INFO",
    #     help="Set the logging level.",
    # )

    return parser.parse_args()


def detect_sensitive_data(text):
    """
    Detects sensitive data in the given text using regular expressions.

    Args:
        text (str): The text to analyze.

    Returns:
        list: A list of detected sensitive data types. Empty if none are found.
    """
    detections = []

    # Credit card number pattern (very basic, needs improvement for real-world use)
    if re.search(r"\b(?:\d[ -]*?){13,16}\b", text):
        detections.append("Credit Card Number (Possible)")

    # API key pattern (example, adjust as needed)
    if re.search(r"\b(?:API_KEY|apikey)=[\w-]+\b", text):
        detections.append("API Key (Possible)")

    # Simple email pattern
    if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
      detections.append("Email address (Possible)")


    return detections


def main():
    """
    Main function to monitor the clipboard and detect sensitive data.
    """
    args = setup_argparse()

    # Set logging level (if argument is added)
    # logging.getLogger().setLevel(args.log_level)

    logging.info("Clipboard monitor started. Press Ctrl+C to stop.")

    previous_clipboard_content = ""

    try:
        while True:
            try:
                clipboard_content = pyperclip.paste()
            except pyperclip.PyperclipException as e:
                logging.error(f"Error accessing clipboard: {e}")
                logging.error("Ensure you have the required dependencies installed (e.g., xclip/xsel on Linux).")
                break # Exit loop if clipboard access fails

            if clipboard_content != previous_clipboard_content:
                logging.debug("Clipboard content changed.")
                previous_clipboard_content = clipboard_content

                sensitive_data = detect_sensitive_data(clipboard_content)

                if sensitive_data:
                    logging.warning(f"Sensitive data detected in clipboard: {sensitive_data}")
                    print(f"Alert! Potential sensitive data found: {sensitive_data}")
                    # Implement more sophisticated reporting if needed.  For example:
                    # data = {"timestamp": [pd.Timestamp.now()], "data_type": [sensitive_data], "content": [clipboard_content[:100] + "..."]} # Trimmed content
                    # df = pd.DataFrame(data)
                    # df.to_csv("clipboard_log.csv", mode='a', header=False, index=False) #Append to a log file
                    

            time.sleep(1)  # Check every 1 second (adjust as needed)

    except KeyboardInterrupt:
        logging.info("Clipboard monitor stopped.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    main()