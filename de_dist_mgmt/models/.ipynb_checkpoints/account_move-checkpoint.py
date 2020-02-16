# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    retail_price_unit = fields.Float(string='Retail Price', digits='Product Price',store=True,default=1.0)
    
    def write2(self, vals):
        #BUSINESS_FIELDS = ('price_unit', 'retail_price_unit','quantity', 'discount', 'tax_ids')
        self.retail_price_unit = True
        res = super(AccountMoveLine,self).write(vals)
        
        return res
    
    def write1(self, vals):
        # OVERRIDE
        def field_will_change(line, field_name):
            #if field_name not in vals:
                #return False
            field = line._fields[field_name]
            if field.type == 'many2one':
                return line[field_name].id != vals[field_name]
            if field.type in ('one2many', 'many2many'):
                current_ids = set(line[field_name].ids)
                after_write_ids = set(r['id'] for r in line.resolve_2many_commands(field_name, vals[field_name], fields=['id']))
                return current_ids != after_write_ids
            if field.type == 'monetary' and line[field.currency_field]:
                return not line[field.currency_field].is_zero(line[field_name] - vals[field_name])
            return line[field_name] != vals[field_name]

        ACCOUNTING_FIELDS = ('debit', 'credit', 'amount_currency')
        BUSINESS_FIELDS = ('price_unit', 'retail_price_unit','quantity', 'discount', 'tax_ids')
        PROTECTED_FIELDS_TAX_LOCK_DATE = ['debit', 'credit', 'tax_line_id', 'tax_ids', 'tag_ids']
        PROTECTED_FIELDS_LOCK_DATE = PROTECTED_FIELDS_TAX_LOCK_DATE + ['account_id', 'journal_id', 'amount_currency', 'currency_id', 'partner_id']
        PROTECTED_FIELDS_RECONCILIATION = ('account_id', 'date', 'debit', 'credit', 'amount_currency', 'currency_id')

        account_to_write = self.env['account.account'].browse(vals['account_id']) if 'account_id' in vals else None

        # Check writing a deprecated account.
        if account_to_write and account_to_write.deprecated:
            raise UserError(_('You cannot use a deprecated account.'))

        # when making a reconciliation on an existing liquidity journal item, mark the payment as reconciled
        for line in self:
            if line.parent_state == 'posted':
                if line.move_id.restrict_mode_hash_table and set(vals).intersection(INTEGRITY_HASH_LINE_FIELDS):
                    raise UserError(_("You cannot edit the following fields due to restrict mode being activated on the journal: %s.") % ', '.join(INTEGRITY_HASH_LINE_FIELDS))
                if any(key in vals for key in ('tax_ids', 'tax_line_ids')):
                    raise UserError(_('You cannot modify the taxes related to a posted journal item, you should reset the journal entry to draft to do so.'))
            if 'statement_line_id' in vals and line.payment_id:
                # In case of an internal transfer, there are 2 liquidity move lines to match with a bank statement
                if all(line.statement_id for line in line.payment_id.move_line_ids.filtered(
                        lambda r: r.id != line.id and r.account_id.internal_type == 'liquidity')):
                    line.payment_id.state = 'reconciled'

            # Check the lock date.
            if any(field_will_change(line, field_name) for field_name in PROTECTED_FIELDS_LOCK_DATE):
                line.move_id._check_fiscalyear_lock_date()

            # Check the tax lock date.
            if any(field_will_change(line, field_name) for field_name in PROTECTED_FIELDS_TAX_LOCK_DATE):
                line._check_tax_lock_date()

            # Check the reconciliation.
            if any(field_will_change(line, field_name) for field_name in PROTECTED_FIELDS_RECONCILIATION):
                line._check_reconciliation()

            # Check switching receivable / payable accounts.
            if account_to_write:
                account_type = line.account_id.user_type_id.type
                if line.move_id.is_sale_document(include_receipts=True):
                    if (account_type == 'receivable' and account_to_write.user_type_id.type != account_type) \
                            or (account_type != 'receivable' and account_to_write.user_type_id.type == 'receivable'):
                        raise UserError(_("You can only set an account having the receivable type on payment terms lines for customer invoice."))
                if line.move_id.is_purchase_document(include_receipts=True):
                    if (account_type == 'payable' and account_to_write.user_type_id.type != account_type) \
                            or (account_type != 'payable' and account_to_write.user_type_id.type == 'payable'):
                        raise UserError(_("You can only set an account having the payable type on payment terms lines for vendor bill."))

        result = super(AccountMoveLine, self).write(vals)

        for line in self:
            if not line.move_id.is_invoice(include_receipts=True):
                continue

            # Ensure consistency between accounting & business fields.
            # As we can't express such synchronization as computed fields without cycling, we need to do it both
            # in onchange and in create/write. So, if something changed in accounting [resp. business] fields,
            # business [resp. accounting] fields are recomputed.
            if any(field in vals for field in ACCOUNTING_FIELDS):
                balance = line.currency_id and line.amount_currency or line.debit - line.credit
                price_subtotal = line._get_price_total_and_subtotal().get('price_subtotal', 0.0)
                to_write = line._get_fields_onchange_balance(
                    balance=balance,
                    price_subtotal=price_subtotal,
                )
                to_write.update(line._get_price_total_and_subtotal(
                    price_unit=to_write.get('price_unit', line.price_unit),
                    retail_price_unit=to_write.get('price_unit', line.retail.price_unit),
                    quantity=to_write.get('quantity', line.quantity),
                    discount=to_write.get('discount', line.discount),
                ))
                super(AccountMoveLine, line).write(to_write)
            elif any(field in vals for field in BUSINESS_FIELDS):
                to_write = line._get_price_total_and_subtotal()
                to_write.update(line._get_fields_onchange_subtotal(
                    price_subtotal=to_write['price_subtotal'],
                ))
                super(AccountMoveLine, line).write(to_write)

        # Check total_debit == total_credit in the related moves.
        if self._context.get('check_move_validity', True):
            self.mapped('move_id')._check_balanced()

        return result
    
    