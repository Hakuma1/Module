def get_actual_page_url_receptions(self):
    for record in self:
        done_receptions_not_duplicated = record.all_done_receptions_not_duplicated()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        action = self.env.ref('valtech_purchase.action_picking_tree_with_domain')
        action['domain'] = [('id', 'in', done_receptions_not_duplicated)]
        if len(done_receptions_not_duplicated) == 1:
            link = str(base_url) + '/web#id=' + str(done_receptions_not_duplicated[0]) + '&action=' + str(
                action.id) + '&model=stock.picking&view_type=form'
        else:
            link = str(base_url) + '/web#' + '&action=' + str(action.id) + '&model=stock.picking&view_type=list'

        return link


def send_notifications_to_all_members_of_cdg_group(self):
    for record in self:
        template_id = self.env.ref(
            'valtech_purchase.notification_reception_not_linked_for_members_of_control_gestion_template').id
        mail_template = self.env['mail.template'].browse(template_id)
        for rec in self.env.ref('valtech_purchase.group_controle_de_gestion').users.mapped('partner_id'):
            email_values_ctx = {
                'partner_to': str(rec.id),
                'purchase_order_name': record.name,
                'partner_name': str(rec.name),
                'lang': rec.lang,
            }
            mail_template.with_context(email_values_ctx).send_mail(record.id, force_send=True)