# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_sessions(self):
        return self.env['opnacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('opnacademy.session',
        string="Sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}

class Course(models.Model):
   _name = 'opnacademy.course'
   _description = "Courses"
   
   name = fields.Char(string="Course Title", required=True, help="Name Of the Course")
   description = fields.Text()
   responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
   session_ids = fields.One2many('opnacademy.session','course_id', string="Sessions")
   participantcount = fields.Integer(compute='compute_count')
#   participant = fields.One2many('res.partner',id,domain="[('session_ids','=',)]"))


   def compute_count(self):
        for record in self:
            record.participantcount = self.env['res.partner'].search_count([('session_ids', '=', self.id)])


#   @api.multi
 #  def open_partner(self):
  #    return {
   #      'name':_('Participants'), 
    #     'domain':[('course_id', '=', self.id)],
     #    'view_type': 'form',
      #   'res_model': 'opnacademy.course',
       #  'view_id': False,
        # 'view_mode': 'tree,form',
         #'type': 'ir.actions.act_window',
      #}      
     


class Session(models.Model):
   _name = 'opnacademy.session'
   _description = "Sessions"
   _inherit = ['mail.thread' ,'mail.activity.mixin']
  
   name = fields.Char(required=True)
   start_date = fields.Date()
   duration = fields.Float(digits=(6,2), help="Duration in days")
   seats = fields.Integer(string="Number of Seats")
   instructor_id = fields.Many2one('res.partner', ondelete='cascade', string="Instructor",required='True')
   course_id = fields.Many2one('opnacademy.course', ondelete='cascade', string="Courses",required=True)
   attendee_ids = fields.Many2many('res.partner',string="Attendees")
   session_status = fields.Selection([
        ('Preperation', 'Preperation'),
        ('Progress', 'Progress'),
        ('Complete', 'Complete'),
    ], string='STATUS', default='Preperation')
   taken_seats = fields.Float(string="Filled Seats", compute='_taken_seats')



   @api.onchange('taken_seats','session_status')
   def chck_status(self):
      if self.taken_seats >= 50:
         self.write({
         'session_status': 'Progress'
          })
      else:
          self.write({
          'session_status': 'Preperation'
          })
             


   @api.depends('seats','attendee_ids')
   def _taken_seats(self):
       for r in self:
           if not r.seats:
              r.taken_seats = 0.0
           else:
              r.taken_seats =100.0*len(r.attendee_ids)/r.seats



   @api.onchange('seats','attendee_ids')
   def _verify_valid_seats(self):
       if self.seats < 0:
           return{
              'warning':{
                 'title': "Please Type Valid seat Value",
                  'message':"The Seats cannot be negative"                
               },
           }  

       if self.seats < len(self.attendee_ids):
           return{
              'warning':{
                 'title': "Too many attendees",
                  'message':"Please remove attendees or add more seats!"                
               },
           }  

            

class search1(models.Model):
   _inherit = 'opnacademy.course'
  
   def participantcounts(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Participants',
            'view_mode': 'tree',
            'res_model': 'res.partner',
            'domain': [('session_ids', '=', self.id)],
            'context': "{'create': False}"
        }

