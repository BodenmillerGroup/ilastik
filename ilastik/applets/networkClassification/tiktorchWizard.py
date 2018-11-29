from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit

from tiktorch.build_spec import TikTorchSpec, BuildSpec
import yaml


class QIComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(QIComboBox, self).__init__(parent)


class MagicWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(MagicWizard, self).__init__(parent)
        self.addPage(Page1(self))
        self.setWindowTitle("Tiktorch Object Build Wizard")
        self.resize(640, 480)
        self.setOption(self.NoBackButtonOnStartPage)

class Page1(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)

        self.label1 = QtWidgets.QLabel()

        self.code_path_textbox = QLineEdit(self)
        self.code_path_textbox.setPlaceholderText("Path to the .py file")

        self.model_class_name_textbox = QLineEdit(self)
        self.model_class_name_textbox.setPlaceholderText("Name of the model class in the .py file")

        self.state_path_textbox = QLineEdit(self)
        self.state_path_textbox.setPlaceholderText("Path to where the state_dict is pickled")

        self.input_shape_textbox = QLineEdit(self)
        self.input_shape_textbox.setPlaceholderText("Input shape of the model in the order CHW")

        self.output_shape_textbox = QLineEdit(self)
        self.output_shape_textbox.setPlaceholderText("Output shape of the model in the order CHW")

        self.dynamic_input_shape_textbox = QLineEdit(self)
        self.dynamic_input_shape_textbox.setPlaceholderText("dynamic_input_shape (Optional)")

        self.devices_textbox = QLineEdit(self)
        self.devices_textbox.setPlaceholderText("List of devices (e.g. 'cpu:0' or ['cuda:0', 'cuda:1'])")

        self.model_init_kwargs_textbox = QLineEdit(self)
        self.model_init_kwargs_textbox.setPlaceholderText("Kwargs to the model constructor (Optional)")

        self.model_path_textbox = QLineEdit(self)
        self.model_path_textbox.setPlaceholderText("Path were the object will be saved")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.code_path_textbox)
        layout.addWidget(self.model_class_name_textbox)
        layout.addWidget(self.state_path_textbox)
        layout.addWidget(self.input_shape_textbox)
        layout.addWidget(self.output_shape_textbox)
        layout.addWidget(self.dynamic_input_shape_textbox)
        layout.addWidget(self.devices_textbox)
        layout.addWidget(self.model_init_kwargs_textbox)
        layout.addWidget(self.model_path_textbox)
        self.setLayout(layout)

    def initializePage(self):
        self.label1.setText("Parameters:")

    def validatePage(self):
        # will be triggered after pressing Done
        self.saveParameters()
        return True

    def saveParameters(self):
        """
        Saves the parameters as tiktorch Object
        """
        self.code_path = str(self.code_path_textbox.text())
        self.model_class_name = str(self.model_class_name_textbox.text())
        self.state_path = str(self.state_path_textbox.text())
        self.input_shape = [int(x) for x in self.input_shape_textbox.text().split(',')]
        self.output_shape = [int(x) for x in self.output_shape_textbox.text().split(',')]
        self.dynamic_input_shape = str(self.dynamic_input_shape_textbox.text())
        self.devices = [x for x in str(self.devices_textbox.text()).split(',')]
        self.model_init_kwargs = yaml.load(str(self.model_init_kwargs_textbox.text()))
        self.model_path = str(self.model_path_textbox.text())

        spec = TikTorchSpec(
            code_path=self.code_path,
            model_class_name=self.model_class_name,
            state_path=self.state_path,
            input_shape=self.input_shape,
            output_shape=self.output_shape,
            dynamic_input_shape=self.dynamic_input_shape,
            devices=self.devices,
            model_init_kwargs=self.model_init_kwargs,
        )

        buildface = BuildSpec(self.model_path)
        buildface.build(spec)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    wizard = MagicWizard()
    wizard.show()
    sys.exit(app.exec_())
