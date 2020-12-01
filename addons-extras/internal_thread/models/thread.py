#coding: utf-8
from openerp import exceptions, SUPERUSER_ID
from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class mail_compose_message(models.TransientModel):
    _inherit = 'mail.compose.message'

    send_only_internal = fields.Boolean(string='Send only for selected users')

    def send_mail(self, cr, uid, ids, context=None):
        context = dict(context or {})
        for wizard in self.browse(cr, uid, ids, context=context):
        	if wizard.send_only_internal:
    			context.update({'put_this_subtype_instead':'internal_thread.mt_internal_mes'})
    	return super(mail_compose_message, self).send_mail(cr, uid, ids, context=context)    	
 	

class mail_message(models.Model):
    _inherit = 'mail.message'

    def _search(self, cr, uid, args, offset=0, limit=None, order=None,
        context=None, count=False, access_rights_uid=None):
        if uid == SUPERUSER_ID:
            return super(mail_message, self)._search(cr, uid, args, offset=offset, limit=limit, order=order,
                context=context, count=count, access_rights_uid=access_rights_uid)
        group_ids = self.pool.get('res.users').browse(cr, uid, uid, context=context).groups_id
        group_user_id = self.pool.get("ir.model.data").get_object_reference(cr, uid, 'base', 'group_user')[1]
        mt_internal_mes = self.pool.get("ir.model.data").get_object_reference(cr, uid, 'internal_thread', 'mt_internal_mes')[1]

        if group_user_id not in [group.id for group in group_ids]:
            args = [('subtype_id', '!=', mt_internal_mes)] + list(args) 

        return super(mail_message, self)._search(cr, uid, args, offset=offset, limit=limit, order=order,
            context=context, count=count, access_rights_uid=access_rights_uid)        