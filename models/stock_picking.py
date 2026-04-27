# -*- coding: utf-8 -*-

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_purchase_order_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase',
            'view_mode': 'list',
            'res_model': 'purchase.order',
            'domain': [('name', '=', self.origin)],
            'context': "{'create': False}"
        }
