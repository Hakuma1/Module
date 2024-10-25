# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, _, api

class IotDevice(models.Model):
    _inherit = 'iot.device'

    type = fields.Selection(selection_add=[("document_scanner", "Document Scanner")])


class Order(models.Model):
    """ Order """
    _inherit = 'sale.order'

    version_odoo_id = fields.Many2one(comodel_name="odoo.version", string="Id odoo version")

    def open_wizard(self):
        action = self.env.ref('kzm_instance_request.purchase_order_action').read()[0]
        return action

class AccountMove(models.Model):
    _inherit = 'account.move'

    scanned_file = fields.Binary("Scanned File", attachment=True)
    filename = fields.Char()
    iot_id = fields.Many2one('iot.box')
    device_id = fields.Many2one('iot.device')

    def print_something(self):
        print("Ça marche mamady")

    def action_call_js(self):
        """Cette méthode sera appelée quand on clique sur le bouton."""
        return {
            'type': 'ir.actions.client',
            'tag': 'your_custom_js_action',
            'params': {
                'message': 'Message from Python to JS!',
                'the_id': self.id
            },
        }

    # def action_scan_document(self):
    #     """
    #     Méthode déclenchée par le bouton pour scanner un document.
    #     Elle envoie une commande à l'IoT Box et récupère le fichier scanné.
    #     """
    #     # Spécifiez l'adresse IP de votre IoT Box
    #     iot_ip = '192.168.0.10'  # Remplacez par l'adresse IP de votre IoT Box
    #     device_identifier = 'usb_03f0:1e0d'  # Identifiant du scanner HP ScanJet Pro 2600 F1
    #
    #     # Instancier un proxy IoTDevice pour communiquer avec le scanner
    #     iot_device = IoTDevice(iot_ip, device_identifier)
    #
    #     # Envoyer la commande de scan au scanner
    #     action_data = {
    #         'action': 'scan_document',
    #         'file_type': 'pdf',  # Format du fichier à scanner (peut être 'jpeg', 'png', etc.)
    #     }
    #
    #     result = iot_device.action(action_data)
    #
    #     if result.get('status') == 'success':
    #         # Mettre à jour la facture avec le fichier scanné
    #         scanned_file_content = result.get('file')
    #         self.write({
    #             'scanned_file': scanned_file_content,
    #             'scanned_filename': 'scanned_document.pdf',  # Nom par défaut du fichier scanné
    #         })
    #     else:
    #         raise UserError(_("Erreur de scan: %s" % result.get('error')))
