from odoo import models, fields, api, exceptions
import datetime
import logging

WEEK_DAYS = ['', 'lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica']
_logger = logging.getLogger(__name__)


def check_artist_hours(self, vals):
    if "appointment_date" in vals:
        appointment_date = vals["appointment_date"]
    else:
        appointment_date = self.appointment_date

    if "tattoo_artist_id" in vals:
        tattoo_artist_id = vals["tattoo_artist_id"]
    else:
        tattoo_artist_id = self.tattoo_artist_id.id

    if isinstance(appointment_date, datetime.datetime):
        date = appointment_date
    else:
        date = datetime.datetime.strptime(appointment_date, "%Y-%m-%d %H:%M:%S")

    day_name = WEEK_DAYS[date.weekday() + 1]
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

    state = fields.Selection([
        ('fissato', 'Fissato'),
        ('annullato', 'Annullato'),
        ('mancato', 'Mancato'),
        ('rispettato', 'Rispettato')], "Stato dell'appuntamento", default='fissato',
        store=True)
    appointment_date = fields.Datetime(string="Data Appuntamento",
                                       required=True,
                                       default=datetime.datetime.now())
    tattoo_artist_id = fields.Many2one('res.users', string='Tatuatore',
                                       default=lambda self: self.env.uid)
    client_id = fields.Many2one('res.partner', string='Cliente', compute="_get_client_id", store=True)

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            if record.client_id.name:
                res.append(
                    (record.id,
                     str(record.client_id.name) + ' - ' + str(record.appointment_date)))
            else:
                res.append(
                    (record.id,
                     'No client selected' + ' - ' + str(record.appointment_date)))

            return res

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
        appointment = super(TattooAppointment, self).create(vals)

        artist_id = vals["tattoo_artist_id"]

        artist_appointment = self.env['tattoo.appointment'].search(
            [('tattoo_artist_id', '=', artist_id), ('state', '=', 'fissato')])

        if len(artist_appointment.ids) >= 2:
            raise exceptions.UserError('Il tatuatore non può avere più di un '
                                       'appuntamento fissato')

        check_artist_hours(self, vals)

        # check if client_id is not empty
        if appointment.client_id.create_date != False:
            client_id = appointment.client_id.id
            artist_id = vals["tattoo_artist_id"]

            # it return a list with two id, first id -> current appointment, second id -> another appointment
            # if it return a list of ids, then it mean that the client have another appointment fixed
            client_appointment = self.env['tattoo.appointment'].search(
                [('client_id', '=', client_id), ('state', '=', 'fissato')])

            if len(client_appointment.ids) >= 2:
                raise exceptions.UserError('Il cliente non può avere più di un '
                                           'appuntamento fissato')

        return appointment

    @api.multi
    def write(self, vals):

        check_artist_hours(self, vals)

        if "tattoo_artist_id" in vals:
            artist_id = vals["tattoo_artist_id"]
            artist_appointment = self.env['tattoo.appointment'].search(
                [('tattoo_artist_id', '=', artist_id), ('state', '=', 'fissato')])

            if artist_appointment.state == "fissato":
                raise exceptions.UserError('Il tatuatore non può avere più di un '
                                           'appuntamento fissato')

        if "session_ids" in vals:
            # vals[session_id] -> [6, false, [9]], 9 -> session_id
            session_ids = self.env['tattoo.session'].browse(vals["session_ids"][0][2])
            for session in session_ids:

                client_appointment = self.env['tattoo.appointment'].search(
                    [('client_id', '=', session.client_id.id), ('state', '=', 'fissato')])

                if client_appointment.state == "fissato" and client_appointment.id != self.id:
                    raise exceptions.UserError('Il cliente non può avere più di un '
                                               'appuntamento fissato')

        return super(TattooAppointment, self).write(vals)
