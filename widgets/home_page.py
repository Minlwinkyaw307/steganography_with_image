from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import os
import traceback
from cv2 import imwrite, imread, imshow, waitKey, destroyAllWindows

from models.enums import EncryptionType, SupportedInputImage, SupportedOutputImage
from models.steganography import Steganography
from models.image_encryption import ImageEncryption


class HomePage(object):
    def __init__(self, ):
        object.__init__(self)
        self._steganography = Steganography()
        self._image_encryption = ImageEncryption()

    def setupUi(self, MainWindow):
        # Main Windows
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(800, 675)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Embedding Image Section Frame
        self.embedding_image_section_frame = QtWidgets.QFrame(self.centralwidget)
        self.embedding_image_section_frame.setGeometry(QtCore.QRect(5, 10, 791, 321))
        self.embedding_image_section_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.embedding_image_section_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.embedding_image_section_frame.setObjectName("embedding_image_section_frame")

        # Embedding Image Section Label
        self.embed_image_section_label = QtWidgets.QLabel(self.embedding_image_section_frame)
        self.embed_image_section_label.setGeometry(QtCore.QRect(10, 10, 771, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.embed_image_section_label.sizePolicy().hasHeightForWidth())
        self.embed_image_section_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.embed_image_section_label.setFont(font)
        self.embed_image_section_label.setObjectName("embed_image_section_label")

        # Embedding's secret image edit box
        self.secret_image_edit_box = QtWidgets.QLineEdit(self.embedding_image_section_frame)
        self.secret_image_edit_box.setGeometry(QtCore.QRect(140, 100, 641, 41))
        self.secret_image_edit_box.setText("")
        self.secret_image_edit_box.setObjectName("secret_image_edit_box")
        self.secret_image_btn = QtWidgets.QPushButton(self.embedding_image_section_frame)
        self.secret_image_btn.setGeometry(QtCore.QRect(10, 100, 121, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.secret_image_btn.sizePolicy().hasHeightForWidth())
        self.secret_image_btn.setSizePolicy(sizePolicy)
        self.secret_image_btn.setObjectName("secret_image_btn")

        # Encryption Type Label (Embed)
        self.encryption_type_label = QtWidgets.QLabel(self.embedding_image_section_frame)
        self.encryption_type_label.setGeometry(QtCore.QRect(20, 160, 211, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.encryption_type_label.sizePolicy().hasHeightForWidth())
        self.encryption_type_label.setSizePolicy(sizePolicy)
        self.encryption_type_label.setObjectName("encryption_type_label")
        # End of Encryption Type Label (Embed)

        # Output Image Type Label (Embed)
        self.embed_image_output_image_type_label = QtWidgets.QLabel(self.embedding_image_section_frame)
        self.embed_image_output_image_type_label.setGeometry(QtCore.QRect(20, 210, 211, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.embed_image_output_image_type_label.sizePolicy().hasHeightForWidth())
        self.embed_image_output_image_type_label.setSizePolicy(sizePolicy)
        self.embed_image_output_image_type_label.setObjectName("embed_image_output_image_type")
        # End of EOutput Image Type Label (Embed)

        # Encryption Type Combo Box (Embed)
        self.embed_image_encryption_type_combo_box = QtWidgets.QComboBox(self.embedding_image_section_frame)
        self.embed_image_encryption_type_combo_box.setEnabled(True)
        self.embed_image_encryption_type_combo_box.setGeometry(QtCore.QRect(240, 160, 541, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.embed_image_encryption_type_combo_box.sizePolicy().hasHeightForWidth())
        self.embed_image_encryption_type_combo_box.setSizePolicy(sizePolicy)
        self.embed_image_encryption_type_combo_box.setAcceptDrops(False)
        self.embed_image_encryption_type_combo_box.setObjectName("encryption_type_combo_box")
        # End of Encryption Type Combo Box (Embed)

        # Output Type Combo Box (Embed)
        self.embed_output_image_type_combo_box = QtWidgets.QComboBox(self.embedding_image_section_frame)
        self.embed_output_image_type_combo_box.setEnabled(True)
        self.embed_output_image_type_combo_box.setGeometry(QtCore.QRect(240, 210, 541, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.embed_output_image_type_combo_box.sizePolicy().hasHeightForWidth())
        self.embed_output_image_type_combo_box.setSizePolicy(sizePolicy)
        self.embed_output_image_type_combo_box.setAcceptDrops(False)
        self.embed_output_image_type_combo_box.setObjectName("embed_output_image_type_combo_box")
        # End of Output Type Combo Box (Embed)

        self.hide_image_action_btn = QtWidgets.QPushButton(self.embedding_image_section_frame)
        self.hide_image_action_btn.setGeometry(QtCore.QRect(660, 270, 121, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hide_image_action_btn.sizePolicy().hasHeightForWidth())
        self.hide_image_action_btn.setSizePolicy(sizePolicy)
        self.hide_image_action_btn.setObjectName("base_image_btn_2")


        self.embed_image_section_error_label = QtWidgets.QLabel(self.embedding_image_section_frame)
        self.embed_image_section_error_label.setGeometry(QtCore.QRect(20, 270, 631, 41))
        self.embed_image_section_error_label.setObjectName("label")

        self.base_image_edit_box = QtWidgets.QLineEdit(self.embedding_image_section_frame)
        self.base_image_edit_box.setGeometry(QtCore.QRect(140, 50, 641, 41))
        self.base_image_edit_box.setObjectName("base_image_edit_box")

        self.base_image_btn = QtWidgets.QPushButton(self.embedding_image_section_frame)
        self.base_image_btn.setGeometry(QtCore.QRect(10, 50, 121, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.base_image_btn.sizePolicy().hasHeightForWidth())
        self.base_image_btn.setSizePolicy(sizePolicy)
        self.base_image_btn.setObjectName("base_image_btn")

        self.extractiong_image_section_frame = QtWidgets.QFrame(self.centralwidget)
        self.extractiong_image_section_frame.setGeometry(QtCore.QRect(5, 340, 791, 291))
        self.extractiong_image_section_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.extractiong_image_section_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.extractiong_image_section_frame.setObjectName("extractiong_image_section_frame")

        self.extract_image_section_label = QtWidgets.QLabel(self.extractiong_image_section_frame)
        self.extract_image_section_label.setGeometry(QtCore.QRect(10, 10, 771, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extract_image_section_label.sizePolicy().hasHeightForWidth())
        self.extract_image_section_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.extract_image_section_label.setFont(font)
        self.extract_image_section_label.setObjectName("extract_image_section_label")

        self.embedded_image_location_edit_box = QtWidgets.QLineEdit(self.extractiong_image_section_frame)
        self.embedded_image_location_edit_box.setGeometry(QtCore.QRect(140, 50, 641, 41))
        self.embedded_image_location_edit_box.setText("")
        self.embedded_image_location_edit_box.setObjectName("embedded_image_location_edit_box")

        self.embedded_image_btn = QtWidgets.QPushButton(self.extractiong_image_section_frame)
        self.embedded_image_btn.setGeometry(QtCore.QRect(10, 50, 121, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.embedded_image_btn.sizePolicy().hasHeightForWidth())
        self.embedded_image_btn.setSizePolicy(sizePolicy)
        self.embedded_image_btn.setObjectName("embedded_image_btn")

        self.extraction_image_encryption_label = QtWidgets.QLabel(self.extractiong_image_section_frame)
        self.extraction_image_encryption_label.setGeometry(QtCore.QRect(20, 110, 211, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extraction_image_encryption_label.sizePolicy().hasHeightForWidth())
        self.extraction_image_encryption_label.setSizePolicy(sizePolicy)
        self.extraction_image_encryption_label.setObjectName("extraction_image_encryption_label")

        self.extraction_image_encryption_combox = QtWidgets.QComboBox(self.extractiong_image_section_frame)
        self.extraction_image_encryption_combox.setEnabled(True)
        self.extraction_image_encryption_combox.setGeometry(QtCore.QRect(240, 110, 541, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extraction_image_encryption_combox.sizePolicy().hasHeightForWidth())
        self.extraction_image_encryption_combox.setSizePolicy(sizePolicy)
        self.extraction_image_encryption_combox.setAcceptDrops(False)
        self.extraction_image_encryption_combox.setObjectName("extraction_image_encryption_combox")

        self.extract_image_btn = QtWidgets.QPushButton(self.extractiong_image_section_frame)
        self.extract_image_btn.setGeometry(QtCore.QRect(660, 240, 121, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extract_image_btn.sizePolicy().hasHeightForWidth())
        self.extract_image_btn.setSizePolicy(sizePolicy)
        self.extract_image_btn.setObjectName("extract_image_btn")

        self.extract_image_error = QtWidgets.QLabel(self.extractiong_image_section_frame)
        self.extract_image_error.setGeometry(QtCore.QRect(20, 240, 631, 41))
        self.extract_image_error.setObjectName("extract_image_error")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Steganography For Images"))
        # Setting on value change on line edit
        self.base_image_edit_box.textChanged.connect(partial(
            self.on_line_edit_value_change,
            self.base_image_edit_box,
            self.embed_image_section_error_label
        ))
        self.secret_image_edit_box.textChanged.connect(partial(
            self.on_line_edit_value_change,
            self.secret_image_edit_box,
            self.embed_image_section_error_label
        ))
        self.embedded_image_location_edit_box.textChanged.connect(partial(
            self.on_line_edit_value_change,
            self.embedded_image_location_edit_box,
            self.embed_image_section_error_label
        ))

        # Labels
        self.embed_image_section_label.setText(_translate("MainWindow", "Embed Image"))
        self.encryption_type_label.setText(_translate("MainWindow", "Encryption Type"))
        self.extract_image_section_label.setText(_translate("MainWindow", "Extract Image"))
        self.extraction_image_encryption_label.setText(_translate("MainWindow", "Encryption Type"))
        self.embed_image_output_image_type_label.setText(_translate("MainWindow", "Output Image Type"))

        # Error Labels
        self.extract_image_error.setText(_translate("MainWindow", ""))
        self.embed_image_section_error_label.setText(_translate("MainWindow", ""))

        # File Import Buttons

        # Base Image Import Button
        self.base_image_btn.setText(_translate("MainWindow", "Base Image"))
        self.base_image_btn.setToolTip('Select Base Image To Hide Secret Image Inside')
        self.base_image_btn.clicked.connect(
            partial(self.open_file_selection_dialog, self.base_image_edit_box, self.embed_image_section_error_label))

        self.secret_image_btn.setText(_translate("MainWindow", "Secret Image"))  # Secret Image Button
        self.secret_image_btn.setToolTip('Select Secret Image That Will Be Embedded Inside Base Image')
        self.secret_image_btn.clicked.connect(partial(self.open_file_selection_dialog,
                                                      self.secret_image_edit_box,
                                                      self.embed_image_section_error_label))

        self.embedded_image_btn.setText(_translate("MainWindow", "Image"))
        self.embedded_image_btn.setToolTip('Select Image which embedded Secret Image')
        self.embedded_image_btn.clicked.connect(partial(self.open_file_selection_dialog,
                                                        self.embedded_image_location_edit_box,
                                                        self.extract_image_error))

        # Action Buttons
        self.hide_image_action_btn.setText(_translate("MainWindow", "Hide Image"))
        self.hide_image_action_btn.clicked.connect(self.on_click_embed_image)
        self.extract_image_btn.setText(_translate("MainWindow", "Extract Image"))
        self.extract_image_btn.clicked.connect(self.on_click_extract_image)

        for encryption_type in EncryptionType:
            # Embedding Encryption Type Combo Box
            self.embed_image_encryption_type_combo_box.addItem(encryption_type.value)
            # Extraction Encryption Type Combo Box
            self.extraction_image_encryption_combox.addItem(encryption_type.value)
        for supported_img_type in SupportedOutputImage:
            self.embed_output_image_type_combo_box.addItem(supported_img_type.value)

    @property
    def base_image_location(self):
        base_image_location_temp = self.base_image_edit_box.text()
        if not os.path.isfile(base_image_location_temp):
            raise Exception('Base image path is not a file')
        else:
            if base_image_location_temp.split('.')[-1] in SupportedInputImage.as_list_of_str():
                return base_image_location_temp
            raise Exception('Base image file type is not supported')

    @property
    def secret_image_location(self):
        secret_image_location_temp = self.secret_image_edit_box.text()
        if not os.path.isfile(secret_image_location_temp):
            raise Exception('secret image path is not a file')
        else:
            if secret_image_location_temp.split('.')[-1] in SupportedInputImage.as_list_of_str():
                return secret_image_location_temp
            raise Exception('Secret image file type is not supported')

    @property
    def embedded_image_location(self):
        embedded_image_location_temp = self.embedded_image_location_edit_box.text()
        if not os.path.isfile(embedded_image_location_temp):
            raise Exception('Embedded image path is not a file')
        else:
            if embedded_image_location_temp.split('.')[-1] in SupportedOutputImage.as_list_of_str():
                return embedded_image_location_temp
            raise Exception('Embedded image file type is not supported')

    @property
    def embed_image_encryption_type(self):
        for enc_type in EncryptionType.as_list_of_encryption_type():
            if self.embed_image_encryption_type_combo_box.currentText() == enc_type.value:
                return enc_type
        raise Exception("Selected encryption type isn't in the supported list")

    @property
    def extract_image_encryption_type(self):
        for enc_type in EncryptionType.as_list_of_encryption_type():
            if self.extraction_image_encryption_combox.currentText() == enc_type.value:
                return enc_type
        raise Exception("Selected encryption type isn't in the supported list")


    def open_file_selection_dialog(self, edit_box: QtWidgets.QLineEdit, error_label: QtWidgets.QLabel):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        supported_type = ['*.' + supp_type.value for supp_type in SupportedInputImage]
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Selecte Image File", "",
                                                            f"Image Files ({' '.join([s for s in supported_type])})",
                                                            options=options)
        if fileName == "":
            return
        if not os.path.exists(fileName):
            error_label.setText("Please Select Valid File")
            edit_box.setText("")
            return

        edit_box.setText(fileName)

    def open_save_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        supported_type = ['*.' + supp_type.value for supp_type in SupportedOutputImage]
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            None,
            "Save Image",
            "", f"Image Files ({' '.join([s for s in supported_type])})", options=options)
        return fileName

    def on_line_edit_value_change(self, line_edit: QtWidgets.QLineEdit, error_label: QtWidgets.QLabel):
        if not os.path.isfile(line_edit.text()):
            error_label.setText("Please Select Valid File")
            error_label.setStyleSheet('color: red')
        else:
            error_label.setText("")

    def save_image(self, image, file_name: str, image_type: str, label: QtWidgets.QLabel):
        file_name_split = file_name.split('.')
        if len(file_name_split) > 1:
            file_name_split[-1] = '.' + image_type
        elif len(file_name_split) == 1:
            file_name_split.append('.' + image_type)
        file_name = ''.join(a for a in file_name_split)
        imwrite(file_name, image)

        label.setText("Image Has Been Saved Successfully")
        label.setStyleSheet('color: green')

    def on_click_embed_image(self):
        try:
            base_image = imread(self.base_image_location)
            base_image = base_image & 0xFC
            secret_image = imread(self.secret_image_location)
            if secret_image.shape[0] * secret_image.shape[1] > base_image.shape[0] * base_image.shape[1] / 4:
                raise Exception("Selected secret image Size is bigger than base image can hold")
            secret_image = self._image_encryption.encrypt_image(
                secret_image,
                self.embed_image_encryption_type,
            )
            result_image = self._steganography.add_secret_image_inside_base_image(base_image, secret_image)
            file_name = self.open_save_file_dialog()

            self.save_image(result_image, file_name, self.embed_output_image_type_combo_box.currentText(),
                            self.embed_image_section_error_label)

            # imshow(file_name, result_image)
            # if waitKey(10000):
            #     pass
            # destroyAllWindows()

        except Exception as e:
            print(traceback.format_exc())
            print(str(e))
            self.embed_image_section_error_label.setText(str(e))
            self.embed_image_section_error_label.setStyleSheet('color: red')

    def on_click_extract_image(self):
        try:
            embedded_image = imread(self.embedded_image_location)
            encrypted_image = self._steganography.get_secret_image_inside_base_image(embedded_image)
            result_image = self._image_encryption.decrypt_image(encrypted_image, self.extract_image_encryption_type)

            file_name = self.open_save_file_dialog()
            self.save_image(result_image, file_name, 'jpg',
                            self.extract_image_error)
        except Exception as e:
            print(traceback.format_exc())
            print(str(e))
            self.extract_image_error.setText(str(e))
            self.extract_image_error.setStyleSheet('color: red')
