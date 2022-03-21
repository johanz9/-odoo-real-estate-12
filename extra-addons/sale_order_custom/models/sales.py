from odoo import fields, models, api, _
from odoo.exceptions import UserError, AccessError
import datetime

current_date = datetime.datetime.now().date()

class SaleOrder(models.Model):
    _inherit = "sale.order"

    particular_request = fields.Boolean(string="Ordine con richiesta particolare")
    request_description = fields.Char(string="Motivo richiesta particolare")

    # adding more field only for test

    test_integer = fields.Integer(string="Test Integer", default="10")
    test_float= fields.Float(string="Test Float", default="15.5")
    test_text = fields.Text(string="Test Text")
    test_date = fields.Date(string="Test date", default=current_date)
    status = fields.Selection([
        ('new', 'New'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')], 'Status', default='new',
        store=True)
    total = fields.Float(string="Total", compute="_compute_total", store=True)

    # get current user as default
    test_many2one = fields.Many2one('res.users', string='User: Many2one Test', index=True,
                                  default=lambda self: self.env.uid)
    test_datetime = fields.Datetime(string="Test Datetime", default=datetime.datetime.now())

    # for computed field
    # it only sum two field and add it to total
    @api.depends("test_integer", "test_float")
    def _compute_total(self):
        print(self.env.user.company_id)
        for record in self:
            record.total = record.test_integer + record.test_float



