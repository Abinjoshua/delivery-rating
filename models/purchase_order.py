# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    delivery_rating = fields.Integer(string='Delivery Rating',compute="_compute_delivery_rating")

    @api.depends("date_planned")
    def _compute_delivery_rating(self):
        for record in self:
            # po_delivery = self.env['stock.picking'].search([('origin', '=', record.name), ('state', '=', 'done')],limit=1)
            po_delivery = record.picking_ids.filtered(
                lambda x: x.state == 'done'
            )
            po_delivery_date = po_delivery.date_done
            if po_delivery_date:
                if record.date_planned.date() >= po_delivery_date.date():
                    record.delivery_rating = 5
                else:
                    diff = po_delivery_date.date() - record.date_planned.date()
                    if 1 <= diff.days <= 2:
                        record.delivery_rating = 4
                    elif 3 <= diff.days <= 5:
                        record.delivery_rating = 3
                    elif 6 <= diff.days <= 10:
                        record.delivery_rating = 2
                    elif diff.days > 10:
                        record.delivery_rating = 1
            else:
                record.delivery_rating = 0


    def button_confirm(self):
        res = super().button_confirm()
        p_line = self.partner_id.purchase_line_ids.mapped('order_id')
        current_vendor_po = p_line.filtered(
            lambda x:x.state == 'purchase'
        )
        cus_ratings = current_vendor_po.mapped('delivery_rating')
        for po in current_vendor_po:
            if po.delivery_rating:
                cus_ratings.append(po.delivery_rating)
        if cus_ratings:
            cus_avg_ratings = sum(cus_ratings) / len(cus_ratings)
            if 0 < cus_avg_ratings < 2:
                raise ValidationError('Customer rating is too low')
        return res
