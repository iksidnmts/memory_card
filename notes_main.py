from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QGroupBox, QButtonGroup, QTextEdit, QListWidget, QLineEdit, QInputDialog

import json

def add_note():
    note_name, ok = QInputDialog.getText(
        mw, 'Добавить заметку', 'Название заметки:'
    )
    if ok and note_name != '':
        notes[note_name] = {'текст' : '', 'теги' : []}
        notes_list.addItem(note_name)

notes = {
    'Добро пожаловать!' : {
        'текст' : 'бла бла бла', 
        'теги' : ['бархатные', 'тяги']
    }
}

def save_note():
    if notes_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        notes[note_name]['текст'] = text_note.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)  
        print(notes)
    
def show_note():
    note_name = notes_list.selectedItems()[0].text()
    text_note.setText(notes[note_name]['текст'])
    tag_list.clear()
    tag_list.addItems(notes[note_name]['теги'])

def delete_note():
    if notes_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        del notes[note_name]
        notes_list.clear()
        tag_list.clear()
        text_note.clear()
        notes_list.addItems(notes)
    with open('notes_data.json', 'w') as file:
        json.dump(notes, file, sort_keys = True)  
    print(notes)

def add_tag():
    if notes_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        tag = note_tag.text()
        if not tag in notes[note_name]['теги']:
            notes[note_name]['теги'].append(tag)
            tag_list.addItem(tag)
            text_note.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)
    else:
        print('Заметка для добавления тега не выбрана')

def delete_tag():
    if tag_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        tag = tag_list.selectedItems()[0].text()
        notes[note_name]['теги'].remove(tag)
        tag_list.clear()
        tag_list.addItems(notes[note_name]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True)

def search_tag():
    tag = note_tag.text()
    if btn_search_tag.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        btn_search_tag.setText('Сбросить поиск')
        notes_list.clear()
        tag_list.clear()
        notes_list.addItems(notes_filtered)
    elif btn_search_tag.text() == 'Сбросить поиск':
        text_note.clear()
        notes_list.clear()
        tag_list.clear()
        notes_list.addItems(notes)
        btn_search_tag.setText('Искать заметки по тегу')
    else:
        pass


with open('notes_data.json', 'w') as file:
    json.dump(notes, file)

app = QApplication([])
mw = QWidget()
mw.setWindowTitle('Умные заметки')

text_note = QTextEdit()

notes_list_label = QLabel('Список заметок')
notes_list = QListWidget()

btn_create_note = QPushButton('Создать заметку')
btn_delete_note = QPushButton('Удалить заметку')
btn_save_note = QPushButton('Сохранить заметку')

tag_list_label = QLabel('Список тегов')
tag_list = QListWidget()
note_tag = QLineEdit()
note_tag.setPlaceholderText('Введите тэг...')

btn_pin_note = QPushButton('Добавить к заметке')
btn_unpin_note = QPushButton('Открепить от заметки')
btn_search_tag = QPushButton('Искать заметки по тегу')


m_layout = QHBoxLayout()
m_line1 = QVBoxLayout()
m_line2 = QVBoxLayout()
line_2_1 = QHBoxLayout()
line_2_2 = QHBoxLayout()
line_2_3 = QHBoxLayout()
line_2_4 = QHBoxLayout()

m_line1.addWidget(text_note)

m_line2.addWidget(notes_list_label)
m_line2.addWidget(notes_list)
line_2_1.addWidget(btn_create_note)
line_2_1.addWidget(btn_delete_note)
line_2_2.addWidget(btn_save_note)

m_line2.addLayout(line_2_1)
m_line2.addLayout(line_2_2)

m_line2.addWidget(tag_list_label)
m_line2.addWidget(tag_list)
m_line2.addWidget(note_tag)
line_2_3.addWidget(btn_pin_note)
line_2_3.addWidget(btn_unpin_note)
line_2_4.addWidget(btn_search_tag)

m_line2.addLayout(line_2_3)
m_line2.addLayout(line_2_4)

m_layout.addLayout(m_line1)
m_layout.addLayout(m_line2)


btn_create_note.clicked.connect(add_note)
notes_list.itemClicked.connect(show_note)
btn_save_note.clicked.connect(save_note)
btn_delete_note.clicked.connect(delete_note)
btn_pin_note.clicked.connect(add_tag)
btn_unpin_note.clicked.connect(delete_tag)
btn_search_tag.clicked.connect(search_tag)

with open('notes_data.json', 'r') as file:
    notes = json.load(file)
notes_list.addItems(notes)

mw.setLayout(m_layout)
mw.show()
app.exec_()