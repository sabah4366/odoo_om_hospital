from odoo import fields,models

class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.reporting.wizard'
    _description = 'Search Appointment Wizard'

    patient_id=fields.Many2one('hospital.patient' , string="Patient")
    date_from=fields.Date(string="Date From")
    date_to=fields.Date(string="Date To")


    def action_print_report(self):
        # #self.read()[0] means current record set that we are passsing in wizard
        # domain=[]
        # patient_id=self.patient_id
        # date_from=self.date_from
        # date_to=self.date_to
        # if patient_id:
        #     domain+=[('patient_id','=',self.patient_id.id)]
        # if date_from:
        #     domain+=[('booking_date','>=',date_from)]
        # if date_to:
        #     domain+=[('booking_date','<=',date_to)]
        #
        # appointments = self.env['hospital.appointment'].search_read(domain)
        # data={
        #     'form':self.read()[0],
        #     'appointments':appointments
        # }

        # self.env.ref('om_hospital.action_report_appointment').report_action(self, data=data)
        return 'jai'