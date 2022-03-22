from odoo import fields, models

WEEK_DAYS = [
    ('lunedi', 'Lunedi'),
    ('martedi', 'Martedi'),
    ('mercoledi', 'Mercoledi'),
    ('giovedi', 'Giovedi'),
    ('venerdi', 'Venerdi'),
    ('sabato', 'Sabato'),
    ('domenica', 'Domenica'),
]


class TattooArtistHours(models.Model):
    _name = "tattoo.artist.hours"
    _description = "Tattoo Artist's Hours"
    _order = 'id desc'

    day = fields.Selection(string='Giorno di lavoro', selection=WEEK_DAYS, default="lunedi", required=True)
    start_hour_01 = fields.Float(string="Orario inizio primo turno", required=True)
    end_hour_01 = fields.Float(string="Orario fine primo turno", required=True)
    start_hour_02 = fields.Float(string="Orario inizio secondo turno")
    end_hour_02 = fields.Float(string="Orario fine secondo turno")
    tattoo_artist_id = client_id = fields.Many2one('res.users', string='Tatuatore',
                                                   default=lambda self: self.env.uid)
    sequence = fields.Integer('Sequence', default=1, help="Used to order hours. Lower is better.")


