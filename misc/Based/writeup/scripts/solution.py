base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def decode_to_bits(base64_text):
    binary = ''
    for char in base64_text:
        if char in base64_alphabet:
            index = base64_alphabet.index(char)
            binary += format(index, '06b')
    return binary

with open('Top_secret', 'r') as file:
    base64_lines = file.readlines()

decoded_data = ''
hidden_data = ''

for line in base64_lines:
    bits = decode_to_bits(line)
    full_bytes_length = (len(bits) // 8) * 8
    visible = bits[:full_bytes_length]
    hidden = bits[full_bytes_length:]   
    decoded_data += visible
    hidden_data += hidden

plain_text = bytes(int(decoded_data[i:i+8], 2) for i in range(0, len(decoded_data), 8))
print("Base64 message:", plain_text)

hidden_text = bytes(int(hidden_data[i:i+8], 2) for i in range(0, len(hidden_data), 8))
print("Hidden flag:", hidden_text)
