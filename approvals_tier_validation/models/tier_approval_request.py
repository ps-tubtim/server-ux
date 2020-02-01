# Copyright 2020 Ecosoft Co., Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from ast import literal_eval
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TierApprovalRequest(models.Model):
    _name = 'tier.approval.request'
    _description = 'Approval Request'
    _inherit = ["tier.validation",
                "mail.thread", "mail.activity.mixin"]
    _state_from = ["pending"]
    _state_to = ["approved"]

    name = fields.Char(string="Approval Subject", tracking=True)
    category_id = fields.Many2one('tier.approval.category', string="Category", required=True, readonly=True, )
    request_owner_id = fields.Many2one('res.users', string="Request Owner")
    attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')
    date_confirmed = fields.Datetime(string="Date Confirmed")
    require_document = fields.Selection(related="category_id.require_document")
    state = fields.Selection([
        ('new', 'New'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('cancel', 'Cancel')], default="new", tracking=True, )
    reference_model = fields.Selection(
        string="Reference Type",
        selection="_selection_target_model",
        related="category_id.reference_model", )
    reference_rec = fields.Reference(
        string="Reference Record",
        selection="_selection_target_model", )
    rec_action_id = fields.Many2one(
        comodel_name="ir.actions.act_window",
        related="category_id.rec_action_id", )
    rec_view_id = fields.Many2one(
        comodel_name="ir.ui.view",
        related="category_id.rec_view_id", )

    @api.constrains("reference_rec", "state")
    def _check_reference_rec(self):
        for request in self:
            if not request.reference_model and request.reference_rec:
                raise UserError(_("Reference record should be nothing"))
            if request.reference_model and request.state == "pending":
                if not request.reference_rec:
                    raise UserError(_("Please create reference record first"))
                if request.reference_rec._name != request.reference_model:
                    raise UserError(_("Reference Record is of the wrong type"))

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]

    def _compute_attachment_number(self):
        domain = [('res_model', '=', 'tier.approval.request'), ('res_id', 'in', self.ids)]
        attachment_data = self.env['ir.attachment'].read_group(domain, ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for request in self:
            request.attachment_number = attachment.get(request.id, 0)

    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'tier.approval.request'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'tier.approval.request', 'default_res_id': self.id}
        return res

    def action_confirm(self):
        if self.require_document == 'required' and not self.attachment_number:
            raise UserError(_("You have to attach at least one document."))
        self.write({'state': 'pending', 'date_confirmed': fields.Datetime.now()})

    def action_approve(self, approver=None):
        self.write({'state': 'approved'})

    def action_refuse(self, approver=None):
        self.write({'state': 'refused'})

    def action_withdraw(self, approver=None):
        self.write({'state': 'pending'})

    def action_draft(self):
        self.write({'state': 'new'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def create_reference_rec(self):
        self.ensure_one()
        ctx = {'request_reference_model': self.reference_model}
        # Default action
        result = {
            'type': 'ir.actions.act_window',
            'name': _('Create Ref. Record'),
            'res_model': self.reference_model,
            'view_mode': 'form',
            'context': ctx,
        }
        if self.rec_action_id:
            action = self.env.ref(self.rec_action_id.xml_id)
            result = action.read()[0]
            action_context = literal_eval(result['context'])
            result["view_mode"] = "form"
            result['context'] = {**action_context, **ctx}
        if self.rec_view_id:
            view = (self.rec_view_id.id, self.rec_view_id.name)
            result["view_id"] = view
            result["views"] = []
        return result
