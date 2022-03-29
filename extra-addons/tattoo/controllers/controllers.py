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
        _logger.info("HTTP Get all sessions receive a request")
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
        _logger.info("HTTP Get all sessions request successfully")
        return data

    # READ A SESSION
    @http.route('/tattoo/sessions/<int:session_id>', type='json', auth='user', methods=['GET'])
    def get_session(self, session_id):
        _logger.info("HTTP Get a sessions receive a request for session_id %s" % session_id)
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
        _logger.info("HTTP Get a sessions request done successfully for session_id %s" % session_id)
        return data

    # CREATE A SESSION
    @http.route('/tattoo/sessions', type='json', auth='user', methods=['POST'])
    def create_session(self, **rec):
        _logger.info("HTTP received data: {} ".format(rec))
        if request.jsonrequest:
            print(rec)

            vals = {
                "client_id": rec["client_id"],
                "design_id": rec["design_id"],
            }
            session_rec = request.env["tattoo.session"].sudo().create(vals)
            args = {"ID": session_rec.id, "success": True, "message": "Success"}
            _logger.info("Session created successfully!")

        return args
