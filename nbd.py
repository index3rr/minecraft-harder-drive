import socket
import minescript
import time
import math
import os
import sys
print("Running Python", sys.version)
print("Site-packages:", sys.path)
#I APOLOGIZE: THIS CODE SUCKS HOT ASS
#DO NOT TOUCH IT WITH A 15 FEET POLE


#extra_paths = ['/usr/lib/python313.zip', '/usr/lib/python3.13', '/usr/local/lib/python3.13/site-packages', '/usr/lib/python3.13/site-packages', '/home/luna/.local/lib/python3.13/site-packages', '/usr/local/lib64/python3.13/site-packages']

#for path in extra_paths:
#	if path not in sys.path:te
#		sys.path.insert(0, path)

import mcschematic

CHUNK_WIDTH = 16
CHUNK_HEIGHT = 16
CHUNK_LENGTH = 8
BYTES_PER_CHUNK = CHUNK_WIDTH * CHUNK_HEIGHT * CHUNK_LENGTH

hexBlocks = ["white_wool", "orange_wool", "magenta_wool", "light_blue_wool", "yellow_wool", "lime_wool", "pink_wool", "gray_wool", "light_gray_wool", "cyan_wool", "purple_wool", "blue_wool", "brown_wool", "green_wool", "red_wool", "black_wool"]
minecraft_hexBlocks = []
for block in hexBlocks:
    minecraft_hexBlocks.append(f"minecraft:{block}") #hacky fix to match for "minecraft:white_wool" as well as the normal string

chunkDict = { #this basically says the origin point for each chunk, read initChunk for more details, it can be hardcoded, what im doing here, and what should probably be done as initchunk wont work properly once its run once, also everything is set up to read chunks on z+ line :p this is really bad fucking code
    (0,0): [0, -46, 0],
    (0,1): [0, -46, 16],
    (0,2): [0, -46, 32],
    (0,3): [0, -46, 48],
    (0,4): [0, -46, 64],
    (0,5): [0, -46, 80],
    (0,6): [0, -46, 96],
    (0,7): [0, -46, 112],
    (0,8): [0, -46, 128],
    (0,9): [0, -46, 144],
    (0,10): [0, -46, 160],
    (0,11): [0, -46, 176],
    (0,12): [0, -46, 192],
    (0,13): [0, -46, 208],
    (0,14): [0, -46, 224],
    (0,15): [0, -46, 240],
    (0,16): [0, -46, 256],
    (0,17): [0, -46, 272],
    (0,18): [0, -46, 288],
    (0,19): [0, -46, 304],
    (0,20): [0, -46, 320],
    (0,21): [0, -46, 336],
    (0,22): [0, -46, 352],
    (0,23): [0, -46, 368],
    (0,24): [0, -46, 384],
    (0,25): [0, -46, 400],
}

def initChunk(x, z):
    targetchunk = (x, z)
    if not targetchunk in chunkDict: #skip if already init'd
        #essentially, go to the chunk with baritone, and then get the player position so we have an origin point for the chunk thats not inside the ground, or in the air.
        targetpos = [targetchunk[0]*16, targetchunk[1]*16]
        minescript.chat(f"#goto {targetpos[0]} {targetpos[1]}")
        while [math.floor(minescript.player_position()[0]), math.floor(minescript.player_position()[2])] != [targetpos[0], targetpos[1]]:
            time.sleep(0.1)
        startpos = minescript.player_position()
        startpos = [math.floor(startpos[0]), math.floor(startpos[1]), math.floor(startpos[2])]
        chunkDict[targetchunk] = startpos
        #also, clear it.
        clearChunk(*targetchunk)

def clearChunk(x, z, depth = 16):
    targetchunk = (x, z)
    #select the chunk
    minescript.chat(f"#sel 1 {chunkDict[targetchunk][0]} {chunkDict[targetchunk][1] + 7} {chunkDict[targetchunk][2]}")
    minescript.chat(f"#sel 2 {chunkDict[targetchunk][0] + 15} {chunkDict[targetchunk][1] + 8 - (depth)} {chunkDict[targetchunk][2]+15}")
    #set the layer order to true so we can clear the chunk from top to bottom
    minescript.chat("#layerOrder true")
    #This var is set at the end to disallow breaking wool, which is important for building
    #but obviously, we need to break wool sometimes using clearchunk.
    minescript.chat("#blocksToDisallowBreaking air")
    with minescript.EventQueue() as event_queue:
        baritone_working = True
        event_queue.register_chat_listener()
        time.sleep(1)
        minescript.chat("#sel cleararea")
        #loop until baritone is done
        while baritone_working:
            event = event_queue.get()
            if event.type == minescript.EventType.CHAT:
                if event.message.startswith("[Baritone] Done building"):
                    #fun fact, this can be triggered by using tellraw! not really all that great of a system :p
                    baritone_working = False
    #clear selection, revert layer order for building, and disallow breaking wool again.
    minescript.chat("#layerOrder false")
    minescript.chat("#sel clear")
    minescript.chat("#blocksToDisallowBreaking red_wool,lime_wool,pink_wool,gray_wool,cyan_wool,blue_wool,white_wool,brown_wool,green_wool,orange_wool,yellow_wool,magenta_wool,light_blue_wool,light_gray_wool,purple_wool,black_wool")

