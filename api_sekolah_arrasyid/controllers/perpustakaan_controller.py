# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
import logging
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
_logger = logging.getLogger(__name__)

class MediaController(http.Controller):

    @http.route('/api/get_medias', type='http', auth='user', methods=['GET'], csrf=False)
    def get_books(self, **kwargs):
        try:
            books = request.env['op.media'].sudo().search([])

            book_list = []
            for book in books:
                book_data = {
                    'id': book.id,
                    'name': book.name,
                    'isbn': book.isbn,
                    'tags': [tag.name for tag in book.tags],
                    'authors': [author.name for author in book.author_ids],
                    'edition': book.edition,
                    'description': book.description,
                    'publishers': [publisher.name for publisher in book.publisher_ids],
                    'courses': [course.name for course in book.course_ids],
                    'subjects': [subject.name for subject in book.subject_ids],
                    'internal_code': book.internal_code,
                    'media_type': book.media_type_id.name if book.media_type_id else None,
                }
                book_list.append(book_data)

            return request.make_response(json.dumps({'status': 200, 'data': book_list}), headers={'Content-Type': 'application/json'})

        except Exception as e:
            return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers={'Content-Type': 'application/json'})

    @http.route('/api/get_media_units', type='http', auth='user', methods=['GET'], csrf=False)
    def get_media_units(self, **kwargs):
        try:
            # Query the op.media.unit model
            media_units = request.env['op.media.unit'].sudo().search([])

            # Prepare the data to be returned
            media_unit_list = []
            for unit in media_units:
                unit_data = {
                    'id': unit.id,
                    'name': unit.name,
                    'media_id': unit.media_id.id,
                    'media_name': unit.media_id.name,
                    'barcode': unit.barcode,
                    'state': unit.state,
                    'media_type_id': unit.media_type_id.id if unit.media_type_id else None,
                    'media_type_name': unit.media_type_id.name if unit.media_type_id else None,
                    'active': unit.active,
                }
                media_unit_list.append(unit_data)

            # Return the data in JSON format
            return request.make_response(json.dumps({'status': 200, 'data': media_unit_list}), headers={'Content-Type': 'application/json'})

        except Exception as e:
            return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers={'Content-Type': 'application/json'})

    @http.route('/api/get_media_with_units', type='http', auth='user', methods=['GET'], csrf=False)
    def get_media_with_units(self, **kwargs):
        try:
            # Query the op.media model
            media_records = request.env['op.media'].sudo().search([])

            # Prepare the data to be returned
            media_list = []
            for media in media_records:
                media_data = {
                    'id': media.id,
                    'name': media.name,
                    'isbn': media.isbn,
                    'tags': [tag.name for tag in media.tags],
                    'authors': [author.name for author in media.author_ids],
                    'edition': media.edition,
                    'description': media.description,
                    'publishers': [publisher.name for publisher in media.publisher_ids],
                    'courses': [course.name for course in media.course_ids],
                    'subjects': [subject.name for subject in media.subject_ids],
                    'internal_code': media.internal_code,
                    'media_type': media.media_type_id.name if media.media_type_id else None,
                    'active': media.active,
                    'units': []
                }

                # Query the op.media.unit model for units related to the current media
                media_units = request.env['op.media.unit'].sudo().search([('media_id', '=', media.id)])
                for unit in media_units:
                    unit_data = {
                        'id': unit.id,
                        'name': unit.name,
                        'barcode': unit.barcode,
                        'state': unit.state,
                        'active': unit.active,
                    }
                    media_data['units'].append(unit_data)

                media_list.append(media_data)

            # Return the data in JSON format
            return request.make_response(json.dumps({'status': 200, 'data': media_list}), headers={'Content-Type': 'application/json'})

        except Exception as e:
            return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers={'Content-Type': 'application/json'})



    # @http.route('/api/get_queue_user', type='http', auth='user', methods=['GET'], csrf=False)
    # def get_media_queue(self, **kwargs):
    #     try:
    #         user_id = request.env.uid
    #         one_week_ago = datetime.now() - timedelta(weeks=1)
            
    #         media_queue_records = request.env['op.media.queue'].sudo().search([
    #             ('user_id', '=', user_id),
    #             ('date_to', '>=', one_week_ago.strftime('%Y-%m-%d'))
    #         ])

    #         media_queue_list = []
    #         for queue in media_queue_records:
    #             queue_data = {
    #                 'id': queue.id,
    #                 'sequence_no': queue.name,
    #                 'partner_id': queue.user_id.partner_id.id,
    #                 'partner_name': queue.user_id.partner_id.name,
    #                 'media_id': queue.media_id.id,
    #                 'media_name': queue.media_id.name,
    #                 'date_from': queue.date_from.strftime('%Y-%m-%d') if queue.date_from else None,
    #                 'date_to': queue.date_to.strftime('%Y-%m-%d') if queue.date_to else None,
    #                 'state': queue.state,
    #                 'active': queue.active,
    #             }
    #             media_queue_list.append(queue_data)

    #         return request.make_response(json.dumps({'status': 200, 'data': media_queue_list}), headers={'Content-Type': 'application/json'})

    #     except Exception as e:
    #         return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers={'Content-Type': 'application/json'})



    @http.route('/api/get_queue_user', type='http', auth='user', methods=['GET'], csrf=False)
    def get_media_queue(self, **kwargs):
        try:
            one_week_ago = datetime.today() - timedelta(days=7)
            user_id = request.env.uid
            media_queue_records = request.env['op.media.queue'].sudo().search([
                ('user_id', '=', user_id),
                ('date_from', '>=', one_week_ago.strftime('%Y-%m-%d'))
            ])

            media_queue_list = []
            for queue in media_queue_records:
                queue_data = {
                    'id': queue.id,
                    'sequence_no': queue.name,
                    'partner_id': queue.user_id.partner_id.id,
                    'partner_name': queue.user_id.partner_id.name,
                    'media_id': queue.media_id.id,
                    'media_name': queue.media_id.name,
                    'date_from': queue.date_from.strftime('%Y-%m-%d') if queue.date_from else None,
                    'date_to': queue.date_to.strftime('%Y-%m-%d') if queue.date_to else None,
                    'state': queue.state,
                    'active': queue.active,
                }
                media_queue_list.append(queue_data)

            # Calculate the total number of media items in the queue
            total_media_count = len(media_queue_list)

            response_data = {
                'status': 200,
                'total_media_count': total_media_count,
                'data': media_queue_list
            }

            return request.make_response(json.dumps(response_data), headers={'Content-Type': 'application/json'})

        except Exception as e:
            _logger.error(f"Error in get_media_queue: {str(e)}")
            return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers={'Content-Type': 'application/json'})
    
    
    @http.route('/api/get_media_status', type='http', auth='user', methods=['GET'], csrf=False)
    def get_media_status(self, **kwargs):
        try:
            media_records = request.env['op.media'].sudo().search([])

            media_list = []
            for media in media_records:
                media_status = 'available' if any(unit.state == 'available' for unit in media.unit_ids) else 'not available'
                
                media_data = {
                    'id': media.id,
                    'name': media.name,
                    'isbn': media.isbn,
                    'tags': [tag.name for tag in media.tags],
                    'authors': [author.name for author in media.author_ids],
                    'edition': media.edition,
                    'description': media.description,
                    'publishers': [publisher.name for publisher in media.publisher_ids],
                    'courses': [course.name for course in media.course_ids],
                    'subjects': [subject.name for subject in media.subject_ids],
                    'internal_code': media.internal_code,
                    'media_type': media.media_type_id.name if media.media_type_id else None,
                    'status': media_status,
                }
                media_list.append(media_data)

            return request.make_response(json.dumps({'status': 200, 'data': media_list}), headers={'Content-Type': 'application/json'})

        except Exception as e:
            return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers={'Content-Type': 'application/json'})



    # @http.route('/api/create_media_queue', type='http', auth='user', methods=['POST'], csrf=False)
    # def create_media_queue(self, **kwargs):
    #     try:
    #         user_id = request.env.uid

    #         media_id = kwargs.get('media_id')
    #         date_from = kwargs.get('date_from')
    #         date_to = kwargs.get('date_to')

    #         if not media_id or not date_from or not date_to:
    #             return request.make_response(json.dumps({'status': 400, 'message': 'Missing required fields'}), headers={'Content-Type': 'application/json'})

    #         media_queue_data = {
    #             'media_id': media_id,
    #             'date_from': date_from,
    #             'date_to': date_to,
    #             'user_id': user_id,
    #         }

    #         media_queue = request.env['op.media.queue'].sudo().create(media_queue_data)

    #         return request.make_response(json.dumps({'status': 200, 'message': 'Media Queue created successfully', 'data': media_queue.id}), headers={'Content-Type': 'application/json'})

    #     except Exception as e:
    #         return request.make_response(json.dumps({'status': 500, 'message': str(e)}), headers={'Content-Type': 'application/json'})

    @http.route('/api/create_media_queue', type='json', auth='user', methods=['POST'], csrf=False)
    def create_media_queue(self, **kwargs):
        try:
            user_id = request.env.uid

            media_id = request.jsonrequest.get('media_id')
            date_from = request.jsonrequest.get('date_from')
            date_to = request.jsonrequest.get('date_to')

            # if not media_id or not date_from or not date_to:
            #     return {
            #         'status': 400,
            #         'message': 'Missing required fields'
            #     }

            missing_fields = []

            if not media_id:
                missing_fields.append('media_id')
            if not date_from:
                missing_fields.append('date_from')
            if not date_to:
                missing_fields.append('date_to')

            if missing_fields:
                return {
                    'status': 400,
                    'message': 'Missing required fields: ' + ', '.join(missing_fields)
                }

            media_queue_data = {
                'media_id': media_id,
                'date_from': date_from,
                'date_to': date_to,
                'user_id': user_id,
            }

            media_queue = request.env['op.media.queue'].sudo().create(media_queue_data)

            return {
                'status': 200,
                'message': 'Media Queue created successfully',
                'data': media_queue.id
            }

        except Exception as e:
            return {
                'status': 500,
                'message': str(e)
            }



    @http.route('/api/create_queue', type='json', auth='user', methods=['POST'])
    def create_queue(self, **kwargs):
        # Get the current logged-in user
        user_id = request.env.uid
        _logger.info(f"Request headers: {request.httprequest.headers}")
        _logger.info(f"Request body: {request.httprequest.get_data()}")

        # Parse the JSON data from the request body
        try:
            data = json.loads(request.httprequest.get_data())
        except json.JSONDecodeError:
            return {
                'status': 'error',
                'message': 'Invalid JSON data'
            }

        _logger.info(f"Parsed data: {data}")

        # Extract the required parameters from the parsed data
        media_id = data.get('media_id')
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        # Validate the input parameters
        if not media_id or not date_from or not date_to:
            return {
                'status': 'error',
                'message': 'Missing required parameters'
            }

        # Create the media queue record
        try:
            media_queue = request.env['op.media.queue'].create({
                'media_id': media_id,
                'date_from': date_from,
                'date_to': date_to,
                'user_id': user_id
            })
            return {
                'status': 'success',
                'message': 'Media queue created successfully',
                'media_queue_id': media_queue.id
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }