from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QStackedWidget, QComboBox, QLabel
from PyQt6.uic import loadUi
import requests
import json
import random
import time
import sys
from currency_lists_file import currency_areas, currency_codes
import edit_database

logged_in_user = edit_database.fetch_logged_in_user().replace("@", "_at_").replace(".", "_dot_")
selection_top = []

for item in range(161):
    selection_top.append(currency_codes[item] + " (" + currency_areas[item] + ")")

print(edit_database.fetch_preferences(logged_in_user)[0])

random_selection = [100, 500, 26, 19.16, 1]
class Mainconverter(QWidget):
    def setUp(self):
        loadUi('mainconverter.ui', self)

        self.insertBudget_lineedit = self.findChild(QLineEdit, 'insertBudget_lineedit')
        self.calculate_button = self.findChild(QPushButton, 'calculate_button')
        self.price_tag = self.findChild(QLabel, 'input_price_label')
        self.currency_label = self.findChild(QComboBox, 'switch_currency_label')
        self.stacked_two = self.findChild(QStackedWidget, 'stackedWidget')
        self.customize_button = self.findChild(QPushButton, 'customize_button')
        self.selection_one = self.findChild(QComboBox, 'selection_combo_one')
        self.selection_two = self.findChild(QComboBox, 'selection_combo_two')
        self.selection_three = self.findChild(QComboBox, 'selection_combo_three')
        self.selection_four = self.findChild(QComboBox, 'selection_combo_four')
        self.selection_five = self.findChild(QComboBox, 'selection_combo_five')
        self.selection_six = self.findChild(QComboBox, 'selection_combo_six')
        self.selection_seven = self.findChild(QComboBox, 'selection_combo_seven')
        self.selection_eight = self.findChild(QComboBox, 'selection_combo_eight')

        self.currency_label_one = self.findChild(QLabel, 'currency_label_one')
        self.currency_label_two = self.findChild(QLabel, 'currency_label_two')
        self.currency_label_three = self.findChild(QLabel, 'currency_label_three')
        self.currency_label_four = self.findChild(QLabel, 'currency_label_four')
        self.currency_label_five = self.findChild(QLabel, 'currency_label_five')
        self.currency_label_six = self.findChild(QLabel, 'currency_label_six')
        self.currency_label_seven = self.findChild(QLabel, 'currency_label_seven')
        self.currency_label_eight = self.findChild(QLabel, 'currency_label_eight')

        self.currency_conversion_label_one = self.findChild(QLabel, 'currency_conversion_label_one')
        self.currency_conversion_label_two = self.findChild(QLabel, 'currency_conversion_label_two')
        self.currency_conversion_label_three = self.findChild(QLabel, 'currency_conversion_label_three')
        self.currency_conversion_label_four = self.findChild(QLabel, 'currency_conversion_label_four')
        self.currency_conversion_label_five = self.findChild(QLabel, 'currency_conversion_label_five')
        self.currency_conversion_label_six = self.findChild(QLabel, 'currency_conversion_label_six')
        self.currency_conversion_label_seven = self.findChild(QLabel, 'currency_conversion_label_seven')
        self.currency_conversion_label_eight = self.findChild(QLabel, 'currency_conversion_label_eight')

        self.currency_label.addItems(selection_top)
        self.selection_one.addItems(currency_codes)
        self.selection_two.addItems(currency_codes)
        self.selection_three.addItems(currency_codes)
        self.selection_four.addItems(currency_codes)
        self.selection_five.addItems(currency_codes)
        self.selection_six.addItems(currency_codes)
        self.selection_seven.addItems(currency_codes)
        self.selection_eight.addItems(currency_codes)

        preferences = edit_database.fetch_preferences(logged_in_user)

        self.selection_one.setCurrentIndex(currency_codes.index(preferences[1]))
        self.selection_two.setCurrentIndex(currency_codes.index(preferences[2]))
        self.selection_three.setCurrentIndex(currency_codes.index(preferences[3]))
        self.selection_four.setCurrentIndex(currency_codes.index(preferences[4]))
        self.selection_five.setCurrentIndex(currency_codes.index(preferences[5]))
        self.selection_six.setCurrentIndex(currency_codes.index(preferences[6]))
        self.selection_seven.setCurrentIndex(currency_codes.index(preferences[7]))
        self.selection_eight.setCurrentIndex(currency_codes.index(preferences[8]))

        self.currency_label_one.setText(self.selection_one.currentText())
        self.currency_label_two.setText(self.selection_two.currentText())
        self.currency_label_three.setText(self.selection_three.currentText())
        self.currency_label_four.setText(self.selection_four.currentText())
        self.currency_label_five.setText(self.selection_five.currentText())
        self.currency_label_six.setText(self.selection_six.currentText())
        self.currency_label_seven.setText(self.selection_seven.currentText())
        self.currency_label_eight.setText(self.selection_eight.currentText())

        self.currency_label.setCurrentIndex(currency_codes.index(preferences[0]))

        self.stacked_two.setCurrentIndex(0)
        self.customize_button.clicked.connect(self.turn_page)
        self.currency_label.currentTextChanged.connect(self.initialise_update)
        self.calculate_button.clicked.connect(self.update_price_tag)

    def update_price_tag(self):
        self.price_tag.setText(self.insertBudget_lineedit.text())

        self.initialise_update()

    def initialise_update(self):
        first_pair = self.currency_label.currentText()[0:3]
        r = requests.get('https://v6.exchangerate-api.com/v6/0cc1ee779f592fb436ec2b9d/latest/'
                         + first_pair)

        value_chart = r.json()['conversion_rates']
        self.stacked_two.setCurrentIndex(0)
        self.customize_button.setText('Customize Currencies')

        self.currency_label_one.setText(self.selection_one.currentText())
        self.currency_label_two.setText(self.selection_two.currentText())
        self.currency_label_three.setText(self.selection_three.currentText())
        self.currency_label_four.setText(self.selection_four.currentText())
        self.currency_label_five.setText(self.selection_five.currentText())
        self.currency_label_six.setText(self.selection_six.currentText())
        self.currency_label_seven.setText(self.selection_seven.currentText())
        self.currency_label_eight.setText(self.selection_eight.currentText())

        self.currency_conversion_label_one.setNum(value_chart.get(self.selection_one.currentText()) * float(self.price_tag.text()))
        self.currency_conversion_label_two.setNum(value_chart.get(self.selection_two.currentText()) * float(self.price_tag.text()))
        self.currency_conversion_label_three.setNum(value_chart.get(self.selection_three.currentText()) * float(self.price_tag.text()))
        self.currency_conversion_label_four.setNum(value_chart.get(self.selection_four.currentText()) * float(self.price_tag.text()))
        self.currency_conversion_label_five.setNum(value_chart.get(self.selection_five.currentText()) * float(self.price_tag.text()))
        self.currency_conversion_label_six.setNum(value_chart.get(self.selection_six.currentText()) * float(self.price_tag.text()))
        self.currency_conversion_label_seven.setNum(value_chart.get(self.selection_seven.currentText()) * float(self.price_tag.text()))
        self.currency_conversion_label_eight.setNum(value_chart.get(self.selection_eight.currentText()) * float(self.price_tag.text()))

        list_upload = [
            first_pair,
            self.selection_one.currentText(),
            self.selection_two.currentText(),
            self.selection_three.currentText(),
            self.selection_four.currentText(),
            self.selection_five.currentText(),
            self.selection_six.currentText(),
            self.selection_seven.currentText(),
            self.selection_eight.currentText()
        ]
        edit_database.update_preferences_by_list(logged_in_user, list_upload)
    def turn_page(self):

        if self.stacked_two.currentIndex() == 0:
            self.stacked_two.setCurrentIndex(1)
            self.customize_button.setText('Back to currencies')
        else:
            self.initialise_update()



if __name__ == '__main__':
    app = QApplication([])
    window = Mainconverter()
    window.show()
    sys.exit(app.exec())
