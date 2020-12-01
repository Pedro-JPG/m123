from openerp import api, models
# import ipdb as pdb

class ParticularReport(models.AbstractModel):
    _inherit = 'report.abstract_report'
    _name = 'report.dtm_minimum_stock.minimum_stock_report'


    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']

        report = report_obj._get_report_from_name('dtm_minimum_stock.minimum_stock_report')

        stock = []

        products = self.env['product.product'].search([]).sorted(key=lambda r: r.name)

        for product in products:
            if product.virtual_available <= product.qty_minimum:
                stock.append(product.id)

        stock_minimo = self.env['product.product'].browse(stock)

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'stock': stock_minimo,
        }
        return report_obj.render('dtm_minimum_stock.minimum_stock_report', docargs)
