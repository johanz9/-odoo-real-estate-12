from odoo import fields, models, api


class HideTattooDesign(models.Model):
    _inherit = 'tattoo.design'

    make_visible = fields.Boolean(string="User", compute='get_user')

    @api.depends('make_visible')
    def get_user(self, ):
        user_crnt = self._uid

        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('tattoo.tattoo_group_manager') or res_user.has_group('tattoo.tattoo_group_artist'):
            self.make_visible = True
        else:
            self.make_visible = False


class HideTattooSession(models.Model):
    _inherit = 'tattoo.session'

    make_visible = fields.Boolean(string="User", compute='get_user')

    @api.onchange('make_visible')
    def get_user(self, ):
        user_crnt = self._uid

        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('tattoo.tattoo_group_manager') or res_user.has_group('tattoo.tattoo_group_artist'):
            self.make_visible = True
        else:
            self.make_visible = False

