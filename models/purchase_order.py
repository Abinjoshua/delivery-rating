# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    delivery_rating = fields.Integer(string='Delivery Rating',compute="_compute_delivery_rating")

    @api.depends("date_planned","delivery_rating")
    def _compute_delivery_rating(self):
        po_delivery = self.env['stock.picking'].search([('origin', '=', self.name), ('state', '=', 'assigned')])
        po_delivery_date = po_delivery.date_done
        if po_delivery_date:
            if self.date_planned.day >= po_delivery_date.day:
                self.delivery_rating = 5
            else:
                diff = po_delivery_date - self.date_planned
                if 1 <= diff.days <= 2:
                    self.delivery_rating = 4
                elif 3 <= diff.days <= 5:
                    self.delivery_rating = 3
                elif 6 <= diff.days <= 10:
                    self.delivery_rating = 2
                elif diff.days > 10:
                    self.delivery_rating = 1
        else:
            self.delivery_rating = None

    #
    # def button_confirm(self):
    #     print('w')
    #     res = super().button_confirm()
    #     current_vendor_po = self.env['purchase.order'].search([('partner_id', '=', self.partner_id),('state','=','purchase')])
    #     print(current_vendor_po)
    #     cus_ratings = []
    #     for po in current_vendor_po:
    #         cus_ratings.append(int(po.delivery_rating))
    #         cus_avg_ratings = sum(cus_ratings) / len(cus_ratings)
    #         print('Customer avg',cus_avg_ratings)
    #         if 0 > cus_avg_ratings < 2:
    #             raise ValidationError('Customer rating is too low')
    #         else:
    #             self.write({'state': 'purchase'})
    #     return res
