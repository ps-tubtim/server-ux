# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, tools


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        reference_model = self._context.get("request_reference_model", False)
        active_model = self._context.get("active_model", False)
        active_id = self._context.get("active_id", False)
        if self._name == reference_model and \
                active_model == "tier.approval.request" and active_id:
            request = self.env[active_model].browse(active_id)
            request.write({"reference_rec": "%s,%s" % (self._name, rec.id)})
        return rec
