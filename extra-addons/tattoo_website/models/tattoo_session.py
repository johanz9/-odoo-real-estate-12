from odoo import models, fields, api, exceptions


class TattooSession(models.Model):
    _inherit = ['tattoo.session']
    user_id = fields.Many2one('res.users')

