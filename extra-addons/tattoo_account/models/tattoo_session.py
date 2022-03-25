from odoo import fields, models, api, _
from odoo.exceptions import UserError, AccessError
import datetime

class Property(models.Model):
    _inherit = "tattoo.session"

    # override sold action
    def pagata_session(self):

        if self.env.user.has_group('account.group_account_invoice'):
            # check if the user is in group billing
            try:
                self.check_access_rights('write')
                self.check_access_rights('create')
            except AccessError:
                raise UserError(_("You don't have the access rights needed to update or create a invoice"))

            # check access rules
            self.check_access_rule('create')

            # sudo bypass right and rules
            # journal = self.env['account.move'].with_context(
            #     default_move_type='out_invoice').sudo()._get_default_journal()

            # JOURNAL
            journal = self.env['account.journal'].search([('type', '=', 'sale')])[0]

            if not journal:
                raise UserError(_('Journal not found'))
            # journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()

            # Move Line creation:
            invoice_lines = [
                {
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100
                }
            ]

            # Move creation
            account_move = self.env['account.move'].sudo().create({
                'partner_id': self.client_id.id,
                'move_type': "out_invoice",
                'journal_id': journal.id,
                'invoice_line_ids': invoice_lines,
                'invoice_date': datetime.datetime.today(),
                'company_id': self.env.user.company_id.id,
            })

            return super().pagata_session()
        else:
            raise UserError(_("You don't have the access needed"))
