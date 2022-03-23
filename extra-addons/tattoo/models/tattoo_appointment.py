from odoo import models, fields, api, exceptions
import datetime


# the client only can have one fixed appointment
def client_only_one_appointment(self, vals):
    # add artist to session
    try:
        for session in vals["session_ids"]:
            for id in session[2]:
                self.env.cr.execute(
                    "INSERT INTO res_users_tattoo_session_rel(tattoo_session_id, res_users_id) VALUES({}, {})".format(
                        id, vals["tattoo_artist_id"]))
    except:
        raise exceptions.UserError('Il cliente non può avere più di un '
                                   'appuntamento fissato')


def artist_only_one_appointment(self, vals):
    artist_appointment = self.env['tattoo.appointment'].search(
        [('tattoo_artist_id', '=', vals["tattoo_artist_id"]), ('state', '=', 'fissato')])

    if artist_appointment.state == "fissato":
        raise exceptions.UserError('Il tatuatore non può avere più di un '
                                   'appuntamento fissato')


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
    client_id = fields.Many2one('res.partner', string='Cliente', compute="_get_client_id", store=True)

    @api.depends("session_ids")
    def _get_client_id(self):
        for record in self:
            if len(record.session_ids) != 0:
                client_id = record.session_ids[0].client_id
                for session in record.session_ids:
                    if client_id != session.client_id:
                        raise exceptions.UserError('Can only add a session of the same client')

                record.client_id = client_id

    def cancel_appointment(self):
        for record in self:
            record.state = "annullato"

        return True

    # button action missed
    def missed_appointment(self):
        for record in self:
            record.state = "mancato"
        return True

    def respected_appointment(self):
        for record in self:
            record.state = "rispettato"
        return True

    @api.model
    def create(self, vals):

        # search if the client have a appointment in state "fissato" return a record
        # client_appointment = self.env['tattoo.appointment'].search(
        #     [('client_id', '=', vals["client_id"]), ('state', '=', 'fissato')])
        #
        # if client_appointment.state == "fissato":
        #     raise exceptions.UserError('Il cliente non può avere più di un '
        #                                'appuntamento fissato')

        artist_only_one_appointment(self, vals)

        client_only_one_appointment(self, vals)


    @api.multi
    def write(self, vals):
        """Override default Odoo write function and extend."""
        artist_only_one_appointment(self, vals)
        client_only_one_appointment(self, vals)

        return super(TattooAppointment, self).write(vals)
