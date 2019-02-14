from django.db import models
from patient.models import Patient
from datetime import  datetime
# from django.contrib.auth.models import
from physician.models import Physician
from hospital.models import Hospital
class MedicationList(models.Model):

    """
    This defines the medication list that the patient has had for that disease

    """
    def __init__(self, *args, **kwargs):
      super(MedicationList,self).__init__(*args, **kwargs)
      self.__model_label__ = "MedicationList"
      self._parent_model = 'Disease'

    medication = models.CharField(max_length=100,
                                  help_text="Only Generic Names.."
                                  )
    strength = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100,
                              help_text="OD, BD, TDS, QID, HS, SOS, PID etc.."
                              )
    prescription_date = models.DateField(auto_now_add=False)
    prescribed_by = models.CharField(max_length=100,
                                     choices=(("internal", "Internal Doctor"),
                                              ("external", "External Doctor")
                                                  ),
                                     default = "Internal"
                                     )
    currently_active = models.BooleanField(default=True)



    def __unicode__(self):
        return "%s" % (self.medication)



class MedicalFile(models.Model):
    parent_hospital=models.ForeignKey(Hospital,null=True)
    patient=models.ForeignKey(Patient,related_name='medical_file')
    date_of_addmition=models.DateField()
    date_of_discharge=models.DateField(blank=True,null=True)
    open=models.BooleanField(default=0)
    ward=models.CharField(max_length=4)
    room=models.CharField(max_length=4)
    bed=models.CharField(max_length=2)







    """
      This defines the Medical History that the patient has had .
    """
    #
    # def __init__(self, *args, **kwargs):
    #   super(MedicalHistory,self).__init__(*args, **kwargs)
    #   self.__model_label__ = "medical_history"
    #   self._parent_model = 'patient'
    #
    # had_infectious_disease = models.BooleanField(default=None)
    # had_allergic_disease = models.BooleanField(default = None)
    # pregnancy_warning = models.BooleanField(default = None)
    #
    # patient_detail = models.OneToOneField(Patient,related_name='history') # surgery records are connected accordingly,
    #
    #
    # patient_current_status = models.TextField("Status",
    #                           max_length=500,
    #                           null=True,
    #                           blank=True
    #                           )
    #
    # def __unicode__(self):
    #     return "%s" % (self.patient_detail)

class Disease(models.Model):
    def __init__(self, *args, **kwargs):
            super(Disease,self).__init__(*args, **kwargs)
            self.__model_label__ = "disease"
            self._parent_model = 'MedicalHistory'

    disease = models.CharField(max_length=100)
    severity = models.CharField(max_length=100)
    date_of_diagnosis = models.DateField(auto_now_add=False, null=True,blank=True)
    is_active = models.BooleanField("Active?",default=None)
    remarks = models.TextField(max_length=1000,
                               help_text="Any Other Remarks",
                               default="None"
                               )
    #icd 10 is the universal classification of diseases
    icd_10  = models.CharField("ICD 10", max_length=100,null=True, blank=True)

    disease_medication_list=models.OneToOneField(MedicationList)
    # medical_history=models.ForeignKey(MedicalHistory)


class Surgery(models.Model): # Surgery

    """
      This defines the Surgical History that the patient has had
    """

    def __init__(self, *args, **kwargs):
      super(Surgery,self).__init__(*args, **kwargs)
      self.__model_label__ = "Surgery"
      self._parent_model = 'MedicalHistory'


    base_condition_after_surgery = models.TextField("Base Condition",
                                      max_length=500,
                                      null=True,
                                      blank=True
                                      )
    description = models.TextField(max_length=1000,
                                  null=True,
                                  blank=True)
    classification = models.CharField(max_length=200)
    date_of_surgery = models.DateField(auto_now_add=False)

    healed = models.BooleanField(default=None)

    remarks = models.TextField(max_length=1000,help_text="Any Other Remarks",default="None" )

    icd_10 = models.CharField("ICD10", max_length=100, null=True, blank=True)
    icd_10_pcs = models.CharField("ICD10 PCS",max_length=100, null=True, blank=True)

    #patient_detail = models.ForeignKey(Patient)  -- migrated to Medical History : each medical history has surgery history
    # medical_history=models.ForeignKey(MedicalHistory)



    def __unicode__(self):
        return "%s,%s"%(self.classification,self.icd_10_pcs)




