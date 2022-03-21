import datetime
from odoo import models, fields, api


class TattooSession(models.Model):
    _name = 'tattoo.session'
    _description = "Tattoo Session"
    _order = 'id desc'

    state = fields.Selection([
        ('fissata', 'Fissata'),
        ('annullata', 'Annullata'),
        ('in_corso', 'In Corso'),
        ('finita', 'Finata'),
        ('Pagata', 'Pagata')], 'Stato della sessione', default='fissata',
        store=True)

    client_id = fields.Many2one('res.partner', string='Cliente')
    session_date = fields.Date(string="Data Sessione",
                               required=True,
                               default=datetime.datetime.now().date())
