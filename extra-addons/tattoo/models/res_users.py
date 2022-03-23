from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    tattoo_artist_hours_ids = fields.One2many("tattoo.artist.hours", "tattoo_artist_id", string="Orari di lavoro")
    hour_cost = fields.Float(string="Costo orario")
    last_name = fields.Char(string="Last Name")





