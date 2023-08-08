from odoo import models,api,fields,_
from odoo.exceptions import ValidationError
import random
class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Patient Appointment"
    _rec_name='name'
    _order='id desc'

    name=fields.Char(string="Sequence" ,default='New' , tracking=True )
    patient_id=fields.Many2one('hospital.patient',string="Patient" , tracking='1' , required=True)
    appointment_time=fields.Datetime(string="Appointment Time" , default=fields.Datetime.now)
    booking_date=fields.Date(string="Booking Date",default=fields.Date.context_today , tracking='2')
    gender=fields.Selection(related="patient_id.gender")
    ref=fields.Char(string="Reference")
    doctor_id=fields.Many2one('res.users',string='Doctor' ,tracking='4')
    prescription = fields.Html(string="Prescription")
    pharmacy_ids=fields.One2many('appointment.pharmacy','appointment_id',string="Pharmacy")
    hide_sales_price=fields.Boolean(string="Hide Sales Price")
    operation=fields.Many2one('hospital.operation',string="Operation")
    progress=fields.Integer(string="Progress" , compute='_compute_progress')
    duration=fields.Float(string="Duration" , tracking='6')
    full_total=fields.Float(string="Total" , compute='_compute_full_total')


    company_id=fields.Many2one('res.company', string="Company" ,default=lambda self:self.env.company )
    currency_id=fields.Many2one('res.currency' , related='company_id.currency_id')
    priority = fields.Selection([
        ("0", "Normal"),
        ("1", "Low"),
        ("2", "High"),
        ("3", "Very High")], string="Priority")
    state = fields.Selection([
        ("draft", "Draft"),
        ("in consultation", "In Consultation"),
        ("done", "Done"),
        ("cancel", "Cancelled")], string="State",default="draft",required=True,tracking='9')

    def sl_number(self):
        sl_no=0
        for rec in self.pharmacy_ids:
            sl_no+=1
            rec.sl_no=sl_no

    def action_send_mail(self):
        template=self.env.ref('om_hospital.appointment_email_template')
        for rec in self:
            if rec.patient_id.email:
                # send_mail() method is used to send the appointment template to the mail
                #force_send=True
                template.send_mail(rec.id,force_send=True)
            else:
                raise ValidationError("Email not specified!!")

    @api.depends('pharmacy_ids')
    def _compute_full_total(self):
        for rec in self:
            rec.full_total = sum(rec.pharmacy_ids.mapped('subtotal'))


    def unlink(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        for rec in self:
            if rec.state != 'draft':    
                raise ValidationError(_("You can delete appointment only in 'Draft' state"))
            return super(HospitalAppointment,self).unlink()


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref=self.patient_id.ref


    def action_test(self):
        return {
            'type':'ir.actions.act_url',
            'target':'self',
            'url':'https://github.com/'
        }

    def action_notification(self):
        action=self.env.ref('om_hospital.action_hospital_patient')
        return{
            'type':'ir.actions.client',
            'tag':'display_notification',
            'params':{
                'title':('Click open patient records'),
                'message':'%s',
                'links':[{
                    'label':self.patient_id.name,
                    'url':f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient'
                }],
                'sticky':True,
                'next':{
                    'type':'ir.actions.act_window',
                    'res_model':'hospital.patient',
                    'res_id':self.patient_id.id,
                    'views':[(False,'form')]
                }
            }
        }

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        res=super(HospitalAppointment, self).create(vals)
        res.sl_number()
        return res

    def write(self, vals):
        if not self.name or self.name == 'New':
            vals['name']=self.env['ir.sequence'].next_by_code('hospital.appointment')
        res=super(HospitalAppointment,self).write(vals)
        self.sl_number()
        return res
    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress=random.randrange(0,25)
            elif rec.state == 'in consultation':
                progress=random.randrange(26,99)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    def action_whatsapp_message(self):
        if not self.patient_id.phone:
            raise ValidationError('Phone number is not specified')
        message='Hai %s Your Appointment number is %s' % (self.patient_id.name,self.name)
        whatsapp_api_url='https://api.whatsapp.com/send?phone=%s&text=%s ' %  (self.patient_id.phone,message)
        return {
            'type': 'ir.actions.act_url',
            'target':'self',
            'url':whatsapp_api_url
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state='in consultation'

    def action_done(self):
        for rec in self:
            rec.state='done'

        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Congratulations!!',
                'tyepe': 'rainbow_man'
            }
        }

    def action_cancel(self):
        action=self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state='draft'



class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy"
    _description = "Patient Appointment"

    product_id=fields.Many2one('product.product',string='Product',required=True)
    price_unit=fields.Float(string="Price",related='product_id.list_price' , digits="Product Price")
    qty=fields.Integer(string='Quantity',default='10')
    appointment_id=fields.Many2one('hospital.appointment',string='Appointment')
    currency_id=fields.Many2one('res.currency',related='appointment_id.currency_id')
    subtotal=fields.Monetary(string="Subtotal" , compute="_compute_subtotal", currency_field='currency_id')
    sl_no=fields.Integer(string="SL No.")




    @api.depends('qty','price_unit')
    def _compute_subtotal(self):
        for rec in  self:
            rec.subtotal = rec.price_unit * rec.qty
