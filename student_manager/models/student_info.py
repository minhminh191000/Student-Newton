from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'student_module.student' # ten bang hien thi trong db la student_module_student
    _description = 'Student Information'
    _inherit = ['mail.thread','mail.activity.mixin','avatar.mixin']

    name = fields.Char(string='Name')
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    id_student = fields.Char(string='ID Student', required=True,unique=True)
    guardian_name = fields.Char(string='Name of Guardian')
    guardian_phone = fields.Char(string='Phone of Guardian')
    guardian_email = fields.Char(string='Email of Guardian')
    guardian_relationship = fields.Selection([('father', 'Father'), ('mother', 'Mother'), ('brother', 'Brother'), ('sister', 'Sister'), ('uncle', 'Uncle'), ('aunt', 'Aunt'), ('grandfather', 'Grandfather'), ('grandmother', 'Grandmother'), ('other', 'Other')], string='Guardian Relationship')
    address_id = fields.Many2one('res.partner', string='Home Address')
    avatar = fields.Image(string='Avatar')
    avatar_url = fields.Char(compute='_compute_avatar_url')
    classroom_id = fields.Many2many('student_module.classroom', string='Class')
    exams = fields.One2many('student_module.exam', 'student_id', string='Exams')

    # Login Fields
    login = fields.Char(string='Login', readonly=True, copy=False)
    password = fields.Char(string='Password', readonly=True, copy=False)
    
    
    # description = fields.(string='Description')
    @api.model
    def create(self, vals):
        # Generate a login based on the student's name
        login = vals.get('id_student').lower().replace(' ', '.')
        vals['login'] = login

        # Create the student record
        student = super().create(vals)

        # Create the user account
        user_vals = {
            'name': vals.get('name'),
            'login': login,
            'password': login,  # You can generate a more secure password here
            'email': vals.get('email'),
            # 'partner_id': student.partner_id.id,
        }
        try:
            self.env['res.users'].create(user_vals)
        except Exception as e:
            raise ValidationError("Error creating user account: %s" % str(e))

        return student