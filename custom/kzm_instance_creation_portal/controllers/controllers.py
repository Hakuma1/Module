# -*- coding: utf-8 -*-
from collections import OrderedDict
from odoo import http, _, fields, SUPERUSER_ID
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.osv.expression import AND, OR
from datetime import datetime
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.tools import groupby as groupbyelem
from operator import itemgetter
from datetime import timedelta
from odoo.fields import Date


class InstanceCustomerPortal(CustomerPortal):

    def _get_portal_default_domain(self):
        my_user = request.env.user
        return [
            ('create_uid', '=', my_user.id),
        ]

    @http.route(['/my/instances', '/my/instances/page/<int:page>'], auth='public', website=True)
    def index(self, page=1, sortby=None, filterby=None, search=None, search_in='name', groupby='none', **kw):
        domain = self._get_portal_default_domain()
        searchbar_sortings = {
            'partner': {'label': _('Customer'), 'order': 'partner_id'},
            'name': {'label': _('Name'), 'order': 'name'},
            'odoo_version': {'label': _('Odoo version'), 'order': 'odoo_id'},
        }

        searchbar_inputs = {
            'name': {'input': 'name', 'label': _('Search in Name')},
            'odoo_id': {'input': 'odoo_id', 'label': _('Search in Odoo Version')},
            'limit_date': {'input': 'limit_date', 'label': _('Search in Limit Date')},
            'partner_id': {'input': 'partner_id', 'label': _('Search in Customer')},
        }

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'state': {'input': 'state', 'label': _('State')},
            'version': {'input': 'odoo_id', 'label': _('Version')},
        }

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('state', 'in', ['Draft', 'Submitted', 'In process', 'Processed'])]},
            'draft': {'label': _('Draft'), 'domain': [('state', '=', 'Draft')]},
            'submitted': {'label': _('Submitted'), 'domain': [('state', '=', 'Submitted')]},
            'in_process': {'label': _('In process'), 'domain': [('state', '=', 'In process')]},
            'processed': {'label': _('Processed'), 'domain': [('state', '=', 'Processed')]},
        }

        if not filterby:
            filterby = 'all'
        domain = AND([domain, searchbar_filters[filterby]['domain']])

        if not sortby:
            sortby = 'partner'
        order = searchbar_sortings[sortby]['order']

        # search
        if search and search_in:
            search_domain = []
            if search_in == 'name':
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in == 'odoo_id':
                search_domain = OR([search_domain, [('odoo_id', 'ilike', search)]])
            if search_in == 'limit_date':
                if '-' in search:
                    search = search.replace("-", "/")
                search = datetime.strptime(search, '%d/%m/%Y')
                search = search.date()
                search_domain = OR([search_domain, [('limit_date', 'ilike', search)]])
            if search_in == 'partner_id':
                search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
            domain = AND([domain, search_domain])

        instance_count = request.env['kzm.instance.request'].search_count(domain)
        pager = portal_pager(
            url="/my/instances",
            url_args={'sortby': sortby, 'search_in': search_in,
                      'search': search, 'groupby': groupby, 'filterby': filterby},
            total=instance_count,
            page=page,
            step=15
        )
        instances = request.env['kzm.instance.request'].sudo().search(domain, order=order, limit=15,
                                                                      offset=pager['offset'])
        request.session['my_instances_history'] = instances.ids[:len(instances)]

        # Group By
        if groupby != 'none':
            grouped_instances = [request.env['kzm.instance.request'].concat(*g) for k, g in
                                 groupbyelem(instances, itemgetter(searchbar_groupby[groupby]['input']))]
        else:
            grouped_instances = [instances]
        events_data = []
        instances_z = instances.filtered(lambda x: x.treat_date and x.limit_date).sorted('treat_date')
        for event in instances_z:
            events_data.append({
                'id': event.id,
                'title': event.name,
                'start': str(event.treat_date.date()),
                'end': str(event.limit_date),
            })
        print("events_data", events_data)

        return request.render('kzm_instance_creation_portal.list_instance_portal',
                              {'page_name': 'instance',
                               'events_data': events_data,
                               'start_date': instances_z[-1].treat_date if instances_z and instances_z[
                                   -1].treat_date else fields.Date.today(),
                               'searchbar_sortings': searchbar_sortings,
                               'searchbar_groupby': searchbar_groupby,
                               'sortby': sortby,
                               'groupby': groupby,
                               'default_url': '/my/instances',
                               'grouped_instances': grouped_instances,
                               'search_in': search_in,
                               'search': search,
                               'searchbar_inputs': searchbar_inputs,
                               'pager': pager,
                               'searchbar_filters': searchbar_filters,
                               'filterby': filterby,
                               # 'instances': instances,
                               })

    @http.route(['/my/instances/<int:instance_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, instance_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            instance_sudo = self._document_check_access('kzm.instance.request', instance_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=instance_sudo, report_type=report_type,
                                     report_ref='kzm_instance_request.instance_action_report', download=download)

        if request.env.user.share and access_token:
            # If a public/portal user accesses the order with the access token
            # Log a note on the chatter.
            today = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % instance_sudo.id)
            if session_obj_date != today:
                # store the date as a string in the session to allow serialization
                request.session['view_quote_%s' % instance_sudo.id] = today
                # The "Quotation viewed by customer" log note is an information
                # dedicated to the salesman and shouldn't be translated in the customer/website lgg
                context = {'lang': instance_sudo.user_id.partner_id.lang or instance_sudo.company_id.partner_id.lang}
                msg = _('Quotation viewed by customer %s', instance_sudo.partner_id.name)
                del context
                _message_post_helper(
                    "kzm_instance_request.kzm.instance.request",
                    instance_sudo.id,
                    message=msg,
                    token=instance_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=instance_sudo.user_id.sudo().partner_id.ids,
                )

        backend_url = f'/web#model={instance_sudo._name}' \
                      f'&id={instance_sudo.id}' \
                      f'&view_type=form'
        values = {
            'instance_order': instance_sudo,
            'message': message,
            'report_type': 'html',
            'backend_url': backend_url,
        }

        # Payment values
        """ if order_sudo._has_to_be_paid():
            values.update(self._get_payment_values(order_sudo))

        if order_sudo.state in ('draft', 'sent', 'cancel'):
            history_session_key = 'my_quotations_history'
        else:"""
        history_session_key = 'my_instances_history'

        values = self._get_page_view_values(
            instance_sudo, access_token, values, history_session_key, False)

        return request.render('kzm_instance_creation_portal.instance_order_portal_template', values)

    @http.route('/form_create_instance', auth='public', website=True)
    def instance_form(self, **kw):
        return request.render('kzm_instance_creation_portal.form_instance_portal', {})

    @http.route('/create/instance', auth='public', website=True)
    def instance_created(self, **kw):
        kw['state'] = 'Submitted'
        request.env['kzm.instance.request'].sudo().create(kw)
        return request.render('kzm_instance_creation_portal.instance_created', {})

    def _prepare_home_portal_values(self, counters):
        values = super(InstanceCustomerPortal, self)._prepare_home_portal_values(counters)
        create_id = http.request.env.context.get('uid')
        instances_count = request.env['kzm.instance.request'].sudo().search_count([('create_uid', '=', create_id)])
        values.update({'instances_count': instances_count, })
        return values

    @http.route('/my_calendar/events', type='json', auth='public')
    def get_events(self):
        events = request.env['kzm.instance.request'].search([])
        events_data = []
        for event in events:
            events_data.append({
                'id': event.id,
                'title': event.name,
                'start': event.treat_date,
                'end': event.limit_date.date(),
            })
        return events_data
