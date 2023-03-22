from odoo import models, fields

class Exam(models.Model):
    # 
    _name = 'student_module.exam' # tao bang trong database
    _description = 'Exam'
    _inherit = ['mail.thread','mail.activity.mixin']

    student_id = fields.Many2one('student_module.student', string='Student', required=True)
    subject_id = fields.Many2one('student_module.subject', string='Subject', required=True)

    assignment_type = fields.Selection([
        ('15p', '15 Minutes Test'),
        ('mieng', 'Oral Test'),
        ('1tiet', 'Periodic Test'),
        ('cuoiki', 'Final Test')
    ], string="Type", required=True)
    
    score = fields.Float(string='Score')
    date = fields.Date(string='Exam Date')

class Subject(models.Model):
    _name = 'student_module.subject'
    _description = 'Subject Information'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
