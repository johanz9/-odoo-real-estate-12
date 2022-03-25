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
    appointment_ids = fields.Many2many('tattoo.appointment', string='Appuntamenti')
    session_date = fields.Datetime(string="Data Sessione",
                                   required=True,
                                   default=datetime.datetime.now())
    design_id = fields.Many2one('tattoo.design', string='Disegno')
    duration = fields.Float(string="Durata Necessaria", related='design_id.time')
    session_cost = fields.Float(string="Costo della sessione", compute="_compute_session_cost")
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
        return True

    def in_corso_session(self):
        for record in self:
            record.state = "in_corso"
        return True

    def finita_session(self):
        for record in self:
            record.state = "finita"

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
        return True

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append(
                (record.id,
                 str(record.client_id.name) + ' - ' + str(record.design_id.name) + ' - ' + str(record.session_date)))
        return res


class MyModuleMessageWizard(models.TransientModel):
    _name = 'mymodule.message.wizard'
    _description = "Show Message"

    message = fields.Text('Message', required=True)

    @api.multi
    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}
