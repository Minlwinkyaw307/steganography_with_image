import numpy as np

from models.enums import EncryptionType


class ImageEncryption:

    def __init__(self):
        pass

    def encrypt_image(self, image, encryption_type: EncryptionType):
        if encryption_type == EncryptionType.REVERSED_XOR:
            return self._encrypt_image_by_reversed_xor(image)
        elif encryption_type == EncryptionType.NONE:
            return image
        else:
            raise Exception("Given Encryption Type is invalid")

    def decrypt_image(self, image, encryption_type: EncryptionType):
        if encryption_type == EncryptionType.REVERSED_XOR:
            return self._decrypt_image_by_reversed_xor(image)
        elif encryption_type == EncryptionType.NONE:
            return image
        else:
            pass

    def _encrypt_image_by_reversed_xor(self, origin):
        # ENCRYPTING
        origin = np.uint8(origin)
        reverse = np.packbits(np.unpackbits(origin.flatten()), bitorder='little').reshape(origin.shape)
        reverse_4bits = np.uint8(reverse & 0xF0)
        xor_origin_rev_4b = (origin ^ reverse_4bits) & 0xF0
        encrypt = xor_origin_rev_4b | np.uint8(reverse & 0x0F)

        return encrypt

    def _decrypt_image_by_reversed_xor(self, encrypted_image):
        # DECRYPTING
        encrypted_image = np.uint8(encrypted_image)
        first_origin_4bit = np.packbits(np.unpackbits((encrypted_image & 0x0F).flatten()),
                                        bitorder='little').reshape(encrypted_image.shape)
        xor_encrypt_f4b_rev = np.packbits(np.unpackbits(((encrypted_image ^ first_origin_4bit) & 0xF0).flatten()),
                                          bitorder='little').reshape(encrypted_image.shape)
        return np.uint8(xor_encrypt_f4b_rev | first_origin_4bit)
