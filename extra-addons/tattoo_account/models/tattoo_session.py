from odoo import fields, models, api, _
from odoo.exceptions import UserError, AccessError
import datetime

from odoo.tools import float_is_zero


class TattooSession(models.Model):
    _inherit = "tattoo.session"

    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        company_id = self.env.user.company_id.id
        journal_id = (self.env['account.invoice'].with_context(company_id=company_id or self.env.user.company_id.id)
            .default_get(['journal_id'])['journal_id'])
        if not journal_id:
            raise UserError(_('Please define an accounting sales journal for this company.'))
        return {
            'name': 'customer invoice',
            'origin': self.design_id.name + ' ' + self.client_id.name + ' ' + str(self.id),
            'type': 'out_invoice',
            # 'account_id': self.partner_invoice_id.property_account_receivable_id.id,
            # 'partner_shipping_id': self.client_id.partner_shipping_id.id,
            'journal_id': journal_id,
            # 'currency_id': self.pricelist_id.currency_id.id,
            'partner_id': self.client_id.id,
            'user_id': self.env.user.id,
            'date_invoice': datetime.datetime.today().date(),
        }

    @api.multi
    def _prepare_invoice_line(self, qty=1):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.
        :param qty: float quantity to invoice
        """
        self.ensure_one()

        res = {
            'name': self.design_id.name,
            'sequence': 10,
            'account_id': 17,
            'price_unit': self.session_cost,
            'quantity': qty,
            'discount': False,
            'uom_id': False,
            'product_id': False,
            'invoice_line_tax_ids': [(6, False, [])],
            # 'account_analytic_id': self.order_id.analytic_account_id.id,
            # 'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'display_type': False,
        }
        return res

    def invoice_line_create_vals(self, invoice_id, qty):
        """ Create an invoice line. The quantity to invoice can be positive (invoice) or negative
            (refund).
            :param invoice_id: integer
            :param qty: float quantity to invoice
            :returns list of dict containing creation values for account.invoice.line records
        """

        vals_list = []
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for line in self:
            if not float_is_zero(qty, precision_digits=precision) or not line.product_id:
                vals = line._prepare_invoice_line(qty=qty)
                vals.update({'invoice_id': invoice_id, 'sale_line_ids': [(6, 0, [line.id])]})
                vals_list.append(vals)
        return vals_list

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        inv_obj = self.env['account.invoice']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {}
        references = {}
        invoices_origin = {}
        invoices_name = {}

        # Keep track of the sequences of the lines
        # To keep lines under their section
        inv_line_sequence = 0
        for record in self:
            # partner_invoice_id.id -> indirizzo invoice
            group_key = record.id if grouped else (
                record.client_id.partner_invoice_id.id, record.client_id.currency_id.id)

            # We only want to create sections that have at least one invoiceable line
            pending_section = None

            # Create lines in batch to avoid performance problems
            line_vals_list = []
            # sequence is the natural order of order_lines

            if group_key not in invoices:
                inv_data = record._prepare_invoice()
                invoice = inv_obj.create(inv_data)
                references[invoice] = record
                invoices[group_key] = invoice
                invoices_origin[group_key] = [invoice.origin]
                invoices_name[group_key] = [invoice.name]
            elif group_key in invoices:
                if record.name not in invoices_origin[group_key]:
                    invoices_origin[group_key].append(record.name)
                if record.client_order_ref and record.client_order_ref not in invoices_name[group_key]:
                    invoices_name[group_key].append(record.client_order_ref)

            # CREATE LINES
            section_invoice = record.invoice_line_create_vals(invoices[group_key].id, qty=1)
            inv_line_sequence += 1
            section_invoice[0]['sequence'] = inv_line_sequence
            line_vals_list.extend(section_invoice)

            if references.get(invoices.get(group_key)):
                if record not in references[invoices[group_key]]:
                    references[invoices[group_key]] |= record

            self.env['account.invoice.line'].create(line_vals_list)

        for group_key in invoices:
            invoices[group_key].write({
                'name': ', '.join(invoices_name[group_key])[:2000],
                'origin': ', '.join(invoices_origin[group_key])
            })

            # tattoo_orders = references[invoices[group_key]]
            # if len(tattoo_orders) == 1:
            #     invoices[group_key].reference = tattoo_orders.reference

        if not invoices:
            raise UserError(
                _('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

        # self._finalize_invoices(invoices, references)
        return [inv.id for inv in invoices.values()]

    # override sold action
    def pagata_session(self):

        # SECURITY CHECK
        if not self.env['account.move'].check_access_rights('create', False):
            # check if the user is in group billing
            try:
                self.check_access_rights('write')
                self.check_access_rights('create')
            except AccessError:
                raise UserError(_("You don't have the access rights needed to update or create a invoice"))

        # CREATE INVOICE
        self.action_invoice_create(self)


        return super().pagata_session()
