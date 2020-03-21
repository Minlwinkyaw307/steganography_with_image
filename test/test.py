import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv


def reverseBits(num, bitSize):
    binary = bin(num)
    reverse = binary[-1:1:-1]
    reverse = reverse + (bitSize - len(reverse)) * '0'
    return int(reverse, 2)


def encrypt_bits(origin, reverse):
    # ENCRYPTING
    origin = np.uint8(origin)
    reverse = np.uint8(reverse)
    reverse_4bits = np.uint8(reverse & 0xF0)
    xor_origin_rev_4b = (origin ^ reverse_4bits) & 0xF0
    encrypt = xor_origin_rev_4b | np.uint8(reverse & 0x0F)

    return encrypt


def decrypt_bits(encrypt):
    # DECRYPTING
    encrypt = np.uint8(encrypt)
    first_origin_4bit = np.uint8(reverseBits(encrypt & 0x0F, 4) << 4)

    xor_encrypt_f4b = (encrypt ^ (first_origin_4bit)) & 0xF0
    xor_encrypt_f4b_rev = reverseBits(xor_encrypt_f4b, 8)
    decrypt = np.uint8(xor_encrypt_f4b_rev) | np.uint8(first_origin_4bit)

    return decrypt


def decrypt_image(encrypted_image):
    # DECRYPTING
    encrypted_image = np.uint8(encrypted_image)
    first_origin_4bit = np.packbits(np.unpackbits((encrypted_image & 0x0F).flatten()),
                                    bitorder='little').reshape(encrypted_image.shape)
    xor_encrypt_f4b_rev = np.packbits(np.unpackbits(((encrypted_image ^ first_origin_4bit) & 0xF0).flatten()),
                                      bitorder='little').reshape(encrypted_image.shape)
    return np.uint8(xor_encrypt_f4b_rev | first_origin_4bit)

# encrypt = []
# decrypt = []
#
# for i in range(0, 255):
#     print(f"Origin\t\t{i}")
#     encrypt.append(encrypt_bits(i))
#     print(f"Encrypt\t\t{encrypt[i]}")
#     decrypt.append(decrypt_bits(encrypt[i]))
#     # print(f"Decrypt\t\t{encrypt}")
# plt.plot(decrypt, encrypt)
# plt.show()

# print("Origin", origin, bin(origin))
# print("Reversed", reverse, bin(reverse))
# print("Reversed First 4 Bits", reverse_4bits, bin(reverse_4bits))
# print("XOR First 4 Bits", xor_origin_rev_4b, bin(xor_origin_rev_4b))
# print("Encrypted", encrypt, bin(encrypt))
#
# print()
# print("First Origin 4 bits", first_origin_4bit, bin(first_origin_4bit))
# print("xor_encrypt_f4b", xor_encrypt_f4b, bin(xor_encrypt_f4b))
# print("xor_encrypt_f4b_rev", xor_encrypt_f4b_rev, bin(xor_encrypt_f4b_rev))
# print("decrypt", decrypt, bin(decrypt))

zoom = 0.1


img = np.array([
    [[1, 2, 3]],
    [[4, 5, 6]],
    [[7, 8, 9]],
], dtype=np.uint8)
img = cv.imread('./images/woman-in-red-hijab-3748399.jpg')
cv.imshow("Origin", cv.resize(img, (int(img.shape[1] * zoom), int(img.shape[0] * zoom))))

print(img.shape)

h = img.shape[0]
w = img.shape[1]
reverse_img = np.packbits(np.unpackbits(img.flatten()), bitorder='little').reshape((h, w, 3))

# reverse_img[:, :, 0] = np.packbits(np.unpackbits(img[:, :, 0].flatten()), bitorder='little').reshape(h, w)
# reverse_img[:, :, 1] = np.packbits(np.unpackbits(img[:, :, 1].flatten()), bitorder='little').reshape(h, w)
# reverse_img[:, :, 2] = np.packbits(np.unpackbits(img[:, :, 2].flatten()), bitorder='little').reshape(h, w)

encrypt = encrypt_bits(img, reverse_img)

cv.imshow("Encrypt", cv.resize(encrypt, (int(encrypt.shape[1] * zoom), int(encrypt.shape[0] * zoom))))

decrypt = decrypt_image(encrypt)
print(decrypt.shape)
cv.imshow("decrypt", cv.resize(decrypt, (int(decrypt.shape[1] * zoom), int(decrypt.shape[0] * zoom))))

if cv.waitKey(100000):
    pass
cv.destroyAllWindows()
