from PySide6.QtCore import Qt, QPoint, QSize, QRect
from PySide6.QtWidgets import (QMainWindow,
                               QLineEdit,
                               QPushButton,
                               QGridLayout,
                               QWidget)

from gui_settings import GuiSettings


class Calculator(QMainWindow):
    def __init__(self, gui_settings: GuiSettings):
        super().__init__()
        self.width = gui_settings.scaled_width
        self.height = gui_settings.scaled_height
        self.center_of_device = gui_settings.center_of_device
        print(f'center_of_device: {self.center_of_device}')
        #left,top,width,height = 100,100,1000,800
        left,top = 100, 100
        left = self.center_of_device[0] - self.width//2
        top = self.center_of_device[1] - self.height//2
        print(f'left: {left}, top: {top}')
        #self.setGeometry(1600, 100, 230, 290)
        # self.setGeometry( QPoint(x,y), QSize(w, h) )
        top_left_corner = QPoint(left,top)
        print(f'top_left_corner: {top_left_corner}')
        calc_size = QSize(self.width,self.height)
        calc_rect = QRect(top_left_corner, calc_size)
        #self.setGeometry(calc_rect)
        #self.setFixedSize(230, 290)
        self.setFixedSize(self.height, self.width)
        self.setWindowOpacity(0.99)

        self.layout = QGridLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setup_display()

        self.layout.addWidget(self.display, 0, 0, 1, 4)

        self.buttons = [
            "C", "+/-", "%", "÷",
            "7", "8", "9", "x",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "0", ".", "="
        ]

        self.buttons_fcn = {
            "C": self.clear,
            "+/-": self.change_sign,
            "%": self.percent,
            "÷": self.divide,
            "x": self.multiply,
            "-": self.subtract,
            "+": self.add,
            "=": self.equal
        }

        self.result = None
        self.first_number = None
        self.second_number = None
        self.operator = None
        self.setup_push_buttons()


    def __get_btn_properties(self):
        return {
            "border": "1px solid rgba(0, 0, 0, 0.5)",
            "color": "white",
            "background-color": "lightblue",
            "color_pressed": "white",
            "number_color": "white",
            "number_color_pressed": "rgb(157, 157, 157)",
            "first_row_btn_color": "pink"
        }


    def __get_btn_styles(self):
        prop = self.__get_btn_properties()

        style_last_col = f"""
                        QPushButton{{
                            background-color: {prop['background-color']};
                            border: {prop['border']};
                            margin: 0;
                            font-size: 30px;
                        }}
                        QPushButton::pressed {{
                            background-color: {prop['color_pressed']}
                        }}
        """

        style_first_row = f"""
                        QPushButton{{
                            background-color: {prop['first_row_btn_color']};
                            border: {prop['border']};
                            margin: 0;
                            font-size: 25px;
                        }}
                        QPushButton::pressed {{
                            background-color: {prop['number_color']}
                        }}
                        """

        general_style = f"""
                        QPushButton{{
                            background-color: {prop['number_color']};
                            border: {prop['border']};
                            margin: 0;
                            font-size: 25px;
                        }}
                        QPushButton::pressed{{
                            background-color: {prop['number_color_pressed']};
                        }}
                        """
        return style_last_col, style_first_row, general_style


    def setup_push_buttons(self):
        width = 60
        height = 50

        row = 0
        col = 0
        style_last_col, style_first_row, general_style = self.__get_btn_styles()

        for btn_txt in self.buttons:
            btn = QPushButton(btn_txt)
            btn.pressed.connect(self.on_btn_clicked)
            if row == 4:
                if btn_txt == "0":
                    self.layout.addWidget(btn, row + 1, col, 1, 2)
                    btn.setFixedSize(2 * width, height)
                else:
                    self.layout.addWidget(btn, row + 1, col + 1, 1, 1)
                    btn.setFixedSize(width, height)
            else:
                self.layout.addWidget(btn, row + 1, col, 1, 1)
                btn.setFixedSize(width, height)
            col += 1

            if row == 0:
                btn.setStyleSheet(style_first_row)
            else:
                btn.setStyleSheet(general_style)

            if col > 3:
                btn.setStyleSheet(style_last_col)
                col = 0
                row += 1
            if btn_txt == "=":
                btn.setStyleSheet(style_last_col)


    def on_btn_clicked(self):
        '''
        Slot for all buttons
        '''
        btn = self.sender()
        btn_text = btn.text()

        if btn_text in self.buttons_fcn:
            self.buttons_fcn[btn_text]()
        elif btn_text == ".":
            if "." not in self.display.text():
                self.display.setText(self.display.text() + btn_text)
        else:
            if self.result:
                self.display.setText(btn_text)
                self.result = None
            else:
                self.display.setText(self.display.text() + btn_text)

            self.last_number = float(self.display.text())


    def clear(self):
        '''Clear line edit'''
        self.display.clear()


    def change_sign(self):
        '''
        Change the sign
        '''
        self.display.setText(str(float(self.display.text()) * -1))


    def percent(self):
        self.display.setText(str(float(self.display.text()) * 0.01))


    def divide(self):
        self.last_operator = "/"
        self.first_number = float(self.display.text())
        self.display.clear()


    def multiply(self):
        self.last_operator = "*"
        self.first_number = float(self.display.text())
        self.display.clear()


    def subtract(self):
        self.last_operator = "-"
        self.first_number = float(self.display.text())
        self.display.clear()


    def add(self):
        self.last_operator = "+"
        self.first_number = float(self.display.text())
        self.display.clear()


    def equal(self):
        if self.last_operator == "+":
            self.result = self.first_number + self.last_number
        elif self.last_operator == "-":
            self.result = self.first_number - self.last_number
        elif self.last_operator == "*":
            self.result = self.first_number * self.last_number
        elif self.last_operator == "/":
            self.result = self.first_number / self.last_number

        self.display.setText(str(round(self.result, 4)))
        self.first_number = round(self.result, 4)


    def setup_display(self):
        self.display = QLineEdit()
        self.display.setPlaceholderText('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.display.setFixedSize(230, 50)

        self.display.setStyleSheet("""
                                   QLineEdit {
                                       font-size: 40px;
                                       padding: 0 10 0 0;
                                       font-weight: bold;
                                       background-color: black;
                                       color: white;
                                   }
                                   """)


