import asyncio
import datetime
import logging
import aiocoap
import aiocoap.resource as resource

class MessageResource(resource.Resource):
    async def render_get(self, request):
        print("\nGET request received: /iot/lab/message")
        payload = b"Xin chao tu CoAP Server"
        return aiocoap.Message(payload=payload)

    async def render_post(self, request):
        print("\nPOST request received:")
        payload_str = request.payload.decode('utf-8')
        print(f"Payload: {payload_str}")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Time: {current_time}")
        
        response_payload = b"Server da nhan thong diep"
        return aiocoap.Message(code=aiocoap.CHANGED, payload=response_payload)

async def main():
    root = resource.Site()
    root.add_resource(['iot', 'lab', 'message'], MessageResource())
    
    await aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683))
    print("CoAP Server started on port 5683")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer Shutdown")