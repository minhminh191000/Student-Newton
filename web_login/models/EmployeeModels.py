
from odoo import models, fields


class EmployeeModels(models.Model):
    _name = "weather_employeemodels"
    _description = 'weather'
    
    name = fields.Char(string='Name', required=True)
    image = fields.Binary(string='Image', attachment=True)
    gender =  fields.Selection([('male', 'Male'),('female','Female')],string='Gender' ,default='male')
    day_of_birth = fields.Datetime(string = 'day_of_birth')
    


