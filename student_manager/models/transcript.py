from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Transcript(models.Model):
    _name = 'academic_manager.transcript'
    _describe = "student's transcript"

    # Student transcript
    classroom = fields.One2Many('academic_manager.classroom', 'id_classroom', string='Class')
    student = fields.One2Many('academic_manager.classroom', 'student', string="Student's Name")
    subject = fields.One2Many('academic_manager.subject', 'name', string='Subject')

    # 15mn test
    first_15mn_test = fields.Interger(string="1st 15 Minutes Test", default='0')
    second_15mn_test = fields.Interger(string="2nd 15 Minutes Test", default='0')
    third_15mn_test = fields.Interger(string="3rd 15 Minutes Test", default='0')
    # Periodic test
    first_periodic_test = fields.Interger(string="1st Periodic Test", default='0')
    second_periodic_test = fields.Interger(string="1st Periodic Test", default='0')
    # Final test
    final_test = fields.Interger(string="Final Test", default='0')

    # Average
    average = (first_15mn_test + second_15mn_test + third_15mn_test + first_periodic_test*2 + second_periodic_test*2 + final_test*3)/10


    @api.constrains(first_15mn_test)
    def Check_first_15mn_test_Valid(self):
        for score in self:
            if score.first_15mn_test < 0 | score.first_15mn_test > 10:
                raise ValidationError("Wrong score format!")
    
    @api.constrains(second_15mn_test)
    def Check_second_15mn_test_Valid(self):
        for score in self:
            if score.second_15mn_test < 0 | score.second_15mn_test > 10:
                raise ValidationError("Wrong score format!")
    
    @api.constrains(third_15mn_test)
    def Check_third_15mn_test_Valid(self):
        for score in self:
            if score.third_15mn_test < 0 | score.third_15mn_test > 10:
                raise ValidationError("Wrong score format!")
    
    @api.constrains(first_periodic_test)
    def Check_first_periodic_test_Valid(self):
        for score in self:
            if score.first_periodic_test < 0 | score.first_periodic_test > 10:
                raise ValidationError("Wrong score format!")
    
    @api.constrains(second_periodic_test)
    def Check_second_periodic_test_Valid(self):
        for score in self:
            if score.second_periodic_test < 0 | score.second_periodic_test > 10:
                raise ValidationError("Wrong score format!")
    
    @api.constrains(final_test)
    def Check_final_test_Valid(self):
        for score in self:
            if score.final_test < 0 | score.final_test > 10:
                raise ValidationError("Wrong score format!")




