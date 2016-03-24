from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
        
class LegendData(models.Model):
	line_id = models.CharField(max_length=200)
	line_name = models.CharField(max_length=200)

	def __str__(self):
		return self.line_id

class ContribSourcesByParty(models.Model):
	interest_category = models.CharField(max_length=200)
	democrat = models.FloatField()
	republican = models.FloatField()
	
	def __str__(self):
		return self.interest_category

### For the candidate table, will be joined to contributor data
### one record for each time someone ran for office
class CandidateData(models.Model):
	district = models.IntegerField()
	candidate = models.CharField(max_length=200)
	house = models.CharField(max_length=200)
	party = models.CharField(max_length=200)
	year_ran = models.DateField(null=True)
	won = models.IntegerField()
	
	def __str__(self):
		return self.candidate + " " + str(self.year_ran)

### For candidate contributions
### Join field will be on cadidate name (from wisc democracy campaign)
class ContributorData(models.Model):
	#candidate_key = models.ForeignKey(CandidateData, on_delete=models.CASCADE)
	date = models.DateField(null=True)
	candidate = models.CharField(max_length=200)
	contributor = models.CharField(max_length=200)
	city_state_zip = models.CharField(max_length=200)
	employer = models.CharField(max_length=200)
	interest_category = models.CharField(max_length=200)
	amount = models.FloatField()
	cumulative = models.FloatField(default=0)
	
	def __str__(self):
		return self.contributor

		
	
	



