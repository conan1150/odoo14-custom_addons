# -*- coding: utf-8 -*-

from odoo import models, fields, api


class containers(models.Model):
    _name = 'transportation.container'
    _description = 'transportation.container'

    name = fields.Char()