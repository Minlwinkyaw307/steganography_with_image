import enum


class EncryptionType(enum.Enum):
    NONE = 'None'
    REVERSED_XOR = 'Reversed XOR'

    @staticmethod
    def as_list_of_supported_img_type():
        return [enc_type.value for enc_type in EncryptionType]

    @staticmethod
    def as_list_of_encryption_type():
        return [enc_type for enc_type in EncryptionType]


class SupportedInputImage(enum.Enum):
    jpg = 'jpg'
    jpeg = 'jpeg'
    png = 'png'
    tiff = 'tiff'
    bmp = 'bmp'

    @staticmethod
    def as_list_of_str():
        return [sup_type.value for sup_type in SupportedInputImage]

    @staticmethod
    def as_list_of_supported_img_type():
        return [sup_type for sup_type in SupportedInputImage]


class SupportedOutputImage(enum.Enum):
    png = 'png'
    tiff = 'tiff'
    bmp = 'bmp'

    @staticmethod
    def as_list_of_str():
        return [sup_type.value for sup_type in SupportedOutputImage]

    @staticmethod
    def as_list_of_supported_img_type():
        return [sup_type for sup_type in SupportedOutputImage]
