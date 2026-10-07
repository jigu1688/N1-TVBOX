import struct
import sys
import os

SPARSE_HEADER_MAGIC = 0xed26ff3a
CHUNK_TYPE_RAW = 0xCAC1
CHUNK_TYPE_FILL = 0xCAC2
CHUNK_TYPE_DONT_CARE = 0xCAC3
CHUNK_TYPE_CRC32 = 0xCAC4

def simg2img(src_path, dst_path):
    print(f"[*] Converting sparse image {src_path} -> {dst_path}...")
    with open(src_path, 'rb') as f_in, open(dst_path, 'wb') as f_out:
        header_data = f_in.read(28)
        if len(header_data) < 28:
            raise ValueError("File too small")
            
        magic, maj, min_v, file_hdr_sz, chunk_hdr_sz, blk_sz, total_blks, total_chunks, crc = struct.unpack('<I4H4I', header_data)
        if magic != SPARSE_HEADER_MAGIC:
            raise ValueError("Not a sparse image")
            
        print(f"[+] Sparse Header: blk_sz={blk_sz}, total_blks={total_blks} ({total_blks*blk_sz/1024/1024:.2f} MB), total_chunks={total_chunks}")
        
        # Skip remaining file header if any
        if file_hdr_sz > 28:
            f_in.seek(file_hdr_sz - 28, os.SEEK_CUR)
            
        total_out_bytes = 0
        for i in range(total_chunks):
            chunk_hdr = f_in.read(chunk_hdr_sz)
            if len(chunk_hdr) < 12:
                break
            chunk_type, _, chunk_sz, total_sz = struct.unpack('<2H2I', chunk_hdr[:12])
            data_sz = chunk_sz * blk_sz
            
            if chunk_type == CHUNK_TYPE_RAW:
                raw_data = f_in.read(data_sz)
                f_out.write(raw_data)
                total_out_bytes += data_sz
            elif chunk_type == CHUNK_TYPE_FILL:
                fill_val = f_in.read(4)
                fill_block = fill_val * (blk_sz // 4)
                for _ in range(chunk_sz):
                    f_out.write(fill_block)
                total_out_bytes += data_sz
            elif chunk_type == CHUNK_TYPE_DONT_CARE:
                f_out.seek(data_sz, os.SEEK_CUR)
                # To ensure file size is correct on disk, write zeros or seek
                # Seeking on empty file will create sparse hole, which is fine
                total_out_bytes += data_sz
            elif chunk_type == CHUNK_TYPE_CRC32:
                f_in.read(4)
            else:
                raise ValueError(f"Unknown chunk type: {hex(chunk_type)} at chunk {i}")
                
        # Ensure final output file size matches
        if f_out.tell() < total_blks * blk_sz:
            f_out.truncate(total_blks * blk_sz)
            
    print(f"[+] Successfully converted to raw image ({total_out_bytes / 1024 / 1024:.2f} MB)!")

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'extracted_aml/system.PARTITION'
    dst = sys.argv[2] if len(sys.argv) > 2 else 'extracted_aml/system.raw.img'
    simg2img(src, dst)
