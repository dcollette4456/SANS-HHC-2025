#!/usr/bin/env python3
"""
WebSocket Signal Capture Script
Captures extended signal data from the Holiday Hack Challenge
"""

import asyncio
import websockets
import json
from datetime import datetime

# Configuration
SIGNAL_DURATION = 90  # seconds
MAX_BITS = 10000  # capture up to 10k bits per wire

wires = ['dq', 'mosi', 'sck', 'sda', 'scl']
signal_data = {wire: [] for wire in wires}

async def capture_wire(wire_name):
    """Capture data from a single wire"""
    uri = f"wss://signals.holidayhackchallenge.com/wire/{wire_name}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"[{wire_name}] Connected!")
            
            # Capture for specified duration or max bits
            start_time = asyncio.get_event_loop().time()
            
            while len(signal_data[wire_name]) < MAX_BITS:
                try:
                    # Set timeout for individual messages
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    
                    # Parse the message
                    try:
                        data = json.loads(message)
                        if 'v' in data:
                            signal_data[wire_name].append(data['v'])
                    except json.JSONDecodeError:
                        # Message might just be a plain 0 or 1
                        if message in ('0', '1'):
                            signal_data[wire_name].append(int(message))
                    
                    # Check if we've been capturing long enough
                    if asyncio.get_event_loop().time() - start_time > SIGNAL_DURATION:
                        break
                        
                except asyncio.TimeoutError:
                    # Check if we should stop
                    if asyncio.get_event_loop().time() - start_time > SIGNAL_DURATION:
                        break
                    continue
                    
            print(f"[{wire_name}] Captured {len(signal_data[wire_name])} bits")
            
    except Exception as e:
        print(f"[{wire_name}] Error: {e}")

async def main():
    """Capture all wires simultaneously"""
    print(f"Starting capture of all 5 wires for {SIGNAL_DURATION} seconds...")
    print("This will capture the complete transmission loop!\n")
    
    # Create tasks for all wires
    tasks = [capture_wire(wire) for wire in wires]
    
    # Run all captures simultaneously
    await asyncio.gather(*tasks)
    
    # Save to JSON
    output_file = f"signals_extended_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(signal_data, f)
    
    print(f"\n✓ Capture complete!")
    print(f"✓ Saved to: {output_file}")
    print(f"\nCapture summary:")
    for wire, bits in signal_data.items():
        print(f"  {wire}: {len(bits)} bits")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nCapture interrupted by user")
        # Still save what we have
        output_file = f"signals_partial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(signal_data, f)
        print(f"Partial data saved to: {output_file}")
EOF
