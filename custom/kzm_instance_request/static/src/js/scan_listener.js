odoo.define('your_module.scan_listener', function (require) {
    var DeviceProxy = require('iot.DeviceProxy');
    var rpc = require('web.rpc');

    // Fonction appelée lorsqu'on clique sur le bouton Scan
    function scan_document(invoice_id) {
        // IP de l'IoT Box et identifiant du scanner
        var iot_ip = '192.168.31.7';
        var device_identifier = 'usb_03f0:6105';

        var iot_device = new DeviceProxy({
            iot_ip: iot_ip,
            identifier: device_identifier
        });

        // Ajouter un listener pour écouter le retour du fichier scanné
        iot_device.add_listener(function (result) {
            if (result.status === 'success') {
                // Envoyer le fichier scanné au serveur Odoo
                rpc.query({
                    model: 'account.move',
                    method: 'write',
                    args: [[invoice_id], {
                        'scanned_file': result.file,
                        'scanned_filename': 'scanned_document.pdf'
                    }]
                }).then(function () {
                    alert("Le document a été scanné et ajouté avec succès.");
                });
            } else {
                alert("Erreur lors du scan : " + result.error);
            }
        });

        // Envoyer la commande de scan
        iot_device.action({
            action: 'scan_document',
            file_type: 'pdf'
        });
    }

    return {
        scan_document: scan_document
    };
});