def writeChunk(x, z, data, offset=0, fast=False):
    chunk = (x, z)
    minescript.echo("Writing chunk...")
    new = False
    if chunk not in chunkDict:
        initChunk(*chunk)
        new = True
    


    if all(val == 0 for val in data):
        return
    #fast mode for doing this on a local world, turn off for using baritone obv, just runs setblock a whole bunch
    if fast:
        base_x, base_y, base_z = chunkDict[chunk]
        base_y = base_y - 8
        idx = 0
        for layer in range(0, 16):
            for j in range(0, 16):
                for k in range(0, 8):
                    if idx - offset >= len(data):
                        return
                        
                    if idx >= offset:
                        byte = data[idx - offset]
                        if byte == 0 and all(b == 0 for b in data[idx - offset + 1:]):
                            return
                            
                        block_x = base_x + j
                        block_z = base_z + (k * 2)
                        
                        lower_nibble = byte & 0x0F
                        minescript.execute(f"setblock {block_x} {base_y + layer} {block_z} {hexBlocks[lower_nibble]}")
                        
                        upper_nibble = (byte >> 4) & 0x0F
                        minescript.execute(f"setblock {block_x} {base_y + layer} {block_z + 1} {hexBlocks[upper_nibble]}")
                        
                    idx += 1
        return
    
    if not new:
        old_schem, _ = ReadChunk(*chunk)
    else:
        old_schem = None
        minescript.echo("New chunk, no old schem passed")
    
    layers = createSchematic(data, old_schem, offset)


    clearChunk(*chunk, 16 - layers)


    minescript.chat(f"#build my_cool_schematic.schem {chunkDict[chunk][0]} {chunkDict[chunk][1] - 8} {chunkDict[chunk][2]}")
    with minescript.EventQueue() as event_queue:
        baritone_working = True
        event_queue.register_chat_listener()
        time.sleep(1)
        minescript.chat("#sel cleararea")
        
        while baritone_working:
            event = event_queue.get()
            if event.type == minescript.EventType.CHAT:
                if event.message.startswith("[Baritone] Done building"):
                    baritone_working = False


def all_zeros_remaining(data, start_index):
    return all(b == 0 for b in data[start_index:])

def createSchematic(new_data, old_schematic=None, offset=0):
    if old_schematic is not None:
        schem = old_schematic
    else:
        schem = mcschematic.MCSchematic()
    lowest = 16
    idx = 0
    
    if all(b == 0 for b in new_data):
        return lowest
        
    for layer in range(0, 16):
        minescript.echo(f"Layer {layer}, lowest: {lowest}")
        for j in range(0, 16):
            for k in range(0, 8):
                if idx - offset >= len(new_data):
                    # all data done, save and return
                    schem.save("schematics", "my_cool_schematic", mcschematic.Version.JE_1_21_5)
                    return lowest
                    
                if idx >= offset:
                    byte = new_data[idx - offset]
                    if byte == 0 and all(b == 0 for b in new_data[idx - offset + 1:]):
                        minescript.echo("Remaining data is all zeros, saving schematic early")
                        schem.save("schematics", "my_cool_schematic", mcschematic.Version.JE_1_21_5)
                        return lowest
                    lower_nibble = byte & 0x0F
                    upper_nibble = (byte >> 4) & 0x0F

                    schem.setBlock((j, layer, k*2), hexBlocks[lower_nibble])
                    schem.setBlock((j, layer, k*2+1), hexBlocks[upper_nibble])
                    if lowest > layer:
                        lowest = layer

                elif idx - offset < len(new_data) and schem.getBlockStateAt((j, layer, k*2)) == "minecraft:air":
                    schem.setBlock((j, layer, k*2), "minecraft:white_wool")
                    schem.setBlock((j, layer, k*2+1), "minecraft:white_wool")
                
                idx += 1
    
    schem.save("schematics", "my_cool_schematic", mcschematic.Version.JE_1_21_5)
    return lowest
    
        
