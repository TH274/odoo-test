from odoo import models, fields, api, _

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'

    reference = fields.Char(string='Reference', default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patients', string='Patient', required=True)
    appointment_date = fields.Datetime(string='Appointment Date', required=True)
    notes = fields.Text(string='Notes')
    state = fields.Selection(
        [('draft', 'Draft'), 
         ('confirm', 'Confirmed'), 
         ('ongoing', 'Ongoing'), 
         ('done', 'Done'), 
         ('cancel', 'Cancelled')],
        string='Status',
        default='draft',
        tracking=True
    )
    appointment_line_ids = fields.One2many('hospital.appointment.line', 'appointment_id', string='Appointment Lines')

    @api.model
    def create(self, vals):
        if not vals.get('reference') or vals['reference'] == 'New':
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        return super().create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'

    class HospitalAppointmentLine(models.Model):
        _name = 'hospital.appointment.line'
        _description = 'Hospital Appointment Lines'

        product_id = fields.Many2one('product.product', string='Product', required=True)
        qty = fields.Float(string='Quantity', required=True)
        appointment_id = fields.Many2one('hospital.appointment', string='Appointment', required=True)