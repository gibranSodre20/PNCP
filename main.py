import sys
import os
import Usuario
import Unidade
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QButtonGroup, QFileDialog, QCheckBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt


class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Cadastro e Consulta")
        self.setGeometry(100, 100, 700, 650)

        layout = QVBoxLayout()

        # ---- CAMPOS DE LOGIN, SENHA E ID ----
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Digite o login")

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Digite a senha")
        self.senha_input.setEchoMode(QLineEdit.Password)

        # ---- CHECKBOX PARA SALVAR LOGIN E SENHA ----
        self.salvar_login_check = QCheckBox("Salvar login e senha")

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Digite o ID do usuário")

        layout.addWidget(QLabel("Login:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Senha:"))
        layout.addWidget(self.senha_input)
        layout.addWidget(self.salvar_login_check)
        layout.addWidget(QLabel("ID Usuário:"))
        layout.addWidget(self.id_input)

        # ---- CARREGAR LOGIN/SENHA SALVOS ----
        self.carregar_credenciais()

        # ---- RADIO BUTTONS ----
        self.radio_consultar = QRadioButton("Consultar usuário")
        self.radio_cadastrar = QRadioButton("Cadastrar entes e unidades")
        self.radio_consultar.setChecked(True)

        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.radio_consultar)
        self.radio_group.addButton(self.radio_cadastrar)

        layout.addWidget(QLabel("Selecione a ação:"))
        layout.addWidget(self.radio_consultar)
        layout.addWidget(self.radio_cadastrar)

        # ---- CHECKBOXES ----
        self.check_ente = QCheckBox("Cadastrar Ente autorizado")
        self.check_unidade = QCheckBox("Cadastrar Unidades")
        self.check_ente.setVisible(False)
        self.check_unidade.setVisible(False)

        layout.addWidget(self.check_ente)
        layout.addWidget(self.check_unidade)

        # ---- UPLOAD DE CSV ----
        self.upload_btn = QPushButton("Selecionar arquivo CSV")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: bold;
                
            }
            QPushButton:hover { background-color: #005fa3; }
        """)
        self.upload_btn.clicked.connect(self.selecionar_csv)
        self.csv_label = QLabel("Nenhum arquivo selecionado")

        layout.addWidget(QLabel("Upload de arquivo CSV:"))
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.csv_label)

        # ---- BOTÃO DE AÇÃO ----
        self.acao_btn = QPushButton("Executar ação")
        self.acao_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        self.acao_btn.clicked.connect(self.executar_acao)
        layout.addWidget(self.acao_btn)

        # ---- TABELA CONSULTA ----
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(1)
        self.tabela.setHorizontalHeaderLabels(["Entes não cadastrados para o usuário informado."])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setFixedHeight(200)

        self.limpar_btn = QPushButton("Limpar tabela de consulta")
        self.limpar_btn.clicked.connect(self.limpar_tabela)
        self.limpar_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #b02a37; }
        """)

        # ---- TABELA CADASTRO ----
        self.tabela_cadastro = QTableWidget()
        self.tabela_cadastro.setColumnCount(2)
        self.tabela_cadastro.setHorizontalHeaderLabels(["Tipo", "Mensagem"])
        self.tabela_cadastro.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_cadastro.setFixedHeight(300)
        self.tabela_cadastro.setVisible(False)

        self.limpar_btn_cadastro = QPushButton("Limpar tabela de cadastro")
        self.limpar_btn_cadastro.clicked.connect(self.limpar_tabela_cadastro)
        self.limpar_btn_cadastro.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #b02a37; }
        """)
        self.limpar_btn_cadastro.setVisible(False)

        # ---- ADICIONAR AO LAYOUT ----
        layout.addWidget(self.tabela)
        layout.addWidget(self.limpar_btn)
        layout.addWidget(self.tabela_cadastro)
        layout.addWidget(self.limpar_btn_cadastro)

        # ---- CONECTAR RADIO BUTTONS ----
        self.radio_cadastrar.toggled.connect(self.atualizar_visibilidade)
        self.radio_consultar.toggled.connect(self.atualizar_visibilidade)

        self.atualizar_visibilidade()
        self.setLayout(layout)

    # -------------------- FUNÇÕES AUXILIARES --------------------

    def carregar_credenciais(self):
        """Carrega login e senha salvos (se existirem)."""
        if os.path.exists("credenciais.txt"):
            with open("credenciais.txt", "r", encoding="utf-8") as f:
                dados = f.read().splitlines()
                if len(dados) >= 2:
                    self.login_input.setText(dados[0])
                    self.senha_input.setText(dados[1])
                    self.salvar_login_check.setChecked(True)

    def salvar_credenciais(self, login, senha):
        """Salva login e senha em arquivo, se marcado."""
        if self.salvar_login_check.isChecked():
            with open("credenciais.txt", "w", encoding="utf-8") as f:
                f.write(f"{login}\n{senha}")
        elif os.path.exists("credenciais.txt"):
            os.remove("credenciais.txt")

    def atualizar_visibilidade(self):
        """Exibe ou oculta elementos conforme o radio button selecionado."""
        if self.radio_cadastrar.isChecked():
            self.check_ente.setVisible(True)
            self.check_unidade.setVisible(True)
            self.tabela.setVisible(False)
            self.limpar_btn.setVisible(False)
            self.tabela_cadastro.setVisible(True)
            self.limpar_btn_cadastro.setVisible(True)
        else:
            self.check_ente.setVisible(False)
            self.check_unidade.setVisible(False)
            self.tabela.setVisible(True)
            self.limpar_btn.setVisible(True)
            self.tabela_cadastro.setVisible(False)
            self.limpar_btn_cadastro.setVisible(False)

    def selecionar_csv(self):
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo CSV", "", "Arquivos CSV (*.csv)")
        if arquivo:
            self.csv_label.setText(arquivo)

    def executar_acao(self):
        login = self.login_input.text().strip()
        senha = self.senha_input.text().strip()
        id_usuario = self.id_input.text().strip()
        arquivo_csv = self.csv_label.text().strip()
        cadastrar_ente = self.check_ente.isChecked()
        cadastrar_unidade = self.check_unidade.isChecked()
        cadastrarEntesUnidades = self.radio_cadastrar.isChecked()
        consultarUsuario = self.radio_consultar.isChecked()
        # ---- Validação obrigatória ----
        if not login or not senha:
            QMessageBox.warning(self, "Campos obrigatórios", "Os campos de login e senha são obrigatórios!")
            return
        
        if cadastrar_ente or consultarUsuario:
            if not id_usuario:
                QMessageBox.warning(self, "Campos obrigatórios", "O campo ID Usuário é obrigatório!")
                return
        if cadastrar_unidade or consultarUsuario:
            if arquivo_csv == "Nenhum arquivo selecionado":
                QMessageBox.warning(self, "Campos obrigatórios", "O arquivo .CSV é obrigatório!")
                return
        
        if cadastrarEntesUnidades and not cadastrar_unidade and not cadastrar_ente:
            QMessageBox.warning(self, "Campos obrigatórios", "É obrigatório selecionar pelo menos uma opção (Cadastrar Unidades ou Cadastrar Ente autorizado).")
            return

        # ---- Salvar credenciais, se solicitado ----
        self.salvar_credenciais(login, senha)

        # ---- Execução ----
        if self.radio_cadastrar.isChecked():
            resultado = Unidade.cadastarEntesUnidades(id_usuario, arquivo_csv, cadastrar_ente, cadastrar_unidade, login, senha)
            self.preencher_tabela_cadastro(resultado)
        else:
            resultado = Usuario.consultarUsuario(id_usuario, arquivo_csv, login, senha)
            self.preencher_tabela_consulta(resultado)

        print("\n--- Resultado da Ação ---")
        print(resultado)

    def preencher_tabela_consulta(self, resultado):
        if isinstance(resultado, list):
            self.tabela.setRowCount(len(resultado))
            for i, cnpj in enumerate(resultado):
                self.tabela.setItem(i, 0, QTableWidgetItem(str(cnpj)))
        else:
            self.tabela.setRowCount(1)
            self.tabela.setItem(0, 0, QTableWidgetItem(str(resultado)))

    def preencher_tabela_cadastro(self, resultado):
        if isinstance(resultado, list):
            self.tabela_cadastro.setRowCount(len(resultado))
            for i, linha in enumerate(resultado):
                tipo = linha.get("tipo", "—") if isinstance(linha, dict) else "Resultado"
                msg = linha.get("mensagem", str(linha)) if isinstance(linha, dict) else str(linha)
                self.tabela_cadastro.setItem(i, 0, QTableWidgetItem(tipo))
                self.tabela_cadastro.setItem(i, 1, QTableWidgetItem(msg))
        else:
            self.tabela_cadastro.setRowCount(1)
            self.tabela_cadastro.setItem(0, 0, QTableWidgetItem("Resultado"))
            self.tabela_cadastro.setItem(0, 1, QTableWidgetItem(str(resultado)))

    def limpar_tabela(self):
        self.tabela.setRowCount(0)
        self.id_input.clear()
        self.csv_label.clear()

    def limpar_tabela_cadastro(self):
        self.tabela_cadastro.setRowCount(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
