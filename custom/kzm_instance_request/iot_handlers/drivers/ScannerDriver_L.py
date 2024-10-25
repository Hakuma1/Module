import base64

from odoo.addons.hw_drivers.driver import Driver
import logging
from odoo.addons.hw_drivers.main import iot_devices

_logger = logging.getLogger(__name__)
from usb import util
import re
from odoo import http, _
import json
import io
import subprocess
import xmlrpc.client
db = 'test_2'
username = 'admin'
password = 'admin'


class ScannerPrinterDriver(Driver):
    connection_type = 'scanner_printer'

    def __init__(self, identifier, device):
        super(ScannerPrinterDriver, self).__init__(identifier, device)
        self.device_connection = 'direct'
        self.device_type = 'document_scanner'
        self.device_name = self._set_name()
        self._actions.update({
            'action_mc_mc': self.action_mc_mc,
        })
        print("device------------>ScannerPrinterDriver111", device)
        _logger.debug("device.get('identifier') MC==== %s" % device)


    @classmethod
    def supported(cls, device):
        """
        Vérifie si le driver supporte un scanner HP ScanJet Pro, en particulier le 2600 f1.
        """
        if device.idVendor == 0x03f0:
            _logger.info(f"Scanner HP ScanJet Pro 2600 f1 détecté : {device}")
            return True
        else:
            _logger.info(f"Périphérique non supporté : {device.idVendor}:{device.idProduct}")
            return False

    def _set_name(self):
        try:
            manufacturer = util.get_string(self.dev, self.dev.iManufacturer)
            product = util.get_string(self.dev, self.dev.iProduct)
            return re.sub(r"[^\w \-+/*&]", '', "%s - %s" % (manufacturer, product))
        except ValueError as e:
            _logger.warning(e)
            return _('Unknown input device')

    def action_mc_mc(self, data):
        dict_string = json.dumps(data)


        scanned_image = self.scan_document()  # Récupérer les données scannées

        """pdf_data = img2pdf.convert(scanned_image.getvalue())

                Encoder les données PDF en base64 pour les envoyer au client
                pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')"""

        # Encoder les données en base64 pour les envoyer au client
        image_data_base64 = base64.b64encode(scanned_image.getvalue()).decode('utf-8')

        url = data['url']

        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})

        success = False
        if uid:
            models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            update_data = {
                'scanned_file': image_data_base64,
            }

            success = models.execute_kw(db, uid, password,
                                        data['model'],
                                        'write',
                                        [[data['the_id']], update_data])
        # Ouvrir le fichier en mode ajout et écrire la chaîne dans le fichier
        with open('/tmp/mamady_camara.txt', 'a', encoding='utf-8') as f:
            f.write(dict_string + '\n')
            f.write(success + '\n')
        return {
            'success': True,
            'image_data': 'MAMADY'
        }



    def scan_document(self):
        """Numériser un document et retourner les données d'image sous forme de variable."""
        cmd = [
            'scanimage',
            '-d', 'airscan:e1:HP ScanJet Pro 2600 f1 (USB)',
            '--format=png'
        ]

        scan_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        scanned_image_data, error = scan_process.communicate()

        if scan_process.returncode != 0:
            _logger.error("Erreur lors de la numérisation: %s", error.decode('utf-8'))
            raise subprocess.CalledProcessError(scan_process.returncode, cmd)

        return io.BytesIO(scanned_image_data)

    #2 def action_mc_mc(self, data):
    #     print("Hello world", data)
    #     _logger.debug("Hello world: %s", data)
    #     _logger.info("Hello world: %s", data)
    #     scanned_image = self.scan_document()  # Récupérer les données scannées
    #
    #     # Encoder les données en base64 pour les envoyer au client
    #     image_data_base64 = base64.b64encode(scanned_image.getvalue()).decode('utf-8')
    #
    #     return {
    #         'success': True,
    #         'image_data': image_data_base64
    #     }
    #
    # def scan_document(self):
    #     """Numériser un document et retourner les données d'image sous forme de variable."""
    #     cmd = [
    #         'scanimage',
    #         '-d', 'airscan:e1:HP ScanJet Pro 2600 f1 (USB)',
    #         '--format=png'
    #     ]
    #
    #     scan_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     scanned_image_data, error = scan_process.communicate()
    #
    #     if scan_process.returncode != 0:
    #         _logger.error("Erreur lors de la numérisation: %s", error.decode('utf-8'))
    #         raise subprocess.CalledProcessError(scan_process.returncode, cmd)
    #
    #     return io.BytesIO(scanned_image_data)

    #1 def action_mc_mc(self, data):
    #     print("Hello world", data)
    #     _logger.debug("Hello world" % data)
    #     _logger.info("Hello world" % data)
    #     return self.scan_document()
    #
    # def scan_document(self):
    #     """Numériser un document et retourner les données d'image sous forme de variable."""
    #     # Commande pour numériser via l'interface eSCL.
    #     cmd = [
    #         'scanimage',
    #         '-d', 'airscan:e1:HP ScanJet Pro 2600 f1 (USB)',
    #         '--format=png'
    #     ]
    #
    #     # Utiliser un sous-processus pour numériser
    #     scan_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #
    #     # Récupérer les données scannées
    #     scanned_image_data, error = scan_process.communicate()
    #
    #     if scan_process.returncode != 0:
    #         raise subprocess.CalledProcessError(scan_process.returncode, cmd)
    #
    #     # Retourner les données sous forme de variable
    #     return io.BytesIO(scanned_image_data)


    """def scan_document(self, output_file='/opt/odoo16/Custom_MC_Module/custom/kzm_instance_request/data/scanned_image.png'):
        # Utilisation de scanimage pour numériser via l'interface eSCL.
        cmd = [
            'scanimage',
            '-d', 'airscan:e1:HP ScanJet Pro 2600 f1 (USB)',
            '--format=png',
            '--output-file', output_file
        ]
        subprocess.run(cmd, check=True)
        return output_file"""



    """def scan_document(self, remote_user='mckarizma', remote_host='ubuntu20king',
                      remote_path='/mamady/scanned_image.png'):
        # Commande complète à exécuter
        command = f"scanimage -d 'airscan:e1:HP ScanJet Pro 2600 f1 (USB)' --format=png | ssh {remote_user}@{remote_host} 'cat > {remote_path}'"

        try:
            # Exécute la commande complète
            result = subprocess.run(command, shell=True, check=True, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Vérifiez la sortie et les erreurs
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout,
                                                    stderr=result.stderr)

        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de la commande : {e.cmd}")
            print(f"Code de retour : {e.returncode}")
            print(f"Sortie : {e.output}")
            print(f"Erreur : {e.stderr}")
            return None  # Indique une erreur lors du traitement

        return remote_path  # Retourne le chemin sur le serveur distant"""








