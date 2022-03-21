from odoo import models, fields, api
import datetime


class TattooAppointment(models.Model):
    _name = 'tattoo.appointment'
    _description = "Tattoo Appointment"
    _order = 'id desc'

    session_ids = fields.Many2many('tattoo.session', string='Sessioni')
    state = fields.Selection([
        ('fissato', 'Fissato'),
        ('annullato', 'Annullato'),
        ('mancato', 'Mancato'),
        ('rispettato', 'Rispettato')], "Stato dell'appuntamento", default='fissato',
        store=True)
    appointment_date = fields.Date(string="Data Appuntamento",
                                   required=True,
                                   default=datetime.datetime.now().date())
