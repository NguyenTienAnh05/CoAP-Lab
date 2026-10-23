import asyncio
import json
import logging
import aiocoap
import aiocoap.resource as resource

class SmartLightResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.state = "OFF"  

    def get_payload(self):
        data = {
            "device_id": "light01",
            "status": self.state
        }
        return json.dumps(data).encode('utf-8')

    async def render_get(self, request):
        print("\nGET request received")
        return aiocoap.Message(code=aiocoap.CONTENT, payload=self.get_payload())

    async def render_put(self, request):
        print("\nPUT request received:")
        try:
            data = json.loads(request.payload.decode('utf-8'))
            device_id = data.get("device_id")
            command = data.get("command")
            
            print(f"Device: {device_id}")
            print(f"Command: {command}")
            
            if command in ["ON", "OFF"]:
                if self.state != command:
                    old_state = self.state
                    self.state = command
                    print(f"Light state changed: {old_state} -> {self.state}")
                    print(f"Notify observers: {self.state}")
                
                    self.updated_state()
                    
                return aiocoap.Message(code=aiocoap.CHANGED, payload=b"Server da cap nhat trang thai den")
            else:
                return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload=b"Invalid command")
        except Exception as e:
            print(f"Error: {e}")
            return aiocoap.Message(code=aiocoap.BAD_REQUEST, payload=str(e).encode('utf-8'))

async def main():
    root = resource.Site()
    light_res = SmartLightResource()
    root.add_resource(['iot', 'lab', 'light01', 'status'], light_res)
    
    await aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683))
    print("CoAP Smart Light Server started...")
    print("Resource: /iot/lab/light01/status")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer Shutdown")