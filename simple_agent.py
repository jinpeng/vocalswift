import os
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    azure,
    openai,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    azure_stt = azure.STT(
        speech_key=os.getenv("AZURE_SPEECH_KEY"),
        speech_region=os.getenv("AZURE_SPEECH_REGION")
    )

    azure_llm = openai.LLM.with_azure(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION")
    )

    azure_tts = azure.TTS(
        speech_key=os.getenv("AZURE_SPEECH_KEY"),
        speech_region=os.getenv("AZURE_SPEECH_REGION"),
    )

    session = AgentSession(
        stt=azure_stt,
        llm=azure_llm,
        tts=azure_tts,
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
