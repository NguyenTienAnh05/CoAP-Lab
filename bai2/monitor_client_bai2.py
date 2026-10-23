import asyncio
import json
import datetime
import aiocoap

async def main():
    context = await aiocoap.Context.create_client_context()
    print("Monitoring CoAP Client started. Press Ctrl+C to stop.\n")
    
    try:
        while True:
            # Thêm cổng :5683 vào URI để tránh lỗi NetworkError
            request = aiocoap.Message(code=aiocoap.GET, uri="coap://127.0.0.1:5683/iot/lab/sensor01/data")
            try:
                response = await context.request(request).response
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"[{current_time}] Received sensor data")
                
                data = json.loads(response.payload.decode('utf-8'))
                device_id = data.get("device_id")
                temp = data.get("temperature")
                humidity = data.get("humidity")
                
                print(f"\nDevice: {device_id}")
                print(f"Temperature: {temp} C")
                print(f"Humidity: {humidity} %")
                
                has_warning = False
                if temp > 35:
                    print("CANH BAO: Nhiet do cao")
                    has_warning = True
                if humidity < 40:
                    print("CANH BAO: Do am thap")
                    has_warning = True
                    
                if not has_warning:
                    print("Trang thai: Binh thuong")
                    
                print("-" * 30)
            except Exception as e:
                print(f"Error fetching data: {e}")
                
            await asyncio.sleep(3)
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Monitoring Client...")