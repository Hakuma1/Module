from odoo import http
from odoo.http import request, route, Controller
from odoo.addons.portal.controllers.mail import PortalChatter
import openai
from odoo.tools import plaintext2html


class ChatbotController(PortalChatter):

    @http.route(['/mail/chatter_post'], type='json', methods=['POST'], auth='public', website=True)
    def portal_chatter_post(self, res_model, res_id, message, attachment_ids=None, attachment_tokens=None, **kw):
        result = super(ChatbotController, self).portal_chatter_post(res_model, res_id, message, attachment_ids,
                                                                    attachment_tokens, **kw)
        if message:
            conversation = []
            key = request.env.user.chatgpt_token
            """token_informations = request.env["token.info"].search(
                [('token', '=', key), ('user_id', '=', request.env.user.id)])
            print("Token info ", token_informations)
            historique = request.env["chatbot.historique"].search([('token_info_id', 'in', token_informations.ids)])
            print("Historique ", historique)
            for info in historique:
                conversation.append({'role': 'user', 'content': info.question})"""
            try:
                conversation.append({'role': 'user', 'content': message})
                print(conversation)

                message_2, total_tokens, prompt_tokens = self.ChatGPT_conversation(conversation, key)
                message_2 += "\n\n" + "Nombre total de token: " + str(total_tokens)
                # message = message + "\n\n" + message_2
                mess = request.env[res_model].search([('id', '=', int(res_id))])
                mess.sudo().message_post(body=plaintext2html(message_2), message_type='comment',
                                         subtype_id=request.env.ref("mail.mt_comment").id, author_id=2)
                info = request.env["token.info"].search(
                    [('user_id', '=', request.env.user.id), ('token', '=', key)])
                print(info)
                if not info:
                    creation = request.env["token.info"].sudo().create(
                        {"total_token": total_tokens, "user_id": request.env.user.id,
                         "token": key, 'prix_total': (total_tokens * 0.002) / 1000,
                         "historique_ids": [(0, 0, {'question': message, 'answer': message_2,
                                                    'total_token': total_tokens,
                                                    'prompt_tokens': prompt_tokens,
                                                    'prix_total': (total_tokens * 0.002) / 1000})]})
                else:
                    modification = info.sudo().write(
                        {"total_token": total_tokens, 'prix_total': (total_tokens * 0.002) / 1000,
                         "historique_ids": [
                             (0, 0, {'question': message, 'total_token': total_tokens,
                                     'prompt_tokens': prompt_tokens, 'answer': message_2,
                                     'prix_total': (total_tokens * 0.002) / 1000})]})
            except Exception as e:
                message_erreur = "Veuillez réessayer s'il vous plaît!!"
                mess = request.env[res_model].search([('id', '=', int(res_id))])
                mess.sudo().message_post(body=plaintext2html(message_erreur), message_type='comment',
                                         subtype_id=request.env.ref("mail.mt_comment").id, author_id=2)
        return result

    def ChatGPT_conversation(self, conversation, api_key):
        openai.api_key = api_key
        model_id = 'gpt-3.5-turbo'
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=conversation
        )
        # api_usage = response['usage']
        # print('Total token: {0}'.format(api_usage['total_tokens']))
        # Arrêt normal ou brutal
        # print(response['choices'][-1].finish_reason)
        return response['choices'][-1]['message']['content'], response['usage']['total_tokens'], response['usage'][
            'prompt_tokens']
