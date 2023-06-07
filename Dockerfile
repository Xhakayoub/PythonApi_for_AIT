# Utilise une image de base appropriée pour ton application
FROM python:3.9

# Installe les dépendances système nécessaires (y compris dbus-1)
RUN apt-get update && apt-get install -y dbus libdbus-1-dev gettext

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de ton application dans le conteneur
COPY . /app

# Installe les dépendances de ton application
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port sur lequel ton application écoute
EXPOSE 8080

# Définit la commande par défaut pour exécuter ton application
CMD ["python", "script.py"]