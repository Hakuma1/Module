import time
import logging
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


def start_odoo_server(start_command):
    try:
        logging.info("Starting Odoo server...")
        return_code = os.system(start_command)
        if return_code == 0:
            print("Commande exécutée avec succès.")
            logging.info("Serveur lancé avec succès")
        else:
            print("Erreur lors de l'exécution de la commande.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start Odoo server with error: {e.stderr}")


class CustomEventHandler(FileSystemEventHandler):
    def __init__(self, file_extensions, the_stop_command, the_start_command, delay, the_sudo_password):
        self.file_extensions = file_extensions
        self.stop_command = the_stop_command
        self.start_command = the_start_command
        self.delay = delay
        self.sudo_password = the_sudo_password
        print("self.sudo_password", self.sudo_password)
        print("self.sudo_password", len(self.sudo_password))

    def _execute_command(self, event_type, src_path):
        logging.info(f"{event_type} file: {src_path}")
        time.sleep(self.delay)
        try:
            logging.info("Stopping Odoo server...")
            command = ["sudo", "-S", "kill"]

            ps_process = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
            grep_process = subprocess.Popen(["grep", "odoo"], stdin=ps_process.stdout, stdout=subprocess.PIPE)
            awk_process = subprocess.Popen(["awk", "{print $2}"], stdin=grep_process.stdout, stdout=subprocess.PIPE)
            ps_process.stdout.close()
            pid_output = awk_process.communicate()[0]

            command.extend(pid_output.decode().split())

            kill_result = subprocess.run(command, input=self.sudo_password, capture_output=True, text=True)
            if kill_result.returncode == 0:
                print("Commande exécutée avec succès.")
                print("Sortie de la commande stop")
                logging.info("Serveur arrêté avec succès")
            else:
                print("Erreur lors de l'exécution de la commande.")
                print("Erreur:", kill_result.stderr)

            odoo_thread = threading.Thread(target=start_odoo_server, args=(self.start_command,))
            odoo_thread.start()

        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed with error: {e.stderr}")

    def _is_watched_extension(self, src_path):
        result = any(src_path.endswith(ext) for ext in self.file_extensions)
        return result

    def on_modified(self, event):
        if not event.is_directory and self._is_watched_extension(event.src_path):
            logging.info(f"Modified file: {event.src_path}")
            self._execute_command(event, event.src_path)

    def on_created(self, event):
        if not event.is_directory and self._is_watched_extension(event.src_path):
            logging.info(f"Created file: {event.src_path}")
            self._execute_command(event, event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and self._is_watched_extension(event.src_path):
            logging.info(f"Deleted file: {event.src_path}")
            self._execute_command(event, event.src_path)


class OnWatchFile:
    def __init__(self, directory, extensions, the_start_command, delay, the_sudo_password):
        self.directory = directory
        self.file_extensions = extensions
        self.stop_command = 'kill $(ps aux | grep odoo | awk \'{print $2}\')'
        self.start_command = the_start_command
        self.delay = delay
        self.sudo_password = the_sudo_password
        self.observer = Observer()

    def run(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        event_handler = CustomEventHandler(self.file_extensions, self.stop_command, self.start_command, self.delay,
                                           self.sudo_password)
        self.observer.schedule(event_handler, self.directory, recursive=True)

        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


if __name__ == '__main__':
    sudo_password = '    '
    start_command = ('/home/mckarizma/Documents/Environnements/odoo_envs/odoo15_env_secours/bin/python3.8 '
                     '/opt/odoo15/odoo-server/odoo-bin -c /etc/odoo15-perla.conf -d Perla_Prod -u kzm_hr_etats_9421,'
                     'perla_hr,perla_budget,perla_hr_budget,perla_purchase')
    watch = OnWatchFile("./custom/addons/PERLA", ['.py', '.xml', '.csv', '.po', '.js', '.css', '.scss'],
                        start_command, 10, sudo_password)
    watch.run()
