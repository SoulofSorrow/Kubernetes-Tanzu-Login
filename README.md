# Tanzu Login Dienstprogramm

Dieses Python-Programm bietet eine grafische Benutzeroberfläche (GUI) für den Tanzu-Login-Prozess. Tanzu ist ein Kubernetes-Verwaltungstool von VMware, und dieses Dienstprogramm vereinfacht das Anmelden und Verwalten von Tanzu-Clustern.

## Funktionen
- **Anmelden:** Ermöglicht das Anmelden an einem Tanzu-Cluster mit Benutzername und Passwort.
- **Kubeconfig Löschen:** Bietet die Möglichkeit, das lokale `.kube`-Verzeichnis zu löschen.

## Voraussetzungen
- Python 3.x
- PyQt5 für die GUI
- `config.yaml`-Datei für die Tanzu-Konfigurationen
- **kubectl:** Das Kubernetes-Befehlszeilentool `kubectl` muss im System installiert sein.

## Verwendung
1. Das Programm zeigt eine Liste von Tanzu-Konfigurationsdateien (`config.yaml`) an, aus denen der Benutzer einen TNS-Namen auswählen kann.
2. Der Benutzer wählt einen TNS-Namen und einen Cluster-Namen aus.
3. Das Passwort wird sicher eingegeben und als Umgebungsvariable (`KUBECTL_VSPHERE_PASSWORD`) festgelegt.
4. Ein Kubernetes-Anmelde-Befehl wird generiert und ausgeführt, um sich am Tanzu-Cluster anzumelden.
5. Nach erfolgreichem Anmelden wird das Passwort aus den Umgebungsvariablen entfernt.

## Anleitung
1. Stellen Sie sicher, dass Sie `Python 3.x` und `PyQt5` installiert haben, um die GUI zu verwenden.
2. Erstellen Sie eine `config.yaml`-Datei mit Ihren Tanzu-Konfigurationen.
3. Installieren Sie `kubectl` auf Ihrem System, wenn es noch nicht vorhanden ist.
4. Führen Sie das Programm aus, wählen Sie einen TNS-Namen aus und geben Sie Ihre Anmeldeinformationen ein.

**Hinweis:** Dieses Dienstprogramm wurde für die Verwendung mit VMware Tanzu entwickelt und erfordert Tanzu-Konfigurationsdateien sowie einen gültigen Benutzernamen und ein Passwort.

