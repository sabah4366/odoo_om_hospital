from odoo import api,fields,models,_
class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name=fields.Char(string="Name")
    active=fields.Boolean(string="Active",default=True)
    color=fields.Integer(string="Color")
    color_2=fields.Char(string="Color 2")
    sequence =fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)",self.name)
        self.sequence=10
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('unique_name','unique (name)','Name must unique'),
        ('check_sequence','check(sequence > 0)','Sequence must be non zero')
    ]
