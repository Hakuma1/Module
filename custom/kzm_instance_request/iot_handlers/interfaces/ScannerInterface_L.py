# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from cups import Connection as cups_connection
from re import sub
from usb import core
from threading import Lock
import subprocess
import logging

from odoo.addons.hw_drivers.interface import Interface

_logger = logging.getLogger(__name__)

conn = cups_connection()
cups_lock = Lock()  # _logger.debug("")We can only make one call to Cups at a time

class ScannerInterface(Interface):
    _loop_delay = 120
    connection_type = 'scanner_printer'

    def get_devices(self):
        """
        USB devices are identified by a combination of their `idVendor` and
        `idProduct`. We can't be sure this combination in unique per equipment.
        To still allow connecting multiple similar equipments, we complete the
        identifier by a counter. The drawbacks are we can't be sure the equipments
        will get the same identifiers after a reboot or a disconnect/reconnect.
        """
        usb_devices = {}
        devs = core.find(find_all=True)
        cpt = 2
        print("devs666666", devs)
        _logger.debug("device------------>ScannerInterface111", devs)
        for dev in devs:
            identifier = "usb_%04x:%04x" % (dev.idVendor, dev.idProduct)
            if identifier in usb_devices:
                identifier += '_%s' % cpt
                cpt += 1
            usb_devices[identifier] = dev
        print("usb_devices666666", usb_devices)
        return usb_devices

    """def get_devices(self):
        discovered_devices = {}
        try:
            with cups_lock:
                # Utiliser scanimage pour lister les scanners disponibles
                output = subprocess.check_output(['scanimage', '-L']).decode('utf-8')
                for line in output.splitlines():
                    # Identifier le scanner spécifique
                    if 'HP ScanJet Pro 2600 f1' in line:
                        device_info = {
                            'name': 'HP ScanJet Pro 2600 f1',
                            'type': 'scanner',
                            'id': self.get_identifier(line),
                            'uri': line.split()[0]  # Assurez-vous que l'URI est correctement extrait
                        }
                        discovered_devices[device_info['id']] = device_info
        except subprocess.CalledProcessError as e:
            _logger.error("Erreur lors de la récupération des périphériques: %s", e)

        # Gérer les périphériques qui sont dans la liste mais qui n'ont pas été trouvés lors de cet appel
        for device in list(self.scanner_devices):
            if not discovered_devices.get(device):
                disconnect_counter = self.scanner_devices.get(device).get('disconnect_counter', 0)
                if disconnect_counter >= 2:
                    self.scanner_devices.pop(device, None)
                else:
                    self.scanner_devices[device].update({'disconnect_counter': disconnect_counter + 1})

        self.scanner_devices.update(discovered_devices)
        print("dict(self.scanner_devices)", dict(self.scanner_devices))
        return dict(self.scanner_devices)

    def get_identifier(self, path):
        # Ici, vous pouvez ajuster cette méthode pour obtenir un identifiant unique
        if 'uuid=' in path:
            identifier = sub('[^a-zA-Z0-9_]', '', path.split('uuid=')[1])
        elif 'serial=' in path:
            identifier = sub('[^a-zA-Z0-9_]', '', path.split('serial=')[1])
        else:
            identifier = sub('[^a-zA-Z0-9_]', '', path)
        return identifier"""
