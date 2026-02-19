import asyncio
import edge_tts

async def list_voices():
    voices = await edge_tts.list_voices()
    
    print("="*70)
    print("AVAILABLE HINDI VOICES")
    print("="*70)
    
    hindi_voices = [v for v in voices if v['Locale'].startswith('hi-IN')]
    
    for voice in hindi_voices:
        print(f"\nName: {voice['ShortName']}")
        print(f"  Gender: {voice['Gender']}")
        print(f"  Locale: {voice['Locale']}")
        print(f"  Description: {voice.get('LocalName', 'N/A')}")

asyncio.run(list_voices())