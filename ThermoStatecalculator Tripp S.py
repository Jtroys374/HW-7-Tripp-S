import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QMessageBox
from PyQt5.QtCore import Qt
from pyXSteam import XSteam


class SteamPropertiesCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Steam Properties Calculator')
        self.setGeometry(100, 100, 400, 250)

        self.state1_label = QLabel('State 1:', self)
        self.state1_combo1 = QComboBox(self)
        self.state1_combo1.addItems(['Pressure', 'Temperature', 'Enthalpy', 'Entropy', 'Volume', 'Quality'])
        self.state1_combo2 = QComboBox(self)
        self.state1_combo2.addItems(['SI', 'English'])
        self.state1_value_edit = QLineEdit(self)
        self.state1_unit_label = QLabel('', self)

        self.state2_label = QLabel('State 2:', self)
        self.state2_combo1 = QComboBox(self)
        self.state2_combo1.addItems(['Pressure', 'Temperature', 'Enthalpy', 'Entropy', 'Volume', 'Quality'])
        self.state2_combo2 = QComboBox(self)
        self.state2_combo2.addItems(['SI', 'English'])
        self.state2_value_edit = QLineEdit(self)
        self.state2_unit_label = QLabel('', self)

        self.calculate_button = QPushButton('Calculate', self)
        self.calculate_button.clicked.connect(self.calculate)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()

        hbox1.addWidget(self.state1_label)
        hbox1.addWidget(self.state1_combo1)
        hbox1.addWidget(self.state1_value_edit)
        hbox1.addWidget(self.state1_combo2)
        hbox1.addWidget(self.state1_unit_label)

        hbox2.addWidget(self.state2_label)
        hbox2.addWidget(self.state2_combo1)
        hbox2.addWidget(self.state2_value_edit)
        hbox2.addWidget(self.state2_combo2)
        hbox2.addWidget(self.state2_unit_label)

        hbox3.addWidget(self.calculate_button)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)
        self.show()

    def calculate(self):
        state1_property = self.state1_combo1.currentText().lower()
        state1_units = self.state1_combo2.currentText()

        state2_property = self.state2_combo1.currentText().lower()
        state2_units = self.state2_combo2.currentText()

        try:
            state1_value = float(self.state1_value_edit.text())
        except ValueError:
            self.showErrorMessage("Invalid input. Please enter a numeric value.")
            return

        try:
            state2_value = float(self.state2_value_edit.text())
        except ValueError:
            self.showErrorMessage("Invalid input. Please enter a numeric value.")
            return

        # Convert units if necessary
        state1_value, state1_units = self.convert_units(state1_property, state1_value, state1_units)
        state2_value, state2_units = self.convert_units(state2_property, state2_value, state2_units)

        steam_table = XSteam()

        # Calculate properties for state 1
        state1_properties = self.calculate_properties(state1_property, state1_value, steam_table)

        # Calculate properties for state 2
        state2_properties = self.calculate_properties(state2_property, state2_value, steam_table)

        # Calculate change in properties
        delta_properties = {}
        for key in state1_properties.keys():
            if key in state2_properties:
                delta_properties[key] = state2_properties[key] - state1_properties[key]

        self.showResult(state1_properties, state2_properties, delta_properties)

    def calculate_properties(self, property_name, value, steam_table):
        if property_name == 'pressure':
            return steam_table.tsat_p(value)
        elif property_name == 'temperature':
            return steam_table.pt(value)
        elif property_name == 'enthalpy':
            return steam_table.h_pt(*value)
        elif property_name == 'entropy':
            return steam_table.s_pt(*value)
        elif property_name == 'volume':
            return steam_table.v_pt(*value)
        elif property_name == 'quality':
            return steam_table.x_ph(*value)

    def convert_units(self, property_name, value, units):
        if units == 'English':
            if property_name == 'temperature':
                value = (value - 32) * 5 / 9  # Fahrenheit to Celsius
            elif property_name == 'pressure':
                value *= 6894.76  # psi to Pa
        # Add more conversions as needed
        return value, units

    def showResult(self, state1_properties, state2_properties, delta_properties):
        result = ""
        result += "State 1 Properties:\n"
        for key, value in state1_properties.items():
            result += f"{key.capitalize()}: {value:.2f}\n"
        result += "\n"

        result += "State 2 Properties:\n"
        for key, value in state2_properties.items():
            result += f"{key.capitalize()}: {value:.2f}\n"
        result += "\n"

        result += "Change in Properties:\n"
        for key, value in delta_properties.items():
            result += f"{key.capitalize()}: {value:.2f}\n"

        QMessageBox.information(self, 'Result', result)

    def showErrorMessage(self, message):
        QMessageBox.critical(self, 'Error', message, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SteamPropertiesCalculator()
    sys.exit(app.exec_())
