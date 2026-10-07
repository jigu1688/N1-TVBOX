import struct
import sys
import os

SPARSE_HEADER_MAGIC = 0xed26ff3a
CHUNK_TYPE_RAW = 0xCAC1
CHUNK_TYPE_FILL = 0xCAC2
CHUNK_TYPE_DONT_CARE = 0xCAC3
CHUNK_TYPE_CRC32 = 0xCAC4

def img2simg(src_path, dst_path, blk_sz=4096):
    print(f"[*] Converting raw image {src_path} -> sparse image {dst_path}...")
    file_size = os.path.getsize(src_path)
    if file_size % blk_sz != 0:
        raise ValueError(f"File size {file_size} is not multiple of block size {blk_sz}")
        
    total_blks = file_size // blk_sz
    print(f"[+] Total blocks: {total_blks} ({file_size / 1024 / 1024:.2f} MB)")
    
    chunks = []
    
    with open(src_path, 'rb') as f:
        curr_type = None
        curr_count = 0
        curr_fill = None
        curr_raw_offset = 0
        
        for blk_idx in range(total_blks):
            block = f.read(blk_sz)
            
            # Check if block is all zeros
            is_zero = (block == b'\x00' * blk_sz)
            
            if is_zero:
                blk_type = CHUNK_TYPE_DONT_CARE
                fill_val = None
            else:
                blk_type = CHUNK_TYPE_RAW
                fill_val = None
                
            if curr_type is None:
                curr_type = blk_type
                curr_count = 1
                curr_fill = fill_val
                curr_raw_offset = blk_idx * blk_sz
            elif curr_type == blk_type and curr_count < 65535:
                curr_count += 1
            else:
                chunks.append((curr_type, curr_count, curr_raw_offset, curr_fill))
                curr_type = blk_type
                curr_count = 1
                curr_fill = fill_val
                curr_raw_offset = blk_idx * blk_sz
                
        if curr_count > 0:
            chunks.append((curr_type, curr_count, curr_raw_offset, curr_fill))
            
    total_chunks = len(chunks)
    print(f"[+] Processed {total_chunks} chunks.")
    
    with open(src_path, 'rb') as f_in, open(dst_path, 'wb') as f_out:
        # Write sparse header
        # struct: magic, maj_v, min_v, file_hdr_sz, chunk_hdr_sz, blk_sz, total_blks, total_chunks, crc
        file_hdr = struct.pack('<I4H4I', SPARSE_HEADER_MAGIC, 1, 0, 28, 12, blk_sz, total_blks, total_chunks, 0)
        f_out.write(file_hdr)
        
        for chunk_type, chunk_sz, raw_off, fill_val in chunks:
            if chunk_type == CHUNK_TYPE_DONT_CARE:
                total_sz = 12
                chunk_hdr = struct.pack('<2H2I', chunk_type, 0, chunk_sz, total_sz)
                f_out.write(chunk_hdr)
            elif chunk_type == CHUNK_TYPE_RAW:
                total_sz = 12 + chunk_sz * blk_sz
                chunk_hdr = struct.pack('<2H2I', chunk_type, 0, chunk_sz, total_sz)
                f_out.write(chunk_hdr)
                f_in.seek(raw_off)
                # Stream raw data in chunks
                bytes_to_copy = chunk_sz * blk_sz
                while bytes_to_copy > 0:
                    read_len = min(bytes_to_copy, 1024 * 1024)
                    buf = f_in.read(read_len)
                    f_out.write(buf)
                    bytes_to_copy -= len(buf)
                    
    sparse_size = os.path.getsize(dst_path)
    print(f"[+] Successfully generated sparse image ({sparse_size / 1024 / 1024:.2f} MB, compression: {sparse_size / file_size * 100:.1f}%)")

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'build_rom/system.raw.img'
    dst = sys.argv[2] if len(sys.argv) > 2 else 'build_rom/system.PARTITION'
    img2simg(src, dst)
