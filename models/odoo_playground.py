from odoo import fields,api,models
from odoo.tools.safe_eval import safe_eval

class OdooPlayGround(models.Model):
    _name = 'odoo.playground'
    _description = 'Odoo PlayGround'
    DEFAULT_NEW_VARIABLES="""
    #available varaibles
    """
    model_id=fields.Many2one('ir.model',string='Model')
    code=fields.Text(string="Code" ,default=DEFAULT_NEW_VARIABLES)
    result=fields.Text(string="Result")

    def action_clear(self):
        self.result=''
        self.code=''


    def action_execute(self):
        try:
            if self.model_id:
                model=self.env[self.model_id.model]
            else:
                model=self
            if self.code:
                self.result=safe_eval(self.code.strip(),{'self':model},mode="eval")
            else:
                self.result="Enter Some Codes to Evaluate"
        except Exception as e:
            self.result=str(e)
