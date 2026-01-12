import sys
import subprocess
import yaml
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QInputDialog, QMessageBox, QTextEdit, QLineEdit, QDialog, QVBoxLayout, QDialogButtonBox

class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Benutzername und Passwort eingeben')
        self.setGeometry(200, 200, 400, 150)

        layout = QVBoxLayout()

        self.label_username = QLabel('Benutzername:')
        self.username_input = QLineEdit(self)
        layout.addWidget(self.label_username)
        layout.addWidget(self.username_input)

        self.label_password = QLabel('Passwort:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.password_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

class TanzuLoginUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tanzu Login')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Bitte wähle eine Aktion:')
        layout.addWidget(self.label)

        self.login_button = QPushButton('1) Login')
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.delete_button = QPushButton('2) Kubeconfig löschen')
        self.delete_button.clicked.connect(self.delete_kubeconfig)
        layout.addWidget(self.delete_button)

        self.text_output = QTextEdit()
        layout.addWidget(self.text_output)

        self.setLayout(layout)

    def clear_output(self):
        self.text_output.clear()

    def display_message(self, message):
        self.text_output.append(message)
        print(message)

    def login(self):
        self.clear_output()
        self.display_message("Tanzu Login")
        self.display_message("---------------------------------\n")

        try:
            cluster_config = load_cluster_config()
            self.display_message("Konfigurationsdatei geladen.")
        except FileNotFoundError:
            self.display_message("Fehler: Konfigurationsdatei nicht gefunden.")
            return

        try:
            tns_name = select_tns_name(cluster_config)
            self.display_message(f"Ausgewählter TNS-Name: {tns_name}")
        except ValueError:
            self.display_message("Fehler: Ungültige Auswahl.")
            return

        try:
            server = cluster_config[tns_name]["server"]
            self.display_message(f"Server für TNS '{tns_name}' gefunden.")
        except KeyError:
            self.display_message(f"Fehler: Server für TNS '{tns_name}' nicht gefunden.")
            return

        password_dialog = PasswordDialog()
        result = password_dialog.exec_()
        if result == QDialog.Accepted:
            username = password_dialog.username_input.text()
            password = password_dialog.password_input.text()
            self.display_message(f"Benutzername: {username}")

            # Setze das Passwort als Systemvariable
            os.environ['KUBECTL_VSPHERE_PASSWORD'] = password
            self.display_message("Passwort als Systemvariable gesetzt.")

        else:
            self.display_message("Aborted!")
            return

        try:
            cluster_name = select_cluster_name(cluster_config, tns_name)
            self.display_message(f"Ausgewählter Cluster-Name: {cluster_name}")
        except ValueError:
            self.display_message("Fehler: Ungültige Auswahl.")
            return

        login_command = generate_login_command(server, username, tns_name, cluster_name)
        self.display_message("Login-Befehl generiert: " + login_command)

        try:
            subprocess.run(login_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            self.display_message("Erfolgreich eingeloggt!")

            # Lösche das Passwort aus den Systemvariablen nach erfolgreichem Login
            if 'KUBECTL_VSPHERE_PASSWORD' in os.environ:
                del os.environ['KUBECTL_VSPHERE_PASSWORD']
                self.display_message("Passwort aus Systemvariablen gelöscht.")
                app.quit()  # Schließe das Programm, wenn die Variable geleert ist

        except subprocess.CalledProcessError as e:
            error_message = f"Fehler: Login fehlgeschlagen. Fehlermeldung: {e.stderr}"
            self.display_message(error_message)
            print(error_message)

        self.clear_output()

    def delete_kubeconfig(self):
        self.clear_output()
        confirm = QMessageBox.question(self, 'Bestätigung', 'Bist du sicher, dass du das .kube-Verzeichnis löschen möchtest?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            kubeconfig_path = os.path.expanduser("~/.kube")
            try:
                subprocess.run(["rm", "-rf", kubeconfig_path])
                success_message = f"Das .kube-Verzeichnis ({kubeconfig_path}) wurde erfolgreich gelöscht."
                self.display_message(success_message)
                print(success_message)
            except subprocess.CalledProcessError:
                error_message = "Fehler: Löschen des .kube-Verzeichnisses fehlgeschlagen."
                self.display_message(error_message)
                print(error_message)
        else:
            self.display_message("Löschvorgang abgebrochen.")

def load_cluster_config():
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
    with open(config_file) as f:
        config = yaml.safe_load(f)
    return config

def select_tns_name(cluster_config):
    tns_names = list(cluster_config.keys())
    tns_name, okPressed = QInputDialog.getItem(None, "TNS-Namen auswählen", "Bitte wähle den TNS-Namen:", tns_names, 0, False)
    if not okPressed:
        raise ValueError("Ungültige Auswahl.")
    return tns_name

def select_cluster_name(cluster_config, tns_name):
    cluster_names = cluster_config[tns_name]["cluster_names"]
    cluster_name, okPressed = QInputDialog.getItem(None, "Cluster-Namen auswählen", "Bitte wähle den Cluster-Namen:", cluster_names, 0, False)
    if not okPressed:
        raise ValueError("Ungültige Auswahl.")
    return cluster_name

def generate_login_command(server, username, tns_name, cluster_name):
    login_command = f"kubectl-vsphere login --server {server} --vsphere-username {username}@<domain> --insecure-skip-tls-verify --tanzu-kubernetes-cluster-namespace {tns_name} --tanzu-kubernetes-cluster-name {cluster_name}"
    return login_command

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TanzuLoginUI()
    window.show()
    sys.exit(app.exec_())
