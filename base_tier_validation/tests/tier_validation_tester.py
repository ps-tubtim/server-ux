# Copyright 2018-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TierValidationTester(models.Model):
    _name = "tier.validation.tester"
    _description = "Tier Validation Tester"
    _inherit = ["tier.validation"]

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("cancel", "Cancel"),
        ],
        default="draft",
    )
    test_field = fields.Float()
    user_id = fields.Many2one(string="Assigned to:", comodel_name="res.users")
    test_bool = fields.Boolean()

    def action_confirm(self):
        self.write({"state": "confirmed"})

    def _get_under_validation_exceptions(self):
        return super()._get_under_validation_exceptions() + ["test_bool"]


class TierValidationTester2(models.Model):
    _name = "tier.validation.tester2"
    _description = "Tier Validation Tester 2"
    _inherit = ["tier.validation"]

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("cancel", "Cancel"),
        ],
        default="draft",
    )
    test_field = fields.Float()
    user_id = fields.Many2one(string="Assigned to:", comodel_name="res.users")

    def action_confirm(self):
        self.write({"state": "confirmed"})
