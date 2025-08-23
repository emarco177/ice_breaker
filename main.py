from dotenv import load_dotenv

load_dotenv()


def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    return len(text)


if __name__ == "__main__":
    print("Hello ReAct LangChain!")
    tools = [get_text_length]
