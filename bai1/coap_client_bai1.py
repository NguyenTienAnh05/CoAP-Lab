import asyncio
import aiocoap

async def main():
    
    msv = input("Nhập Mã sinh viên: ").strip()
    ho_ten = input("Nhập Họ và tên: ").strip()
    

    context = await aiocoap.Context.create_client_context()
    
    print("CoAP Client")
    print("Sending GET request...")
    print("URI: coap://localhost:5683/iot/lab/message\n")
    
    
    request = aiocoap.Message(code=aiocoap.GET, uri="coap://127.0.0.1/iot/lab/message")
    try:
        response = await context.request(request).response
        print("Response:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8')}\n")
    except Exception as e:
        print(f"Failed to fetch GET: {e}")

    
    payload_msg = f"Xin chao tu CoAP Client - {msv} - {ho_ten}"
    print("Sending POST request...")
    print(f"Payload: {payload_msg}\n")
    
    request = aiocoap.Message(code=aiocoap.POST, uri="coap://127.0.0.1/iot/lab/message", payload=payload_msg.encode('utf-8'))
    try:
        response = await context.request(request).response
        print("Response:")
        print(f"Code: {response.code}")
        print(f"Payload: {response.payload.decode('utf-8')}")
    except Exception as e:
        print(f"Failed to send POST: {e}")

if __name__ == "__main__":
    asyncio.run(main())