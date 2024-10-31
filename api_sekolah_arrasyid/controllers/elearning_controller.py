from odoo import http, fields
from odoo.http import request, Response
from odoo.exceptions import AccessError
import json
import base64
from werkzeug.exceptions import BadRequest

class ELearningController(http.Controller):

    @http.route('/api/get_user_quizzes', type='http', auth='user', methods=['GET'], csrf=False)
    def get_user_quizzes(self, **kwargs):
        try:
            user = request.env.user
            partner_id = user.partner_id.id
            slide_partner_relations = request.env['slide.slide.partner'].sudo().search([('partner_id', '=', partner_id)])
            
            quizzes = []
            for relation in slide_partner_relations:
                if relation.quiz_attempts_count > 0:
                    slide = relation.slide_id
                    channel = slide.channel_id

                    if slide.slide_type == 'quiz':
                        quizzes.append({
                            'slide_id': slide.id,
                            'slide_name': slide.name,
                            'slide_description': slide.description,
                            'slide_completion_time': slide.completion_time,
                            'slide_type': slide.slide_type,
                            'slide_first': slide.quiz_first_attempt_reward,
                            'slide_second': slide.quiz_second_attempt_reward,
                            'slide_third': slide.quiz_third_attempt_reward,
                            'slide_fourth': slide.quiz_fourth_attempt_reward,
                            'channel_id': channel.id,
                            'channel_name': channel.name,
                            'channel_description': channel.description,
                            'channel_type': channel.channel_type,
                            'completed': relation.completed,
                            'quiz_attempts_count': relation.quiz_attempts_count,
                            'partner_id': relation.partner_id.id,
                            'vote': relation.vote,
                        })

            response_data = {
                'partner_id': partner_id,
                'quizzes': quizzes
            }

            return Response(json.dumps(response_data), content_type='application/json', status=200)
        
        except Exception as e:
            return Response(json.dumps({'status': 500, 'message': str(e)}), status=500, mimetype='application/json')


    @http.route('/api/get_child_quizzes', type='http', auth='user', methods=['GET'], csrf=False)
    def get_child_quizzes(self, **kwargs):
        try:
            user = request.env.user
            partner = request.env['res.partner'].sudo().search([('user_id', '=', user.id)])

            parent_ayah = request.env['op.data.ayah'].sudo().search([('partner_id', '=', partner.id)], limit=1)
            parent_ibu = request.env['op.data.ibu'].sudo().search([('partner_id', '=', partner.id)], limit=1)
            parent_wali = request.env['op.data.wali'].sudo().search([('partner_id', '=', partner.id)], limit=1)

            if not parent_ayah and not parent_ibu and not parent_wali:
                return Response(json.dumps({'error': 'User is not a parent'}), status=403, mimetype='application/json')

            parent = parent_ayah or parent_ibu or parent_wali

            if not parent:
                return Response(json.dumps({'error': 'User is not a parent'}), status=403, mimetype='application/json')

            children = request.env['op.student'].sudo().search([
                '|', '|',
                ('ayah_id', '=', parent_ayah.id if parent_ayah else 0),
                ('ibu_id', '=', parent_ibu.id if parent_ibu else 0),
                ('wali_id', '=', parent_wali.id if parent_wali else 0)
            ])
                
            parent_partner_id = user.partner_id.id

            # Retrieve children associated with the parent
            # children = request.env['op.student'].sudo().search([('parent_id', '=', parent_partner_id)])
            # children = request.env['op.student'].sudo().search({('ayah_id','=', parent.id)})

            if not children:
                return Response(json.dumps({'status': 404, 'message': 'No children found for this parent'}), content_type='application/json', status=404)

            all_quizzes = []

            for child in children:
                child_partner_id = child.partner_id.id
                slide_partner_relations = request.env['slide.slide.partner'].sudo().search([('partner_id', '=', child_partner_id)])

                quizzes = []
                for relation in slide_partner_relations:
                    if relation.quiz_attempts_count > 0:
                        slide = relation.slide_id
                        channel = slide.channel_id

                        if slide.slide_type == 'quiz':
                            quizzes.append({
                                'slide_id': slide.id,
                                'slide_name': slide.name,
                                'slide_description': slide.description,
                                'slide_completion_time': slide.completion_time,
                                'slide_type': slide.slide_type,
                                'slide_first': slide.quiz_first_attempt_reward,
                                'slide_second': slide.quiz_second_attempt_reward,
                                'slide_third': slide.quiz_third_attempt_reward,
                                'slide_fourth': slide.quiz_fourth_attempt_reward,
                                'channel_id': channel.id,
                                'channel_name': channel.name,
                                'channel_description': channel.description,
                                'channel_type': channel.channel_type,
                                'completed': relation.completed,
                                'quiz_attempts_count': relation.quiz_attempts_count,
                                'partner_id': relation.partner_id.id,
                                'vote': relation.vote,
                            })

                all_quizzes.append({
                    'child_id': child.id,
                    'child_name': child.name,
                    'quizzes': quizzes
                })

            response_data = {
                'parent_id': parent_partner_id,
                'children_quizzes': all_quizzes
            }

            return Response(json.dumps(response_data), content_type='application/json', status=200)
        
        except Exception as e:
            return Response(json.dumps({'status': 500, 'message': str(e)}), status=500, mimetype='application/json')

