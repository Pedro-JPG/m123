from openerp import api, fields, models


class account_summary_wizard(models.TransientModel):
    _name = 'account_summary_wizard'
    _description = 'Partner Account Summary Wizard'

    from_date = fields.Date('From')
    to_date = fields.Date('To')
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required = True,
        default = lambda self: self . env['res.company'] . _company_default_get ( 'account.invoice' ),
        help="If blank are to list all movements for which the user has permission , if a company is defined will be shown only movements that company")
    show_invoice_detail = fields.Boolean('Show Invoice Detail')
    show_receipt_detail = fields.Boolean('Show Receipt Detail')
    result_selection = fields.Selection(
        [('customer', 'Receivable Accounts'),
         ('supplier', 'Payable Accounts'),
         ('customer_supplier', 'Receivable and Payable Accounts')],
        "Account Type's", required=True, default='customer_supplier')
    partner_ids = fields.Many2many ( 'res.partner', 'rel_wizard_partner_summary', 'partner_ids', 'id', string = 'Partner', required = True,
        domain = "[( 'company_id', '=', company_id ), ( 'active', '=', True ), '|', ( 'customer', '=', True ), ( 'supplier', '=', True )]"
    )
    company_currency_id = fields.Many2one ( 'res.currency', string = 'Currency', required = True,
        default = lambda self: self . company_id . browse ( self . env['res.company'] . _company_default_get ( 'account.invoice' ) ) . currency_id . id )
    currency_id = fields.Many2one ( 'res.currency', string = 'Currency', required = True,
        default = lambda self: self . company_id . browse ( self . env['res.company'] . _company_default_get ( 'account.invoice' ) ) . currency_id . id )

    @api.multi
    def account_summary(self):
        # import pdb; pdb.set_trace ( )
        active_id = self._context.get('active_id', False)
        # active_ids = self._context.get('active_ids', False)
        # if not active_ids:
        #     active_ids = [self.env.user.partner_id]
        if not active_id:
            partner = self.env.user.partner_id
            active_id = partner.id
        else:
            partner = self.env['res.partner'].browse(active_id)

        active_ids = self . partner_ids

        if self . currency_id == self . company_currency_id:
            return self.env['report'].with_context(
                from_date=self.from_date,
                to_date=self.to_date,
                company_id=self.company_id.id,
                currency_id = self . currency_id . id,
                currency_symbol = self . currency_id . name + ' (' + self . currency_id . symbol + ')',
                company_currency_id = self . company_currency_id . id,
                active_id=active_id,
                active_ids=active_ids,
                show_invoice_detail=self.show_invoice_detail,
                show_receipt_detail=self.show_receipt_detail,
                result_selection=self.result_selection).get_action(
                active_ids, 'report_account_summary')
        else:
            return self.env['report'].with_context(
                from_date=self.from_date,
                to_date=self.to_date,
                company_id=self.company_id.id,
                currency_id = self . currency_id . id,
                currency_symbol = self . currency_id . name + ' (' + self . currency_id . symbol + ')',
                company_currency_id = self . company_currency_id . id,
                active_id=active_id,
                active_ids=active_ids,
                show_invoice_detail=self.show_invoice_detail,
                show_receipt_detail=self.show_receipt_detail,
                result_selection=self.result_selection).get_action(
                active_ids, 'report_account_summary_2')

