from odoo import models, fields, api
from odoo.exceptions import ValidationError
# goi cac libary python


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
    classroom_ids = fields.Many2many('student_module.classroom', string='Class Taught')
    subject_ids = fields.Many2many('student_module.subject', string='Teaching Subjects')
    address_id = fields.Many2one('res.partner', string='Home Address')
    

    # Login Fields
    login = fields.Char(string='Login', readonly=True, copy=False)
    password = fields.Char(string='Password', readonly=True, copy=False)

    _sql_constraints = [('id_teacher', 'unique(id_teacher)', 'This teacher id is already exist!!!')]

    @api.constrains('phone')
    def check_phonenumber(self):
        for rec in self:   
            if not re.match("^\\d{8,11}$", rec.phone):
                raise ValidationError("Enter valid 10 digits Mobile number")
        
    @api.constrains('guardemailian_email')
    def _check_valid_email(self):
        for rec in self:
            if not re.match('(\w+[.|\w])*@(\w+[.])*\w+', rec.email):
                raise ValidationError("Wrong email format")
    
    
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
