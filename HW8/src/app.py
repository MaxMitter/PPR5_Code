import os
import pathlib
import shutil
from os import listdir
from os.path import isfile

import converter as conv

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
from window import Ui_MainWindow


class Application(Ui_MainWindow):
    files_folder = "./files"

    def __init__(self):
        super().__init__()
        os.makedirs(self.files_folder, exist_ok=True)
    # ------- Event Handlers -------- #

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        # connect Event Handlers #
        self.btn_AddFile.clicked.connect(self._on_add_file)
        self.btn_DeleteFile.clicked.connect(self._on_remove_file)
        self.listWidget_Files.itemClicked.connect(self._select_file)
        self.btn_DeleteRow.clicked.connect(self._on_delete_row)
        self.btn_DeleteCol.clicked.connect(self._on_delete_col)
        self.btn_Export.clicked.connect(self._on_export)
        self._update_file_list()

    def _on_add_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            caption="Open File",
            filter=".txt (*.txt);;.csv (*.csv);;.json (*.json);;.db(*.db)")

        if not file_name or file_name == "":
            return

        if self.file_exists(pathlib.Path(file_name)):
            Application._display_error("File already uploaded")
            return

        self.copy_file(file_name)
        self._update_file_list()

    def _on_remove_file(self):
        file_name = self.listWidget_Files.selectedItems()
        if len(file_name) > 0:
            try:
                path = os.path.join(self.files_folder, file_name[0].text())
                os.remove(path)
                self.reset_table()
                self._update_file_list()
            except OSError as err:
                Application._display_error(f"File delete error: {err}")

    def _select_file(self):
        self.reset_table()
        try:
            file_name = self.listWidget_Files.selectedItems()
            if len(file_name) < 1:
                return

            path = pathlib.Path(os.path.join(self.files_folder, file_name[0].text()))

            if path.suffix == ".txt" or path.suffix == ".csv":
                self.data = conv.parseCsvFile(path.__str__(), ";")
            elif path.suffix == ".json":
                self.data = conv.parseJsonFile(path.__str__())
            elif path.suffix == ".db":
                self.data = conv.parseDbFile(path.__str__(), path.name)
            else:
                Application._display_error("Invalid File Type")
                return

            self.update_data_table()
        except BaseException as ex:
            print(ex)

    def _update_file_list(self):
        files = self.get_all_files()
        self.listWidget_Files.clear()
        for file in files:
            self.listWidget_Files.addItem(file)

    def _on_data_changed(self, item):
        file_path = self.get_selected_file_path()
        self.data.iloc[item.row(), item.column()] = item.text()
        conv.updateFile(file_path, self.data)

    def _on_delete_row(self):
        row = self.table_Data.currentRow()
        file_path = os.path.join(self.files_folder, self.listWidget_Files.selectedItems()[0].text())

        if row >= 0:
            self.data.drop([row], inplace=True)
            self.table_Data.removeRow(row)
            conv.updateFile(file_path, self.data)

    def _on_delete_col(self):
        col = self.table_Data.currentColumn()
        header = self.table_Data.horizontalHeaderItem(col).text()
        file_path = os.path.join(self.files_folder, self.listWidget_Files.selectedItems()[0].text())

        if col >= 0:
            self.data.drop(columns=[header], inplace=True)
            self.table_Data.removeColumn(col)
            conv.updateFile(file_path, self.data)

    def _on_export(self):
        file_path = pathlib.Path(self.get_selected_file_path())
        conv.exportFiles(self.data, file_path.absolute())

    # ------------ Util Functions ------------ #

    def get_selected_file_path(self):
        return os.path.join(self.files_folder, self.listWidget_Files.selectedItems()[0].text())

    def reset_table(self):
        self.table_Data.clear()
        self.table_Data.setRowCount(0)
        self.table_Data.setColumnCount(0)

    def update_data_table(self):
        rows, cols = self.data.shape
        headers = []
        self.table_Data.setColumnCount(cols)
        self.table_Data.setRowCount(rows)
        for i in range(0, cols):
            headers.append(self.data.columns[i])
            for j in range(0, rows):
                item = QTableWidgetItem(str(self.data.iloc[j, i]))
                self.table_Data.setItem(j, i, item)

        self.table_Data.setHorizontalHeaderLabels(headers)
        self.table_Data.resizeColumnsToContents()
        self.table_Data.resizeRowsToContents()
        self.table_Data.itemChanged.connect(self._on_data_changed)

    def copy_file(self, file_name: str):
        shutil.copyfile(file_name, os.path.join(self.files_folder, pathlib.Path(file_name).name))

    def file_exists(self, file_path: pathlib.Path) -> bool:
        file_path = pathlib.Path(os.path.join(self.files_folder, file_path.name))
        for file in listdir(self.files_folder):
            test_file = pathlib.Path(os.path.join(self.files_folder, file))
            if isfile(test_file):
                if test_file.absolute() == file_path.absolute():
                    return True
        return False

    def remove_file(self, file_path: str):
        os.remove(os.path.join(self.files_folder, pathlib.Path(file_path).name))

    def get_all_files(self):
        return [l for l in listdir(self.files_folder) if os.path.isfile(l)]

    @staticmethod
    def _display_error(error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error)
        msg.setWindowTitle("Error")
        msg.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Application()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
