from datetime import datetime

def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits', '1'))
    last_time_visit = request.COOKIES.get('last_time_visit', str(datetime.now()))
    last_time = datetime.strptime(last_time_visit[:-7],'%Y-%m-%d %H:%M:%S')
    print(visits)
    if((datetime.now() - last_time).seconds > 1):
        visits = visits + 1
        last_time_visit = str(datetime.now())
    response.set_cookie('last_time_visit', last_time_visit)
    response.set_cookie('visits', visits)

def return_visits(request):
    visits = int(request.COOKIES.get('visits', '1'))
    return visits

