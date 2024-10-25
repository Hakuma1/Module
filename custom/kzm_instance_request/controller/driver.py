# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from base64 import b64decode
import json
import logging
import os
import subprocess
import time

from odoo import http, tools
from odoo.modules.module import get_resource_path

from odoo.addons.hw_drivers.event_manager import event_manager
from odoo.addons.hw_drivers.main import iot_devices, manager
from odoo.addons.hw_drivers.tools import helpers

_logger = logging.getLogger(__name__)


class DocumentScannerController(http.Controller):

    @http.route('/hw_drivers/action', type='json', auth='none', cors='*', csrf=False, save_session=False)
    def action(self, session_id, device_identifier, data):
        """
        This route is called when we want to make a action with device (take picture, printing,...)
        We specify in data from which session_id that action is called
        And call the action of specific device
        """
        iot_device = iot_devices.get(device_identifier)
        if iot_device:
            iot_device.data['owner'] = session_id
            data = json.loads(data)

            # Skip the request if it was already executed (duplicated action calls)
            print("data Hercule1", data)
            _logger.debug("Hello world Hercule1" % data)
            _logger.info("Hello world Hercule2" % data)
            iot_device.action(data)
            return True
        return False
