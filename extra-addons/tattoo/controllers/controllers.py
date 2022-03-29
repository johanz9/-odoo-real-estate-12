# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class Tattoo(http.Controller):
    # READ All SESSIONS
    @http.route('/tattoo/sessions', type='json', auth='user', methods=['GET'])
    def get_sessions(self):
        _logger.info("[SESSION] HTTP Get received a request")
        sessions_rec = request.env["tattoo.session"].sudo().search([])
        sessions = []
        for session in sessions_rec:
            sessions.append({
                "id": session.id,
                "client_id": session.client_id.id,
                "design_id": session.design_id.id,
                "duration": session.duration,
                "session_cost": session.session_cost,
                "state": session.state,
            })
        data = {"status": 200, "response": sessions, "message": "Success"}
        _logger.info("[SESSION] HTTP Get all sessions request successfully")
        return data

    # READ A SESSION
    @http.route('/tattoo/sessions/<int:session_id>', type='json', auth='user', methods=['GET'])
    def get_session(self, session_id, **kwargs):
        print(kwargs)

        _logger.info("[SESSION] HTTP Get a sessions receive a request for session_id %s" % session_id)
        session_rec = request.env["tattoo.session"].sudo().browse(session_id)
        session = {
            "id": session_rec.id,
            "client_id": session_rec.client_id.id,
            "design_id": session_rec.design_id.id,
            "duration": session_rec.duration,
            "session_cost": session_rec.session_cost,
            "state": session_rec.state,
        }
        data = {"status": 200, "response": session, "message": "Success"}
        _logger.info("[SESSION] HTTP Get request done successfully for session_id %s" % session_id)
        return data

    # CREATE A SESSION
    @http.route('/tattoo/sessions', type='json', auth='user', methods=['POST'])
    def create_session(self, **rec):
        _logger.info("[SESSION] HTTP Post received data: {} ".format(rec))
        if request.jsonrequest:
            vals = {
                "client_id": rec["client_id"],
                "design_id": rec["design_id"],
            }
            session_rec = request.env["tattoo.session"].sudo().create(vals)
            args = {"ID": session_rec.id, "success": True, "message": "Success"}
            _logger.info("[SESSION] created successfully!")

        return args

    # UPDATE A SESSION
    @http.route('/tattoo/sessions/<int:session_id>', type='json', auth='user', methods=['PUT'])
    def update_session(self, session_id, **rec):
        _logger.info("[SESSION] HTTP PUT received data: {} ".format(rec))
        if request.jsonrequest:
            session_rec = request.env["tattoo.session"].sudo().browse(session_id)
            session_rec.sudo().write(rec)
            args = {"success": True, "message": "Session: {} updated Successfully".format(session_rec.id)}
            _logger.info("[SESSION] updated successfully!")
        return args

    # DELETE A SESSION
    @http.route('/tattoo/sessions/<int:session_id>', type='json', auth='user', methods=['DELETE'])
    def update_session(self, session_id, **rec):
        _logger.info("[SESSION] HTTP DELETE received data: {} ".format(rec))
        if request.jsonrequest:
            session_rec = request.env["tattoo.session"].sudo().browse(session_id)
            session_rec.sudo().unlink()
            args = {"success": True, "message": "Session: {} deleted Successfully".format(session_rec.id)}
            _logger.info("[SESSION] deleted successfully!")
        return args
