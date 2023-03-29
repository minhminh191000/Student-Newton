from odoo import models, fields, api
from odoo.exceptions import ValidationError
# goi cac libary python

class Assigment(models.Model):
    _name = 'student_module.assignment'
    _description = 'Assignment'
    _inherit = ['mail.thread','mail.activity.mixin']
    subject_id = fields.Many2many('student_module.subject', string='Subject', required=True)
    classroom_id = fields.Many2one('student_module.classroom', string='Classroom', required=True)
    date = fields.Date(string='Date')


class Teacher(models.Model):
    _name = 'student_module.teacher'
    _description = 'Teacher Information'
    _inherit = ['mail.thread','mail.activity.mixin','avatar.mixin']

    name = fields.Char(string='Name')
    id_teacher = fields.Char(string='ID Teacher', required=True,unique=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    image = fields.Image(string='Avatar')
    homeroom_class = fields.Many2one('student_module.classroom',string='Homeroom Class', copy=False, unique=True)
    assignment = fields.Many2many('student_module.assignment', string='Assignment', copy=False, unique=True)

    # Login Fields
    login = fields.Char(string='Login', readonly=True, copy=False)
    password = fields.Char(string='Password', readonly=True, copy=False)

    _sql_constraints = [
        ('id_teacher_unique',
            'UNIQUE(id_teacher)',
            "ID Teacher must be unique!"),
        ('homeroom_class_unique',
            'UNIQUE(homeroom_class)',
            "The class has a homeroom teacher"),
        ('assignment_unique',
            'UNIQUE(assignment)',
            "The teacher has an assignment"),
    ]
    
    
    # description = fields.(string='Description')
    @api.model 
    def create(self, vals):
        # Generate a login based on the student's name
        login = vals.get('id_teacher').lower().replace(' ', '.')
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
