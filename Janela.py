import sys
import Unidade
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QCheckBox,
    QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt


class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface de Upload CSV")
        self.setFixedSize(400, 420)
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        # Campo de Login
        self.label_login = QLabel("Login:")
        self.input_login = QLineEdit()
        layout_principal.addWidget(self.label_login)
        layout_principal.addWidget(self.input_login)

        # Campo de Senha
        self.label_senha = QLabel("Senha:")
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.Password)
        layout_principal.addWidget(self.label_senha)
        layout_principal.addWidget(self.input_senha)

        # Campo de ID
        self.label_id = QLabel("ID:")
        self.input_id = QLineEdit()
        layout_principal.addWidget(self.label_id)
        layout_principal.addWidget(self.input_id)

        # Campo de Arquivo CSV
        self.label_csv = QLabel("Arquivo CSV:")
        layout_principal.addWidget(self.label_csv)

        csv_layout = QHBoxLayout()
        self.input_csv = QLineEdit()
        self.botao_csv = QPushButton("Selecionar")
        self.botao_csv.clicked.connect(self.selecionar_csv)
        csv_layout.addWidget(self.input_csv)
        csv_layout.addWidget(self.botao_csv)
        layout_principal.addLayout(csv_layout)

        # --- Novos Checkboxes ---
        self.checkbox_consultar = QCheckBox("Consultar ente autorizado")
        self.checkbox_cadastrar_ente = QCheckBox("Cadastrar ente autorizado")
        self.checkbox_cadastrar_unidades = QCheckBox("Cadastrar unidades")

        layout_principal.addSpacing(10)
        layout_principal.addWidget(QLabel("Ações disponíveis:"))
        layout_principal.addWidget(self.checkbox_consultar)
        layout_principal.addWidget(self.checkbox_cadastrar_ente)
        layout_principal.addWidget(self.checkbox_cadastrar_unidades)
        layout_principal.addSpacing(10)

        # Botão de Ação
        self.botao_acao = QPushButton("Executar Ação")
        self.botao_acao.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.botao_acao.clicked.connect(self.executar_acao)
        layout_principal.addWidget(self.botao_acao, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)

    def selecionar_csv(self):
        """Abre o seletor de arquivo para escolher o CSV."""
        arquivo, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo CSV", "", "Arquivos CSV (*.csv);;Todos os arquivos (*)"
        )
        if arquivo:
            self.input_csv.setText(arquivo)

    def executar_acao(self):
        """Executa a ação do botão."""
        login = self.input_login.text().strip()
        senha = self.input_senha.text().strip()
        id_usuario = self.input_id.text().strip()
        arquivo_csv = self.input_csv.text().strip()

        if not all([login, senha, id_usuario, arquivo_csv]):
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos e selecione um arquivo CSV.")
            return

        # Verifica os checkboxes
        acoes = []
        if self.checkbox_consultar.isChecked():
            acoes.append("Consultar ente autorizado")
        if self.checkbox_cadastrar_ente.isChecked():
            acoes.append("Cadastrar ente autorizado")
        if self.checkbox_cadastrar_unidades.isChecked():
            acoes.append(Unidade.inserirUnidade('1231', '123','teste','1234', arquivo_csv))

        if not acoes:
            acoes.append("Nenhuma ação marcada")

        QMessageBox.information(
            self,
            "Sucesso",
            f"Ação executada com sucesso!\n\n"
            f"Login: {login}\nID: {id_usuario}\nArquivo: {arquivo_csv}\n\n"
            f"Ações selecionadas:\n- " + "\n- ".join(acoes)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
