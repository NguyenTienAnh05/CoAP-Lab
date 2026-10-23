import asyncio
import json
import random
import logging
import aiocoap
import aiocoap.resource as resource

class SensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.temperature = 28.5
        self.humidity = 65.2
        asyncio.create_task(self.update_sensor_periodically())

    async def update_sensor_periodically(self):
        while True:
            await asyncio.sleep(3)
            
            self.temperature = round(random.uniform(20.0, 40.0), 1)
            self.humidity = round(random.uniform(30.0, 90.0), 1)

    async def render_get(self, request):
        data = {
            "device_id": "sensor01",
            "temperature": self.temperature,
            "humidity": self.humidity
        }
        payload = json.dumps(data).encode('utf-8')
        return aiocoap.Message(code=aiocoap.CONTENT, payload=payload, content_format=50)

async def main():
    root = resource.Site()
    root.add_resource(['iot', 'lab', 'sensor01', 'data'], SensorResource())
    
    await aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683))
    print("Sensor CoAP Server started on port 5683...")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer Shutdown")
