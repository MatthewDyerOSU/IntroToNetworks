




def main():
    # Read in the tcp_addrs_0.txt file

    # Split the line in two, the source and destination addresses

    # Write a function that converts the dots-and-numbers
    # IP addresses into bytestrings

    # Read in the tcp_data_0.dat file

    # Write a function that generates the IP pseudo header bytes from the IP
    # addresses from tcp_addrs_0.txt and the TCP length from the tcp_data_0.dat file

    # Build a new version of the TCP data that has the checksum set to zero

    # Concatenate the pseudo header and the TCP data with zero checksum

    # Compute the checksum of that concatenation

    # Extract the checksum from the original data in tcp_data_0.dat

    # Compare the two checksums. If they're identical, it works!

    # Modify your code to run it on all 10 of the data files. The first 5 files
    # should have matching checksums! The second five files should not! That is,
    # the second five files are simulating being corrupted in transit
    pass

if __name__ == '__main__':
    main()