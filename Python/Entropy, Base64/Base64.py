#files = ["1.txt","2.txt","3.txt"]
files = ["1.tar.bz2", "2.tar.bz2", "3.tar.bz2"]
for file in files:
    f = open(file,'rb')
    file_bytes = f.read()
    f.close()
    Base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    Encoded_file = ""
    end_bytes = len(file_bytes) % 3
    
    for i in range(0, len(file_bytes)-end_bytes, 3):
        Base64_buffer = ""
        for k in range(3):
            bin_data = str(bin(file_bytes[i+k]))[2:]
            bin_data = (8-len(bin_data))*'0' + bin_data
            Base64_buffer += bin_data
        for j in range(0,24,6):
            Buffer_part = Base64_buffer[j:j+6]
            Base64_index = int(Buffer_part, base=2)
            Encoded_file += Base64_alphabet[Base64_index]
            
    if end_bytes != 0:
        Base64_buffer = ""
        for k in range(-end_bytes,0):
            bin_data = str(bin(file_bytes[k]))[2:]
            bin_data = (8-len(bin_data))*'0' + bin_data
            Base64_buffer += bin_data
        Base64_buffer += (6-len(Base64_buffer) % 6) * '0'
        
        for j in range(0, 6*end_bytes + 1, 6):
            Buffer_part = Base64_buffer[j:j+6]
            Base64_index = int(Buffer_part, base=2)
            Encoded_file += Base64_alphabet[Base64_index]
        Encoded_file += (3-end_bytes)*"="
    f2 = open(f"{file}-Base64.txt",'w', encoding="utf-8")
    f2.write(Encoded_file)
    f2.close()