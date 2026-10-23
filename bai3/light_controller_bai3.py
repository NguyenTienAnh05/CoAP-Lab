import asyncio
import json
import aiocoap

async def main():
    context = await aiocoap.Context.create_client_context()
    
    while True:
        choice = await asyncio.get_running_loop().run_in_executor(
            None, input, "Nhap lenh: "
        )
        choice = choice.strip().upper()
        
        if choice == "EXIT":
            print("Exiting controller...")
            break
            
        elif choice in ["ON", "OFF"]:
            print("\nSending PUT request...")
            payload_data = {
                "device_id": "light01",
                "command": choice
            }
            request = aiocoap.Message(
                code=aiocoap.PUT,
                uri="coap://127.0.0.1/iot/lab/light01/status",
                payload=json.dumps(payload_data).encode('utf-8')
            )
            try:
                response = await context.request(request).response
                print(f"Response Code: {response.code}")
                if choice == "ON":
                    print("Da bat den light01\n")
                else:
                    print("Da tat den light01\n")
            except Exception as e:
                print(f"Failed PUT: {e}\n")
                
        elif choice == "STATUS":
            print("\nSending GET request...")
            request = aiocoap.Message(
                code=aiocoap.GET,
                uri="coap://127.0.0.1/iot/lab/light01/status"
            )
            try:
                response = await context.request(request).response
                print("Response:")
                print(f"{response.payload.decode('utf-8')}\n")
            except Exception as e:
                print(f"Failed GET: {e}\n")
        else:
            print("Lenh khong hop le.\n")

if __name__ == "__main__":
    asyncio.run(main())