from odoo import models, fields, api, exceptions
import datetime

WEEK_DAYS = ['', 'lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica']


# the client only can have one fixed appointment
def client_only_one_appointment(self, vals):
    if "state" not in vals:
        if "tattoo_artist_id" in vals:
            artist_id = vals["tattoo_artist_id"]
        else:
            artist_id = self.tattoo_artist_id.id

        if "client_id" in vals:
            client_id = vals["client_id"]
            session_ids = vals["session_ids"]
        else:
            client_id = self.client_id.id
            session_ids = self.session_ids

        client_appointment = self.env['tattoo.appointment'].search(
            [('client_id', '=', client_id), ('state', '=', 'fissato')])

        if client_appointment.state == "Fissato":
            raise exceptions.UserError('Il cliente non può avere più di un '
                                       'appuntamento fissato')
        else:
            # TODO check it
            for session in vals["client_id"]:
                for id in session[2]:
                    self.env.cr.execute(
                        "INSERT INTO res_users_tattoo_session_rel(tattoo_session_id, res_users_id) VALUES({}, {})".format(
                            id, artist_id))

        # add artist to session
        # try:
        #     for session in vals["session_ids"]:
        #         for id in session[2]:
        #             self.env.cr.execute(
        #                 "INSERT INTO res_users_tattoo_session_rel(tattoo_session_id, res_users_id) VALUES({}, {})".format(
        #                     id, artist_id))
        # except:
        #     raise exceptions.UserError('Il cliente non può avere più di un '
        #                                'appuntamento fissato')


def artist_only_one_appointment(self, vals):
    if "tattoo_artist_id" in vals:
        artist_id = vals["tattoo_artist_id"]
    else:
        artist_id = self.tattoo_artist_id.id

    artist_appointment = self.env['tattoo.appointment'].search(
        [('tattoo_artist_id', '=', artist_id), ('state', '=', 'fissato')])

    if artist_appointment.state == "fissato":
        raise exceptions.UserError('Il tatuatore non può avere più di un '
                                   'appuntamento fissato')


def check_artist_hours(self, vals):
    if "appointment_date" in vals:
        appointment_date = vals["appointment_date"]
    else:
        appointment_date = self.appointment_date

    if "tattoo_artist_id" in vals:
        tattoo_artist_id = vals["tattoo_artist_id"]
    else:
        tattoo_artist_id = self.tattoo_artist_id.id

    date = datetime.datetime.strptime(appointment_date, "%Y-%m-%d %H:%M:%S")
    day_name = WEEK_DAYS[date.weekday()]
    artist_hour = self.env['tattoo.artist.hours'].search(
        [('tattoo_artist_id', '=', tattoo_artist_id), ('day', '=', day_name)])

    # check if the artist_hour is empty
    if artist_hour.create_date != False:
        start_hour_01 = str(datetime.timedelta(hours=artist_hour.start_hour_01)).rsplit(':', 1)[0]
        start_hour_01 = start_hour_01.split(":")
        end_hour_01 = str(datetime.timedelta(hours=artist_hour.end_hour_01)).rsplit(':', 1)[0]
        end_hour_01 = end_hour_01.split(":")

        start_hour_02 = str(datetime.timedelta(hours=artist_hour.start_hour_02)).rsplit(':', 1)[0]
        start_hour_02 = start_hour_02.split(":")
        end_hour_02 = str(datetime.timedelta(hours=artist_hour.end_hour_02)).rsplit(':', 1)[0]
        end_hour_02 = end_hour_02.split(":")

        if datetime.time(int(start_hour_01[0]), int(start_hour_01[1])) <= date.time() <= datetime.time(
                int(end_hour_01[0]), int(end_hour_01[1])):
            pass
        elif artist_hour.has_second_hour:
            if datetime.time(int(start_hour_02[0]), int(start_hour_02[1])) <= date.time() <= datetime.time(
                    int(end_hour_02[0]), int(end_hour_02[1])):
                pass
            else:
                raise exceptions.UserError(
                    'Il tatuattore questo giorno puo lavorare solo: {} - {} e {} - {}'.format(
                        str(datetime.timedelta(hours=artist_hour.start_hour_01)).rsplit(':', 1)[0],
                        str(datetime.timedelta(hours=artist_hour.end_hour_01)).rsplit(':', 1)[0],
                        str(datetime.timedelta(hours=artist_hour.start_hour_02)).rsplit(':', 1)[0],
                        str(datetime.timedelta(hours=artist_hour.end_hour_02)).rsplit(':', 1)[0]))
        else:
            raise exceptions.UserError(
                'Il tatuattore questo giorno puo lavorare solo: {} - {}'.format(
                    str(datetime.timedelta(hours=artist_hour.start_hour_01)).rsplit(':', 1)[0],
                    str(datetime.timedelta(hours=artist_hour.end_hour_01)).rsplit(':', 1)[0]))
    else:
        raise exceptions.UserError('Il tatuatore non ha orari in questa data')


class TattooAppointment(models.Model):
    _name = 'tattoo.appointment'
    _description = "Tattoo Appointment"
    _order = 'id desc'

    session_ids = fields.Many2many('tattoo.session', string='Sessioni')
    # session_ids = fields.Many2many(
    #     'tattoo.session', 'res_users_tattoo_session_rel', 'client_id', 'session_id', string='Sessioni')
    #

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
        # if "client_id" in vals:
        #     client_appointment = self.env['tattoo.appointment'].search(
        #         [('client_id', '=', vals["client_id"]), ('state', '=', 'fissato')])
        #
        #     if client_appointment.state == "fissato":
        #         raise exceptions.UserError('Il cliente non può avere più di un '
        #                                    'appuntamento fissato')

        # artist_only_one_appointment(self, vals)

        date = datetime.datetime.strptime(vals["appointment_date"], "%Y-%m-%d %H:%M:%S")
        day_name = WEEK_DAYS[date.weekday()]

        artist_hour = self.env['tattoo.artist.hours'].search(
            [('tattoo_artist_id', '=', vals["tattoo_artist_id"]), ('day', '=', day_name)])

        # check if the artist_hour is empty
        check_artist_hours(self, vals)

        return super().create(vals)

    @api.multi
    def write(self, vals):
        """Override default Odoo write function and extend."""
        # artist_only_one_appointment(self, vals)
        # TODO check artist hours
        check_artist_hours(self, vals)

        # client_only_one_appointment(self, vals)

        return super(TattooAppointment, self).write(vals)