class Progress_notes_sheet(models.Model):
    medical_file=models.OneToOneField(MedicalFile,related_name='progress_note_sheet')
    date=models.DateField(auto_now_add=True)
    attending_physician=models.ForeignKey(Physician)


class Progress_note(models.Model):
    date=models.DateField(auto_now_add=True)
    treatment_progress=models.CharField(max_length=200,default='insert value')
    sheet=models.ForeignKey(Progress_notes_sheet,related_name='notes')
    physician=models.ForeignKey(Physician)

class Physician_order_sheet(models.Model):
    medical_file=models.OneToOneField(MedicalFile,related_name='physician_order_sheet')
    date=models.DateTimeField(auto_now_add=True,blank=True)
    attending_physician=models.ForeignKey(Physician)

class Order(models.Model):
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    order=models.CharField(max_length=200,default='insert value')
    sheet=models.ForeignKey(Physician_order_sheet,related_name='orders')
    physician=models.ForeignKey(Physician,related_name='orders')


class Unit_summary_sheet(models.Model):
    medical_file=models.OneToOneField(MedicalFile,related_name='unit_summary_sheet')
    attending_physician=models.ForeignKey(Physician,related_name='unit_summaries')
    other_physicians=models.ManyToManyField(Physician,related_name='summary_attend')
    chief_complaint_and_primary_diagnosis=models.CharField(max_length=200,default='insert value')
    final_diagnosis=models.CharField(max_length=200,default='insert value')
    medical_and_surgical_procedures=models.CharField(max_length=200,default='insert value')
    results_of_paraclinical_examinations=models.CharField(max_length=200,default='insert value')
    disease_progress=models.CharField(max_length=200,default='insert value')
    patient_condition_on_discharge=models.CharField(max_length=200,default='insert value')
    recommendations_after_discharge=models.CharField(max_length=200,default='insert value')
    recommendations_for_family_physician=models.CharField(max_length=200,default='insert value')


class  Medical_history_sheet(models.Model):
    medical_file=models.OneToOneField(MedicalFile,related_name='medical_history_sheet')
    attending_physician=models.ForeignKey(Physician,related_name='medical_history_sheets')
    chief_complain=models.CharField(max_length=200,default='insert value')
    history_of_present_illness=models.CharField(max_length=200,default='insert value')
    pass_diseases_history=models.CharField(max_length=200,default='insert value')
    current_drug_theraphy_and_other_addiction=models.CharField(max_length=200,default='insert value')
    allergy_to=models.CharField(max_length=200,default='insert value')
    family_history=models.CharField(max_length=200,default='insert value')
    summary=models.TextField(default='insert value')
    primary_dx=models.TextField(default='insert value')





class BaseDocument(models.Model):
    date=models.DateField()
    comment=models.CharField(max_length=200)

class X_ray_area(models.Model):
    area=models.CharField(max_length=20)


class X_ray_view(models.Model):
    view=models.CharField(max_length=20)

class Ct_area(models.Model):
    area=models.CharField(max_length=20)


class Mri_area(models.Model):
    area=models.CharField(max_length=20)

class Test_type(models.Model):
    type=models.CharField(max_length=20)
    desciption=models.CharField(max_length=100,null=True)





class X_ray(BaseDocument):
    image=models.ImageField(upload_to='x_rays')
    historyFile=models.ForeignKey(MedicalFile,related_name='x_ray')
    area=models.OneToOneField(X_ray_area)
    view=models.OneToOneField(X_ray_view)
    ADM_CHOICES=(('emg','Emergency'),('hosp','Hosp.'),('opd','O.P.D.'))
    kind_of_adm=models.CharField(max_length=10,choices=ADM_CHOICES)


class Ct(BaseDocument):
    image=models.ImageField(upload_to='cts')
    historyFile=models.ForeignKey(MedicalFile,related_name='ct')
    area=models.ForeignKey(Ct_area)
    CT_DESCRIPTION_CHOISES=(('1','With injection'),
                            ('0','Without injection'))

    description=models.CharField(max_length=20,choices=CT_DESCRIPTION_CHOISES)




class Mri(BaseDocument):
    image=models.ImageField(upload_to='mris')
    historyFile=models.ForeignKey(MedicalFile,related_name='mri')
    area=models.OneToOneField(Mri_area)



class Test(BaseDocument):
    image=models.ImageField(upload_to='tests')
    historyFile=models.ForeignKey(MedicalFile,related_name='test')











