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
    tattoo_artist_ids = fields.Many2many('res.users', string='Tatuatore')
    session_date = fields.Datetime(string="Data Sessione",
                                   required=True,
                                   default=datetime.datetime.now())
    design_id = fields.Many2one('tattoo.design', string='Disegno')
    duration = fields.Float(string="Durata Necessaria", compute="_compute_duration")
    session_cost = fields.Float(string="Costo della sessione", compute="_compute_session_cost")

    @api.depends('design_id')
    def _compute_duration(self):
        for record in self:
            try:
                design_id = self.env['tattoo.design'].browse(record.design_id.id)
                record.duration = design_id.time
            except:
                pass

    @api.depends('design_id','tattoo_artist_ids')
    def _compute_duration(self):
        for record in self:
            try:
                design_id = self.env['tattoo.design'].browse(record.design_id.id)
                artist_cost = 0
                for artist in record.tattoo_artist_ids:
                    artist_cost += artist.hour_cost * design_id.time
                record.session_cost = design_id.price + artist_cost
            except:
                pass
