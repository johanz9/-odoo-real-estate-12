# from odoo import fields, models, api, _
# import datetime
#
# current_date = datetime.datetime.now().date()
#
#
# class ProductTemplate(models.Model):
#     _inherit = "product.template"
#
#     sale_order_ids = fields.One2many('sale.order', 'sale_order_id')
#     sale_order_count = fields.Integer("Orders", compute='_compute_order_count')
#
#     @api.depends("offer_ids")
#     def _compute_order_count(self):
#         for record in self:
#             count = 0
#             for item in record.sale_order_ids:
#                 count += 1
#             record.sale_order_count = countfrom odoo import fields, models, api, _
# import datetime
#
# current_date = datetime.datetime.now().date()
#
#
# class ProductTemplate(models.Model):
#     _inherit = "product.template"
#
#     sale_order_ids = fields.One2many('sale.order', 'sale_order_id')
#     sale_order_count = fields.Integer("Orders", compute='_compute_order_count')
#
#     @api.depends("offer_ids")
#     def _compute_order_count(self):
#         for record in self:
#             count = 0
#             for item in record.sale_order_ids:
#                 count += 1
#             record.sale_order_count = count
