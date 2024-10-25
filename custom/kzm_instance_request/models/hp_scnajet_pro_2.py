from odoo.addons.hw_drivers.driver import Driver
import subprocess

class HPScanJetPro2600Driver(Driver):
    connection_type = 'USB'

    def __init__(self, identifier, device):
        super(HPScanJetPro2600Driver, self).__init__(identifier, device)
        self.device_type = 'scanner'
        self.device_name = 'HP ScanJet Pro 2600 f1'

    @classmethod
    def supported(cls, device):
        return 'HP ScanJet Pro 2600 f1' in device.get('name', '')

    def scan_document(self, output_file='/opt/odoo16/Custom_MC_Module/custom/kzm_instance_request/data/scanned_image.png'):
        # Utilisation de scanimage pour numériser via l'interface eSCL.
        cmd = [
            'scanimage',
            '-d', 'airscan:e1:HP ScanJet Pro 2600 f1 (USB)',
            '--format=png',
            '--output-file', output_file
        ]
        subprocess.run(cmd, check=True)
        return output_file
