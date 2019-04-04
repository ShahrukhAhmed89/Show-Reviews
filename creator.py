import os, django
from datetime  import datetime, timedelta
from django.db.models import Avg, Count
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_settings.settings')
from django.urls import reverse
django.setup()
from dramas.models import Show
from reviews.models import Reviews
from jinja2 import Template
from django.db.models.functions import Coalesce

###################################################################################################################

template_trend_month = """
<h2>TRENDING DRAMAS THIS WEEK</h2>
<div class="scroll">
    <ul class="trending">
    {% for show in list_ %}
        <li class="trending__drama">
            <a href="{{show.url}}">
                <div class="drama__poster">
                    <img src="{{show.img}}">
                    <div class="drama__name">{{show.title}}</div>
                </div>
            </a>
            <div class="drama-rating">{{show.avg_rating}}</div>	
        </li>
    {% endfor %}
    </ul>
</div>
"""

trend_list = []
shows = Show.objects.filter(release_date__range=(datetime.now()-timedelta(days=30), datetime.now())).annotate(avg_rating=Coalesce(Avg('reviews__rating'),0)).order_by('-avg_rating')[0:10]

for show in shows:
    drama = {}
    drama["title"] = show.title
    drama["img"] = show.image_portrait.url
    drama["url"] = reverse('show:show_page',kwargs={'id': show.id, 'slug':show.slug})
    drama["avg_rating"] = round(show.avg_rating,1)
    trend_list.append(drama)

f = open('templates/components/home_components/trend_month.html','w')
template = Template(template_trend_month)
render = template.render(list_=trend_list)
f.write(render)
f.close()





###################################################################################################################
template_new_drama= """
<h2>NEW DRAMA</h2>
<div class="scroll">
    <ul class="recent">
    {% for show in list_ %}
        <li class="recent__drama">
            <a href="{{show.url}}">
                <div class="drama__poster">
                    <img src="{{show.img}}">
                    <div class="drama__name">{{show.title}}</div>
                </div>
            </a>
            <div class="drama-rating">{{show.avg_rating}}</div>
        </li>
    {% endfor %}
    </ul>
</div>
"""
new_drama = []
shows = Show.objects.filter(release_date__range=(datetime.now()-timedelta(days=30), datetime.now())).annotate(avg_rating=Coalesce(Avg('reviews__rating'),0))[0:10]

for show in shows:
    drama = {}
    drama["title"] = show.title
    drama["img"] = show.image_portrait.url
    drama["url"] = reverse('show:show_page',kwargs={'id': show.id, 'slug':show.slug})
    drama["avg_rating"] = round(show.avg_rating,1)
    new_drama.append(drama)


f = open('templates/components/home_components/new_drama.html','w')
template = Template(template_new_drama)
render = template.render(list_=new_drama)
f.write(render)
f.close()




###################################################################################################################
template_all_time = """
<h2>ALL-TIME FAVOURITE</h2>
<div class="scroll">
    <ul class="favourite">
    {% for show in list_ %}
        <li class="favourite__drama">
            <a href="{{show.url}}">
                <div class="drama__poster"><img src="{{show.img}}"></div>
                <div class="drama__text">
                    <div class="drama__name">{{show.title}}</div>
                    <div class="drama-rating">{{show.avg_rating}}</div>
                    <span class="drama__rate-votes">{{show.no_of_ratings}}</span>
                </div>
            </a>
        </li>
    {% endfor %}
    </ul>
</div>
"""
all_time = []
shows = Show.objects.all().annotate(avg_rating=Coalesce(Avg('reviews__rating'),0), no_of_ratings=Count('reviews'))[0:10]

for show in shows:
    drama = {}
    drama["title"] = show.title
    drama["img"] = show.image_portrait.url
    drama["url"] = reverse('show:show_page',kwargs={'id': show.id, 'slug':show.slug})
    drama["avg_rating"] = round(show.avg_rating,1)
    drama["no_of_ratings"] = show.no_of_ratings
    all_time.append(drama)


f = open('templates/components/home_components/all_time.html','w')
template = Template(template_all_time)
render = template.render(list_=all_time)
f.write(render)
f.close()






###################################################################################################################
template_upcoming = """
<h2>UPCOMING DRAMA</h2>
<div class="scroll">
    <ul class="upcoming">
        {% for show in list_ %}
        <li class="upcoming__drama">
            <a href="{{show.url}}">
                <div class="drama__poster">
                    <img src="{{show.img}}">
                    <div class="drama__name">{{show.title}}</div>
                </div>
            </a>
        </li>
        {% endfor %}
    </ul>
</div>	
"""
all_time = []
shows = Show.objects.filter(release_date__gte=datetime.today())[0:10]

for show in shows:
    drama = {}
    drama["title"] = show.title
    drama["img"] = show.image_portrait.url
    drama["url"] = reverse('show:show_page',kwargs={'id': show.id, 'slug':show.slug})
    all_time.append(drama)


f = open('templates/components/home_components/upcoming.html','w')
template = Template(template_upcoming)
render = template.render(list_=all_time)
f.write(render)
f.close()





###################################################################################################################
template_top__reviews = """
<h2>TRENDING REVIEW</h2>
{% for review in list_ %}
<div class="review-trend">	
    <div class="user__profile">
       <img src="{{review.author_img}}">
    </div>
    <div class="review__detail">
        <div class="details__info">
            <span class="info__user-name">{{review.author}}</span>
            <span>&nbsp;review of&nbsp;</span>
            <span class="info__drama-name"><a href="{{review.show_url}}">{{review.show}}</a></span>
        </div>
        <div class="review__rate">
            <div class="drama-rating">{{review.rating}}</div>	
            <div class="like__button"></div>
            <div class="like__count">{{review.upvotes}}</div>
        </div>
    </div>
    <div class="review__text">
        <p>{{review.post}}</p>
    </div>
</div>
{% endfor %}
"""

top_reviews = []
reviews = Reviews.objects.filter(post_date_created__gte=datetime.now()-timedelta(days=7))[0:10]

for review in reviews:
    user_review = {}
    user_review["show"] = review.show.title
    user_review["author"] = review.user
    user_review["author_img"] = review.user.avatar.url if review.user.avatar  else '/static/girl.png'
    user_review["show_url"] = reverse('show:show_page',kwargs={'id':  review.show.id, 'slug': review.show.slug})
    user_review["rating"] = review.rating
    user_review["post"] = review.post
    user_review["upvotes"] = review.user_like_count
    top_reviews.append(user_review)


f = open('templates/components/home_components/top_reviews.html','w')
template = Template(template_top__reviews)
render = template.render(list_=top_reviews)
f.write(render)
f.close()
