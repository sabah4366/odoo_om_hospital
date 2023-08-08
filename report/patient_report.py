import base64
import io

from odoo import fields,models,api

class PatientReportXlsx(models.AbstractModel):
    _name = 'report.om_hospital.patient_report_details_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        format1 = workbook.add_format({'bold': True, 'bg_color': 'gray'})
        bold = workbook.add_format({'bold': True})
        format2 = workbook.add_format({'align': 'right'})
        row=0
        col=0
        sheet = workbook.add_worksheet('Book'[:31])
        for obj in patients:
            sheet.merge_range(row, col, row , col + 1, "Patient details",bold)
            sheet.set_column('A:C',15)
            patient_name=obj.name
            patient_dob = obj.date_of_birth
            patient_age = obj.age
            appointment_count=obj.appointment_count

            sheet.write(row + 7, col, "Ref",bold)
            sheet.write(row + 7, col +1 , "Age",bold)
            sheet.write(row + 7, col + 2, "date of Birth",bold)
            if obj.image:
                patient_image=io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row + 1,col,"image.png",{'image_data':patient_image, 'x_scale': 0.1,'y_scale': 0.1,})
            if patient_name:
                sheet.write(row + 8,col,patient_name)
            if patient_dob:
                sheet.write(row + 8, col + 1, patient_age)
            if patient_age:
                sheet.write(row + 8, col + 2, patient_dob.strftime('%d/%m/%Y'))


            sheet.write(row + 10,col,"SNO.",bold)
            sheet.write(row + 10, col + 1, "Reference", bold)
            sheet.write(row + 10, col + 2, "Date", bold)
            sheet.write(row + 10, col + 3, "Status", bold)
            sl_no=0
            for pat in patients.appointment_ids:
                row+=1
                sl_no+=1
                patient_ref=pat.name
                patient_date=pat.booking_date
                patient_status=pat.state
                if patient_ref:
                    sheet.write(row + 10, col, sl_no,format2)
                    sheet.write(row + 10,col + 1,patient_ref,format2)
                if patient_date:
                    sheet.write(row + 10,col + 2,patient_date.strftime('%d/%m/%Y'),format2)
                if patient_status:
                    sheet.write(row + 10,col + 3,patient_status,format2)
            if appointment_count:
                sheet.merge_range(row + 12, col, row + 12, col + 1, "Appointment Count", bold)
                sheet.merge_range(row + 12, col +2, row + 12, col + 3, appointment_count, bold)

