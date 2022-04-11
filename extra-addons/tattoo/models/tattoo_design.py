import datetime
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError, AccessError


class TattooDesign(models.Model):
    _name = 'tattoo.design'
    _description = "Tattoo Design"
    _order = 'id desc'

    name = fields.Char(string="Nome del disegno", required=True)
    time = fields.Float(string='Tempo di esecuzione (in ore)')
    material_ids = fields.Many2many('tattoo.design.material', string='Materiali')
    additional_cost = fields.Float(string="Costo Adizionale")
    price = fields.Float(string="Costo tattuaggio", compute="_compute_price", readonly=True)
    image_01 = fields.Binary("Prima Immagine", help="Select image here", attachment=True)
    image_02 = fields.Binary("Seconda Immagine", help="Select image here", attachment=True)
    session_ids = fields.One2many("tattoo.session", "design_id")
    session_finita_ids = fields.One2many("tattoo.session", "design_id", string="Sessioni Finiti",
                                         compute="_compute_session")

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The design name must be unique'),
    ]

    @api.depends('additional_cost', "material_ids")
    @api.one
    def _compute_price(self):

        for record in self:
            material_price_sum = 0
            for material in self.material_ids:
                material_price_sum += material.price

            record.price = record.additional_cost + material_price_sum

    @api.depends('session_ids')
    def _compute_session(self):
        new_ids = self.session_ids.filtered(lambda t: t.state == 'finita')
        # result = self.session_ids.read_group([("state", "=", "finita")], fields=['client_id'],
        #                                      groupby=['client_id'])

        client_id_list = []
        session_id_list = []
        # search session_id, get the client_id and add session if the client_id is not into client_id_list
        # in this way i can onlye get one session by client
        for session in new_ids.ids:
            session_id = self.env['tattoo.session'].browse(session)
            if session_id.client_id not in client_id_list:
                session_id_list.append(session)
                client_id_list.append(session_id.client_id)

        self.session_finita_ids = session_id_list

    @api.model
    def create(self, values):

        # Security controls
        if self.env.user.has_group('tattoo.tattoo_group_artist') or self.env.user.has_group(
                'tattoo.tattoo_group_manager'):
            # check if the user is in group billing
            try:
                self.check_access_rights('create')
            except AccessError:
                raise UserError(_("You don't have the access rights needed to create a design"))
        else:
            raise UserError(_("You arent in one of the following groups: artist or manager"))

        return super(TattooDesign, self).create(values)

    @api.multi
    def write(self, vals):

        if self.env.user.has_group('tattoo.tattoo_group_artist') or self.env.user.has_group(
                'tattoo.tattoo_group_manager'):
            # check if the user is in group billing
            try:
                self.check_access_rights('write')
            except AccessError:
                raise UserError(_("You don't have the access rights needed to update a design"))
        else:
            raise UserError(_("You arent in one of the following groups: artist or manager"))

        return super(TattooDesign, self).write(vals)


class TattooDesignMaterial(models.Model):
    _name = 'tattoo.design.material'
    _description = "Tattoo Design Material"
    _order = 'id desc'

    name = fields.Char(string="Nome del Materiale", required=True)
    price = fields.Float(string="Prezzo del materiale", required=True)

    @api.model
    def create(self, values):

        # Security controls
        if self.env.user.has_group('tattoo.tattoo_group_manager'):
            # check if the user is in group billing
            try:
                self.check_access_rights('create')
            except AccessError:
                raise UserError(_("You don't have the access rights needed to create a design"))
        else:
            raise UserError(_("You arent in one of the following groups: artist or manager"))

        return super(TattooDesignMaterial, self).create(values)

    @api.multi
    def write(self, vals):

        if self.env.user.has_group('tattoo.tattoo_group_manager'):
            # check if the user is in group billing
            try:
                self.check_access_rights('write')
            except AccessError:
                raise UserError(_("You don't have the access rights needed to update a design"))
        else:
            raise UserError(_("You arent in one of the following groups: manager"))

        return super(TattooDesignMaterial, self).write(vals)
