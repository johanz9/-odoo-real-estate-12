import datetime
from odoo import models, fields, api

class TattooDesign(models.Model):
    _name = 'tattoo.design'
    _description = "Tattoo Design"
    _order = 'id desc'

    name = fields.Char(string="Nome del disegno", required=True)
    time = fields.Float(string='Tempo di esecuzione (in ore)')
    material_ids = fields.Many2many('tattoo.design.material', string='Materiali')
    labor_price = fields.Float(string="Costo Manodopera")
    price = fields.Float(string="Costo tattuaggio", compute="_compute_price", readonly=True)
    image_01 = fields.Binary("Prima Immagine", help="Select image here")
    image_02 = fields.Binary("Seconda Immagine", help="Select image here")

    @api.depends('labor_price', "material_ids")
    def _compute_price(self):
        for record in self:
            material_price_sum = 0
            for material in self.material_ids:
                material_price_sum += material.price

            record.price = record.labor_price + material_price_sum


class TattooDesignMaterial(models.Model):
    _name = 'tattoo.design.material'
    _description = "Tattoo Design Material"
    _order = 'id desc'

    name = fields.Char(string="Nome del Materiale", required=True)
    price = fields.Float(string="Prezzo del materiale", required=True)


