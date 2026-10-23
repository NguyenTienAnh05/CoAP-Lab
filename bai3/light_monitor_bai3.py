import asyncio
import json
import datetime
import aiocoap

async def main():
    context = await aiocoap.Context.create_client_context()
    print("Registering CoAP Observe...")
    
    
    request = aiocoap.Message(code=aiocoap.GET, uri="coap://127.0.0.1/iot/lab/light01/status", observe=0)
    
    try:
        pr = context.request(request)
        async for response in pr.observation:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                data = json.loads(response.payload.decode('utf-8'))
                device_id = data.get("device_id")
                status = data.get("status")
                
                print(f"\n[{current_time}] State Update Received")
                print(f"Device: {device_id}")
                print(f"Status: {status}\n")
            except Exception:
                print(f"\n[{current_time}] Payload: {response.payload.decode('utf-8')}\n")
                
    except Exception as e:
        print(f"Observation failed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Monitoring Client...")