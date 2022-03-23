from odoo import models, fields, api, exceptions
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
    appointment_date = fields.Datetime(string="Data Appuntamento",
                                       required=True,
                                       default=datetime.datetime.now())
    tattoo_artist_id = client_id = fields.Many2one('res.users', string='Tatuatore',
                                                   default=lambda self: self.env.uid)
    client_id = fields.Many2one('res.partner', string='Cliente')

    def cancel_appointment(self):
        for record in self:
            record.state = "annullato"

        return True

    @api.model
    def create(self, vals):
        # search if the client have a appointment in state "fissato" return a record
        client_appointment = self.env['tattoo.appointment'].search(
            [('client_id', '=', vals["client_id"]), ('state', '=', 'fissato')])

        if client_appointment.state == "fissato":
            raise exceptions.UserError('Il cliente non può avere più di un '
                                       'appuntamento fissato')

        artist_appointment = self.env['tattoo.appointment'].search(
            [('tattoo_artist_id', '=', vals["tattoo_artist_id"]), ('state', '=', 'fissato')])

        if artist_appointment.state == "fissato":
            raise exceptions.UserError('Il tatuatore non può avere più di un '
                                       'appuntamento fissato')

        # add artist to session
        for session in vals["session_ids"]:
            for id in session[2]:
                self.env.cr.execute(
                    "INSERT INTO res_users_tattoo_session_rel(tattoo_session_id, res_users_id) VALUES({}, {})".format(
                        id, vals["tattoo_artist_id"]))

        return super().create(vals)
