# Copyright 2020 Ecosoft Co., Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from odoo import fields, models, api
from odoo.modules.module import get_module_resource


class TierApprovalCategory(models.Model):
    _name = 'tier.approval.category'
    _description = 'Tier Approval Category'
    _order = 'sequence'

    def _get_default_image(self):
        default_image_path = get_module_resource(
            'approvals', 'static/src/img', 'clipboard-check-solid.svg')
        return base64.b64encode(open(default_image_path, 'rb').read())

    name = fields.Char(string="Name", translate=True, required=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(string="Sequence")
    description = fields.Char(string="Description", translate=True)
    image = fields.Binary(string='Image', default=_get_default_image)
    require_document = fields.Selection([('required', 'Required'), ('optional', 'Optional')], string="Documents", default="optional", required=True)
    request_to_validate_count = fields.Integer("Number of requests to validate", compute="_compute_request_to_validate_count")
    reference_model = fields.Selection(
        string='Reference Model', selection='_selection_target_model')
    rec_action_id = fields.Many2one(
        string="Window Action",
        comodel_name="ir.actions.act_window",
        domain="[('res_model', '=', reference_model)]")
    rec_view_id = fields.Many2one(
        string="Form View",
        comodel_name="ir.ui.view",
        domain="[('model', '=', reference_model), ('type', '=', 'form')]")

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]

    def _compute_request_to_validate_count(self):
        for category in self:
            category.request_to_validate_count = 1000

    # def _compute_request_to_validate_count(self):
    #     domain = [('request_status', '=', 'pending'), ('approver_ids.user_id', '=', self.env.user.id)]
    #     requests_data = self.env['approval.request'].read_group(domain, ['category_id'], ['category_id'])
    #     requests_mapped_data = dict((data['category_id'][0], data['category_id_count']) for data in requests_data)
    #     for category in self:
    #         category.request_to_validate_count = requests_mapped_data.get(category.id, 0)

    def create_request(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "tier.approval.request",
            "views": [[False, "form"]],
            "context": {
                'form_view_initial_mode': 'edit',
                'default_name': self.name,
                'default_category_id': self.id,
                'default_request_owner_id': self.env.user.id,
                'default_state': 'new'
            },
        }
