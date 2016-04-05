from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Post, LegendData, ContribSourcesByParty, ContributorData, CandidateData
from .forms import PostForm
import json
from datetime import date

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {"posts": posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, "blog/post_detail.html", {'post': post})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

def asm_leadership(request):
	return render(request, "blog/asm_leadership_graph.html", {})
	
def legend_data(request):
	obj = LegendData.objects.all()
	data = list(obj.values("line_id","line_name"))
	return JsonResponse(data, safe=False)
#	data = json.dumps(data)
#	data = serializers.serialize('json', list(objectQuerySet), fields=('id', 'line_id', 'line_name'))
#	return JsonResponse(list(data), safe=False)
#data = get_object_or_404(LegendData)
#return HttpResponse(json.dumps(data))
#return render_to_response("template.html", {"legend_data": json.dumps(data)})

def contrib_sources_by_party(request):
	return render(request, "blog/ContributionSourcesByParty.html", {})
	
def contrib_sources_data(request):
	obj = ContribSourcesByParty.objects.all()
	data = list(obj.values("interest_category","democrat", "republican"))
	return JsonResponse(data, safe=False)

def test_retrieval(request):
	objs = LegendData.objects.all()
	return render(request, "blog/test_retrieval.html", {"retrieval": objs})
	
def contributor_data(request, cand, year):

	if year == "2014":
		frm_date = date(2012,11,6)
		to_date = date(2014, 11, 4)
	
	#cand += cand.replace(",", ", ")
	qryst = ContributorData.objects.filter(
		candidate=cand
	).filter(
		date__gte=frm_date
	).filter(
		date__lte=to_date
	).order_by(
	 	"date"
	)
	
	cumulative = 0
	data = list(qryst.values("candidate", "date", "cumulative", "amount", "contributor"))
	for i, dat in enumerate(data):
		cumulative += dat["amount"]
		dat["cumulative"] = cumulative
	
	return JsonResponse(data, safe=False)
	
def candidate_data(request, house, year):
	info = "Received: " + year
	qryst = CandidateData.objects.filter(
		house=house
	).filter(
		year_ran__year=year
	).order_by(
	 	"year_ran"
	)
	data = list(qryst.values("candidate", "year_ran", "party", "house", "district", "won"))
	return JsonResponse(data, safe=False)
	
def index(request):
	return render(request, "blog/index.html", {})
	
	
def legislative_contributions(request):
	return render(request, "blog/legislative_contributions.html", {})