def ReadChunk(x, z):
    chunk = (x, z)
    initChunk(*chunk)
    start_pos = chunkDict[chunk]
    schem = mcschematic.MCSchematic()
    array = []
    
    positions = []
    for layer in range(16):
        array.append([])
        for j in range(16):
            array[layer].append([None] * 16)
            for k in range(16):
                positions.append([
                    start_pos[0] + j,
                    start_pos[1] - 8 + layer,
                    start_pos[2] + k
                ])
    
    blocks = minescript.getblocklist(positions)
    
    idx = 0
    for layer in range(16):
        for j in range(16):
            for k in range(16):
                block = blocks[idx]
                idx += 1
                schem.setBlock((j, layer, k), block)
                array[layer][j][k] = block
    
    return schem, array
                
def ChunkBytes(x, z):
    chunk = (x, z)
    schem, array = ReadChunk(*chunk)
    result = bytearray()
    
    for layer in range(16):
        for j in range(16):
            for k in range(0, 8):
                try:
                    lower_block = array[layer][j][k*2]
                    upper_block = array[layer][j][k*2+1]
                    
                    try:
                        lower_nibble = minecraft_hexBlocks.index(lower_block)
                        upper_nibble = minecraft_hexBlocks.index(upper_block)
                        
                        byte = (upper_nibble << 4) | lower_nibble
                        result.append(byte)
                        
                    except ValueError:
                        result.append(0)
                    
                except IndexError:
                    if len(result) < BYTES_PER_CHUNK:
                        result += b'\x00' * (BYTES_PER_CHUNK - len(result))

                    return bytes(result)
                except Exception as e:
                    minescript.echo(f"Unexpected error: {e}")
                    raise
    

    return bytes(result)

def Write(offset, data):

        
    total_written = 0
    remaining_data = bytearray(data)
    current_offset = offset
    
    while remaining_data:
        chunk_x = 0
        chunk_z = current_offset // BYTES_PER_CHUNK
        pos_in_chunk = current_offset % BYTES_PER_CHUNK
        bytes_available_in_chunk = BYTES_PER_CHUNK - pos_in_chunk
        bytes_to_write = min(len(remaining_data), bytes_available_in_chunk)
        
        chunk_data = remaining_data[:bytes_to_write]
        
        writeChunk(chunk_x, chunk_z, chunk_data, pos_in_chunk)
        
        total_written += bytes_to_write
        current_offset += bytes_to_write
        remaining_data = remaining_data[bytes_to_write:]
    
    return total_written


def Read(offset, amount):
    result = bytearray()
    remaining = amount
    current_offset = offset
    

    while remaining > 0:
        chunk_x = 0
        chunk_z = current_offset // BYTES_PER_CHUNK
        pos_in_chunk = current_offset % BYTES_PER_CHUNK
        
        bytes_available_in_chunk = BYTES_PER_CHUNK - pos_in_chunk
        bytes_to_read = min(remaining, bytes_available_in_chunk)
        

        chunk_data = ChunkBytes(chunk_x, chunk_z)
        if len(chunk_data) < BYTES_PER_CHUNK:
            pass
            
        start_pos = pos_in_chunk
        end_pos = start_pos + bytes_to_read
        result.extend(chunk_data[start_pos:end_pos])
        
        remaining -= bytes_to_read
        current_offset += bytes_to_read
    

    return result

minescript.echo("Connecting to NBD...")

def handle_nbd_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 65300))
    minescript.echo("Connected to NBD!")
    
    hello = sock.recv(1024)
    minescript.echo(f"Server says: {hello.decode()}")
    sock.send(b"ACK")
    
    try:
        while True:

            data = sock.recv(1024)
            if not data:
                minescript.echo("Connection closed by server")
                break
                
            decoded = data.decode().strip()
            minescript.echo(f"Received command: {decoded}")
            
            if decoded == "SIZE":
                sock.send(b"ACK")
                sock.send(b"51200")
                
            elif decoded.startswith("RD"):
                try:
                    _, offset_str, length_str = decoded.split()
                    offset = int(offset_str)
                    length = int(length_str)
                    minescript.echo(f"Reading {length} bytes at offset {offset}")
                    
                    sock.send(b"ACK")
                    
                    data = Read(offset, length)
                    minescript.echo(f"Sending Data... {len(data)} bytes")
                    sock.send(data)
                    
                except Exception as e:
                    minescript.echo(f"Error handling RD: {e}")
                    
            elif decoded.startswith("WR"):
                try:
                    _, offset_str, length_str = decoded.split()
                    offset = int(offset_str)
                    length = int(length_str)
                    
                    sock.send(b"ACK")
                    
                    data = bytearray()
                    chunk = sock.recv(length)
                    if not chunk:
                        raise Exception("Connection closed during data transfer")
                    data.extend(chunk)
                    
                    Write(offset, data)
                    sock.send(b"END")
                    
                except Exception as e:
                    minescript.echo(f"Error handling WR: {e}")
                
    except Exception as e:
        minescript.echo(f"Error in NBD connection: {e}")
    finally:
        sock.close()
        minescript.echo("NBD connection closed")

handle_nbd_connection()