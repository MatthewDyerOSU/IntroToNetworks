PROTOCOL = b'\x06'
ZERO_BYTE = b'\x00'

def get_source_and_dest(textfile):
    with open(textfile) as f:
        line = f.readline()
    # print(line)
    line_array = line.split()
    source = line_array[0]
    dest = line_array[1]
    # print(f'source: {source}, dest: {dest}')
    return source, dest

def ip_to_bytes(ip):
    bytestring = b''
    int_array = ip.split(".")
    for i in int_array:
        bytestring += int(i).to_bytes()
    return bytestring

def get_length_and_checksum_and_data(datfile):
    with open(datfile, 'rb') as f:
        line = f.readline()
    # print(line)
    length = len(line)
    length = length.to_bytes()
    checksum = int.from_bytes(line[16:18])
    # print(f'Length: {length}')
    # print(f'Checksum: {checksum}')
    return length, checksum, line

def generate_pseudo_header(source, dest, protocol, length):
    header = b''.join((source, dest, ZERO_BYTE, protocol, length))
    # hex_header = header.hex()
    # print(hex_header)
    return header

def generate_tcp_zero_chksm(data):
    tcp_zero_chksum = data[:16] + b'\x00\x00' + data[18:]
    # if number of bytes is odd, pad on the right with a zero byte to make even
    if len(tcp_zero_chksum) % 2 == 1:
        tcp_zero_chksum += b'\x00'
    # print(tcp_zero_chksum)
    return tcp_zero_chksum

def checksum(pseudo_header, tcp_zero_chksm):
    data = pseudo_header + tcp_zero_chksm
    offset = 0
    total = 0
    while offset < len(data):
        word = int.from_bytes(data[offset:offset+2], "big")
        total += word
        offset += 2
        total = (total & 0xffff) + (total >> 16)
    return (~total) & 0xffff
    

def main():
    # Read in the tcp_addrs_n.txt file
    # Split the line in two, the source and destination addresses
    source, dest = get_source_and_dest('tcp_addrs_0.txt')

    # Write a function that converts the dots-and-numbers
    # IP addresses into bytestrings
    source_bytes = ip_to_bytes(source)
    # print(source_bytes)
    dest_bytes = ip_to_bytes(dest)
    # print(dest_bytes)

    # Read in the tcp_data_0.dat file
    length, chksm_a, data = get_length_and_checksum_and_data('tcp_data_0.dat')

    # Function that generates the IP pseudo header bytes from the IP
    # addresses from tcp_addrs_n.txt and the TCP length from the tcp_data_n.dat file
    pseudo_header = generate_pseudo_header(source_bytes, dest_bytes, PROTOCOL, length)

    # Build a new version of the TCP data that has the checksum set to zero
    tcp_zero_chksum = generate_tcp_zero_chksm(data)

    # Concatenate the pseudo header and the TCP data with zero checksum
    # Compute the checksum of that concatenation
    chksm_b = checksum(pseudo_header, tcp_zero_chksum)

    # Extract the checksum from the original data in tcp_data_0.dat

    # Compare the two checksums. If they're identical, it works!
    print(chksm_a)
    print(chksm_b)

    # Modify your code to run it on all 10 of the data files. The first 5 files
    # should have matching checksums! The second five files should not! That is,
    # the second five files are simulating being corrupted in transit

if __name__ == '__main__':
    main()