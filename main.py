import os
from dotenv import load_dotenv
from openai import AzureOpenAI


def main():
    api_version = os.getenv("OPENAI_API_VERSION")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    # gets the API Key from environment variable AZURE_OPENAI_API_KEY
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=azure_endpoint,
    )

    completion = client.chat.completions.create(
        model=azure_deployment,  # e.g. gpt-35-instant
        messages=[
            {
                "role": "user",
                "content": "How do I output all files in a directory using Python?",
            },
        ],
    )
    print(completion.to_json())



if __name__ == "__main__":
    # load env variables
    load_dotenv()
    print(os.getenv("AZURE_OPENAI_API_KEY"))
    main()

