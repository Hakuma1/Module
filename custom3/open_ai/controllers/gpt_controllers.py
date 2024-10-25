# -*- coding: utf-8 -*-
import openai
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.mail import PortalChatter
from odoo.tools import plaintext2html


class OpenAi(PortalChatter):

    @http.route(['/mail/chatter_post'], type='json', methods=['POST'], auth='public', website=True)
    def portal_chatter_post(self, res_model, res_id, message, attachment_ids=None, attachment_tokens=None, **kw):
        result = super().portal_chatter_post(res_model, res_id, message, attachment_ids, attachment_tokens, **kw)
        if message:
            api_key = request.env.user.tokengpt
            user = request.env.user.id
            info = request.env["token.info"].sudo().search([('token', '=', api_key), ('user_id', '=', user)])
            ticket_id = request.env[res_model].sudo().search([("id", '=', int(res_id))])
            try:
                message_2, prompt_tokens, total_tokens = self.ChatGPT_conversation(message, api_key)
                message_2 = plaintext2html(message_2)
                ticket_id.message_post(body=message_2, message_type='comment', author_id=2,
                                       subtype_id=request.env.ref('mail.mt_comment').id)
                historique = {"prompt_tokens": prompt_tokens, "total_tokens": total_tokens,
                              "montant_total": (total_tokens * 0.002) / 1000, "answer": message_2, "question": message}
                if not info:
                    info.sudo().create(
                        {"user_id": user, "total_tokens": total_tokens, "montant_total": (total_tokens * 0.002) / 1000,
                         "token": api_key, "historique_ids": [(0, 0, historique)]})
                else:
                    info.sudo().create(
                        {"total_tokens": total_tokens, "montant_total": (total_tokens * 0.002) / 1000,
                         "historique_ids": [(0, 0, historique)]})
            except Exception as e:
                #message_erreur = "Veuillez réessayer s'il vous plaît!!"
                message_erreur = plaintext2html(e)
                ticket_id.message_post(body=message_erreur, message_type='comment', author_id=2,
                                       subtype_id=request.env.ref('mail.mt_comment').id)
        return result

    def ChatGPT_conversation(self, message, key):
        openai.api_key = key
        model_id = 'gpt-3.5-turbo'
        conversation = []
        conversation.append({'role': 'user', 'content': message})
        response = openai.ChatCompletion.create(model=model_id, messages=conversation)
        return response['choices'][-1]['message']['content'], response['usage']['prompt_tokens'], response['usage'][
            'total_tokens']
