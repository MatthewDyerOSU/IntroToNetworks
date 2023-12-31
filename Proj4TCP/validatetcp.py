PROTOCOL = b'\x06'
ZERO_BYTE = b'\x00'

def get_source_and_dest(textfile):
    '''
    Function that takes a textfile with source and destination IP addresses
    and returns the source and destination IPs separately.
    '''
    with open(textfile) as f:
        line = f.readline()
    line_array = line.split()
    source = line_array[0]
    dest = line_array[1]
    return source, dest

def ip_to_bytes(ip):
    '''
    Takes an IP address and converts it to a bytestring without the dots
    '''
    bytestring = b''
    int_array = ip.split(".")
    for i in int_array:
        bytestring += int(i).to_bytes()
    return bytestring

def get_length_and_checksum_and_data(datfile):
    '''
    Takes a .dat file and returns he length of the data, the checksum at
    offsets 16 and 17, as well as the data as a whole
    '''
    with open(datfile, 'rb') as f:
        data = f.readline()
    length = len(data)
    length = length.to_bytes(2, byteorder='big')
    checksum = int.from_bytes(data[16:18])
    return length, checksum, data

def generate_pseudo_header(source, dest, protocol, length) -> bytes:
    '''
    creates a header out of the source IP bytes, the destination IP bytes,
    two zero bytes, a protocol byte, and the length of the data represented
    as two bytes and returns said header in bytes
    '''
    header = b''.join((source, dest, ZERO_BYTE, protocol, length))
    return header

def generate_tcp_zero_chksm(data):
    '''
    takes TCP data and changes the checksum bytes at offset 16 and 17 to zeros
    '''
    tcp_zero_chksum = data[:16] + b'\x00\x00' + data[18:]
    # if number of bytes is odd, pad on the right with a zero byte to make even
    if len(tcp_zero_chksum) % 2 == 1:
        tcp_zero_chksum += b'\x00'
    return tcp_zero_chksum

def checksum(pseudo_header, tcp_zero_chksm):
    '''
    Concatenates the tcp header with the checksum set to zero bytes to the
    pseudo header, iterates over all the words (2 bytes) converting each to
    an int. Each word converted to an int is added to a total, then bitwise
    AND is performed, isolating the lower 16 bits of total, setting all higher
    bits to zero. A bitwise right shift operation is performed on total by 16
    positions, shifting the lower 16 bits out. The results of the bitwise and
    operation and the bitwise right shift are added together, effectively 
    adding the lower 16 bits (after masking) and the higher 16 bits 
    (after shifting) of the total value
    '''
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
    for i in range(10):
        # Read in the tcp_addrs_n.txt file
        # Split the line in two, the source and destination addresses
        source, dest = get_source_and_dest(f'tcp_addrs_{i}.txt')

        # Write a function that converts the dots-and-numbers
        # IP addresses into bytestrings
        source_bytes = ip_to_bytes(source)
        dest_bytes = ip_to_bytes(dest)

        # Read in the tcp_data_n.dat file
        # Extract the checksum from the original data in tcp_data_n.dat
        length, chksm_a, data = get_length_and_checksum_and_data(f'tcp_data_{i}.dat')

        # Function that generates the IP pseudo header bytes from the IP
        # addresses from tcp_addrs_n.txt and the TCP length from the tcp_data_n.dat file
        pseudo_header = generate_pseudo_header(source_bytes, dest_bytes, PROTOCOL, length)

        # Build a new version of the TCP data that has the checksum set to zero
        tcp_zero_chksum = generate_tcp_zero_chksm(data)

        # Concatenate the pseudo header and the TCP data with zero checksum
        # Compute the checksum of that concatenation
        chksm_b = checksum(pseudo_header, tcp_zero_chksum)

        # Compare the two checksums. If they're identical, it works!
        if chksm_a == chksm_b:
            print('PASS')
        else:
            print('FAIL')

if __name__ == '__main__':
    main()