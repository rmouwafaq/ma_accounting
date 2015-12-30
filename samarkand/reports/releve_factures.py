import time
from openerp.osv import osv
from openerp.report import report_sxw


class releve_factures(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(releve_factures, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_titles': self._get_titles,
        })
    def _get_titles(self,qty):
        return qty*2
class report_product_pricelist(osv.AbstractModel):
    _name = 'report.samarkand.report_relevefacture'
    _inherit = 'report.abstract_report'
    _template = 'samarkand.report_relevefacture'
    _wrapped_report_class = releve_factures