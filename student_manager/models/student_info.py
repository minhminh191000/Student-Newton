from odoo import models, fields, api
from odoo.exceptions import ValidationError
import  re
class Student(models.Model):
    _name = 'student_module.student' # ten bang hien thi trong db la student_module_student
    _description = 'Student Information'
    _inherit = ['mail.thread','mail.activity.mixin','avatar.mixin']

    name = fields.Char(string='Name')
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    id_student = fields.Char(string='ID Student', required=True,unique=True)
    guardian_name = fields.Char(string='Name of Guardian')
    guardian_phone = fields.Char(string='Phone of Guardian',required=True)
    guardian_email = fields.Char(string='Email of Guardian',required=True)
    guardian_relationship = fields.Selection([('parent', 'Parent'), ('sibling', 'Sibling'), ('relative', 'Relative')],
                                             string='Guardian RelationShip', required=True)
    address = fields.Char(string='Home Address')
    avatar = fields.Image(string='Avatar')
    avatar_url = fields.Char(compute='_compute_avatar_url')
    classroom_id = fields.Many2many('student_module.classroom', string='Class')
    exams = fields.One2many('student_module.exam', 'student_id', string='Exams')

    # Login Fields
    login = fields.Char(string='Login', readonly=True, copy=False)
    password = fields.Char(string='Password', readonly=True, copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Related Partner', required=True, ondelete='cascade')

    user_id = fields.Many2one(comodel_name='res.userss', string='Students')


    # Check if student id is unique
    _sql_constraints = [('id_student', 'unique(id_student)', 'This student id is already exist!!!')]
    
    # description = fields.(string='Description')

    # Check guardian phone valid
    @api.constrains('guardian_phone')
    def check_phonenumber(self):
        for rec in self:
            if not re.match("^\\d{8,11}$", rec.guardian_phone):
                raise ValidationError("Enter valid 10 digits Mobile number")

    # Check guardian email valid
    @api.constrains('guardian_email')
    def _check_valid_email(self):
        for rec in self:
            if not re.match('(\w+[.|\w])*@(\w+[.])*\w+', rec.guardian_email):
                raise ValidationError("Wrong email format")
    @api.model
    def create(self, vals):
        # Generate a login based on the student's name
        login = vals.get('id_student').lower().replace(' ', '.')
        vals['login'] = login

        partner = self.env['res.partner'].create({
            'name': vals.get('name'),
            'email': vals.get('guardian_email'),
            'phone': vals.get('guardian_phone'),
        })
        vals['partner_id'] = partner.id

        student = super().create(vals)

        # Create the user account
        user_vals = {
            'name': vals.get('name'),
            'login': login,
            'password': login,  # You can generate a more secure password here
            'email': vals.get('email'),
            'partner_id': partner.id,
        }
        try:
            user = self.env['res.users'].create(user_vals)
            student.write({'user_id': [(4, user.id)]})
            group = self.env.ref('student_manager.group_student_manager')
            user.write({'groups_id': [(4, group.id)]})

        except Exception as e:
            raise ValidationError("Error creating user account: %s" % str(e))

        return student