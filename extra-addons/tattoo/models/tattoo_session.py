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
        ('pagata', 'Pagata')], 'Stato della sessione', default='fissata',
        store=True)
    client_id = fields.Many2one('res.partner', string='Cliente')
    tattoo_artist_ids = fields.Many2many('res.users', string='Tatuatore')
    session_date = fields.Datetime(string="Data Sessione",
                                   required=True,
                                   default=datetime.datetime.now())
    design_id = fields.Many2one('tattoo.design', string='Disegno')
    duration = fields.Float(string="Durata Necessaria", related='design_id.time')
    session_cost = fields.Float(string="Costo della sessione", compute="_compute_session_cost")
    design_cost = fields.Float(related='design_id.price')


    @api.depends('design_cost', 'tattoo_artist_ids', 'duration')
    def _compute_session_cost(self):
        for record in self:
            try:
                # design_id = self.env['tattoo.design'].browse(record.design_id.id)
                artist_cost = 0
                for artist in record.tattoo_artist_ids:
                    artist_cost += artist.hour_cost * record.duration
                record.session_cost = record.design_cost + artist_cost
            except:
                pass

    # ACTIONS BUTTONS
    def cancel_session(self):
        for record in self:
            record.state = "annullata"
        return True

    def in_corso_session(self):
        for record in self:
            record.state = "in_corso"
        return True

    def finita_session(self):
        for record in self:
            record.state = "finita"
        return True

    def pagata_session(self):
        for record in self:
            record.state = "pagata"
        return True

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append(
                (record.id, str(record.client_id.name) + ' - ' + str(record.design_id.name) + ' - ' + str(record.session_date)))
        return res
