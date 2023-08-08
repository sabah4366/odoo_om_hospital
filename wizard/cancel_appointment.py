from odoo import api,fields,models,_
import datetime
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import  date
class CancelAppointmentWizard(models.TransientModel):
    _name = 'appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        res=super(CancelAppointmentWizard,self).default_get(fields)
        res['cancel_date']=datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id']=self.env.context.get('active_id')
        return res

    appointment_id=fields.Many2one('hospital.appointment',string="Apponintment" ,required=True )
    reason=fields.Text(string="Reason")
    cancel_date=fields.Date(string="Cancel Date")

    def cancel_appointment(self):
        cancel_day=self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        allowed_date=self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        if cancel_day != 0 and  allowed_date < date.today():
            raise ValidationError(_("Sorry cancellation is not allowded for this booking!"))
        self.appointment_id.state='cancel'

        return {
            'type':'ir.actions.client',
            'tag':'reload',
        }


        # return  {
        #     'type': 'ir.actions.act_window',
        #     'view_mode':'form',
        #     'res_model':'appointment.wizard',
        #     'target':'new',
        #     'res_id':self.id
        # }



        # return {
        #     'type':'ir.actions.client',
        #     'tag':'reload',
        # }
        # 'tag' : 'reload' => automatic reloading page

