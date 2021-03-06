import datetime
from odoo import models, fields, api, exceptions

STATE = [
    ('fissata', 'Fissata'),
    ('annullata', 'Annullata'),
    ('in_corso', 'In Corso'),
    ('finita', 'Finata'),
    ('pagata', 'Pagata')
]


class TattooSession(models.Model):
    _name = 'tattoo.session'
    _description = "Tattoo Session"
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection(STATE, 'Stato della sessione', default='fissata',
        store=True)
    client_id = fields.Many2one('res.partner', string='Cliente')
    appointment_ids = fields.Many2many('tattoo.appointment', string='Appuntamenti')
    design_id = fields.Many2one('tattoo.design', string='Disegno')
    duration = fields.Float(string="Durata Necessaria", related='design_id.time')
    session_cost = fields.Float(string="Costo della sessione", compute="_compute_session_cost", store=True)
    design_cost = fields.Float(related='design_id.price')
    same_design_count = fields.Integer(string="Numero di questo tatuaggio", compute="_compute_same_design")

    @api.depends('design_cost', 'appointment_ids', 'duration')
    def _compute_session_cost(self):
        for record in self:
            artist_cost = 0
            for appointment in record.appointment_ids:
                artist_cost += appointment.tattoo_artist_id.hour_cost * record.duration
            record.session_cost = record.design_cost + artist_cost

    @api.depends('design_id')
    def _compute_same_design(self):
        for record in self:
            count = self.env['tattoo.session'].search_count(
                [('design_id', '=', record.design_id.id), ('client_id', '=', record.client_id.id)])
            record.same_design_count = count

    # ACTIONS BUTTONS
    def cancel_session(self):
        for record in self:
            record.state = "annullata"
            status = ""
            for state in STATE:
                if state[0] == record.state:
                    status = state[1]
            body = "Lo stato della sezione è <strong>{}</strong> in data {}".format(status,
                                                                                    datetime.datetime.now().date())
            record.message_post(body=body)
        return True

    def in_corso_session(self):
        for record in self:
            record.state = "in_corso"
            status = ""
            for state in STATE:
                if state[0] == record.state:
                    status = state[1]
            body = "Lo stato della sezione è <strong>{}</strong> in data {}".format(status, datetime.datetime.now().date())
            record.message_post(body=body)
        return True

    def finita_session(self):
        for record in self:
            record.state = "finita"

            status = ""
            for state in STATE:
                if state[0] == record.state:
                    status = state[1]
            body = "Lo stato della sezione è <strong>{}</strong> in data {}".format(status,
                                                                                    datetime.datetime.now().date())
            record.message_post(body=body)

            message_id = self.env['mymodule.message.wizard'].create(
                {'message': 'Il cambio dello stato della sessione è stato completato con successo'})
            return {
                'name': 'Message',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard',
                'res_id': message_id.id,
                'target': 'new'
            }
        return True

    def pagata_session(self):
        for record in self:
            record.state = "pagata"
            status = ""
            for state in STATE:
                if state[0] == record.state:
                    status = state[1]
            body = "Lo stato della sezione è <strong>{}</strong> in data {}".format(status,
                                                                                    datetime.datetime.now().date())
            record.message_post(body=body)
        return True

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append(
                (record.id,
                 str(record.client_id.name) + ' - ' + str(record.design_id.name)))
        return res

    @api.model
    def create(self, vals):

        if self.env.user.has_group('tattoo.tattoo_group_client'):
            vals["client_id"] = self.env.user.partner_id.id
        return super().create(vals)

    @api.multi
    def unlink(self):
        for record in self:
            if record.state not in ['fissata', 'annullata']:
                raise exceptions.UserError('Non si può eliminare una session in corso, finita o pagata')
        return super(TattooSession, self).unlink()


class MyModuleMessageWizard(models.TransientModel):
    _name = 'mymodule.message.wizard'
    _description = "Show Message"

    message = fields.Text('Message', required=True)

    @api.multi
    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}
